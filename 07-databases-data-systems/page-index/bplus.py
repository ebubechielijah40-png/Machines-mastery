"""Original bounded byte-page B+ index. No transactions, filesystem or locks.

Pages are re-encoded after modification. Counters measure requests to this byte
page map, never disk I/O. The snapshot format is ours, not SQLite's format.
"""
from bisect import bisect_left, bisect_right
from dataclasses import dataclass
import math
import struct
import zlib

MIN_KEY = -(1 << 63)
MAX_KEY = (1 << 63) - 1
MAX_VALUE = 24
MAX_ITEMS = 100_000
MAX_PAGES = 65_535
MAX_IMAGE_BYTES = 16 * 1024 * 1024
PAGE_HEADER = struct.Struct('>4sBBHII')
LEAF_CELL = struct.Struct('>qB24s')
INNER_CELL = struct.Struct('>qI')
IMAGE_HEADER = struct.Struct('>8sHHIIIQ')
CRC = struct.Struct('>I')


def key_number(value):
    if type(value) is not int or not MIN_KEY <= value <= MAX_KEY:
        raise ValueError('key must be an actual signed 64-bit integer')
    return value


def value_bytes(value):
    if type(value) is not bytes or len(value) > MAX_VALUE:
        raise ValueError('value must be bytes of length 0 through 24')
    return value


def page_size_number(value):
    if type(value) is not int or not 128 <= value <= 4096 or value & (value - 1):
        raise ValueError('page size must be a power of two from 128 through 4096')
    return value


def capacities(page_size):
    page_size_number(page_size)
    payload = page_size - PAGE_HEADER.size - CRC.size
    return payload // LEAF_CELL.size, payload // INNER_CELL.size


@dataclass(frozen=True)
class Node:
    page_id: int
    leaf: bool
    keys: tuple
    values: tuple = ()
    children: tuple = ()
    next_leaf: int = 0


def encode_node(node, page_size):
    """Validate one page's local shape and emit a canonical fixed-size byte page."""
    leaf_cap, inner_cap = capacities(page_size)
    if not isinstance(node, Node) or type(node.leaf) is not bool:
        raise ValueError('Node with boolean leaf kind required')
    if type(node.page_id) is not int or not 1 <= node.page_id <= MAX_PAGES:
        raise ValueError('invalid page id')
    if type(node.keys) is not tuple or any(type(x) is not int for x in node.keys):
        raise ValueError('keys must be a tuple of signed integers')
    for key in node.keys:
        key_number(key)
    if any(a >= b for a, b in zip(node.keys, node.keys[1:])):
        raise ValueError('page keys must be strictly increasing')
    cap = leaf_cap if node.leaf else inner_cap
    if len(node.keys) > cap:
        raise ValueError('page overflow')
    if node.leaf:
        if node.children or type(node.values) is not tuple or len(node.values) != len(node.keys):
            raise ValueError('leaf value/key shape mismatch')
        if type(node.next_leaf) is not int or not 0 <= node.next_leaf <= MAX_PAGES or node.next_leaf == node.page_id:
            raise ValueError('invalid leaf successor')
        for value in node.values:
            value_bytes(value)
        link = node.next_leaf
        cells = b''.join(LEAF_CELL.pack(key, len(value), value.ljust(MAX_VALUE, b'\0'))
                         for key, value in zip(node.keys, node.values))
    else:
        if node.values or node.next_leaf != 0 or type(node.children) is not tuple or len(node.children) != len(node.keys) + 1:
            raise ValueError('internal child/key shape mismatch')
        if any(type(x) is not int or not 1 <= x <= MAX_PAGES or x == node.page_id for x in node.children):
            raise ValueError('invalid child id')
        if len(set(node.children)) != len(node.children):
            raise ValueError('duplicate child within page')
        link = node.children[0]
        cells = b''.join(INNER_CELL.pack(key, child) for key, child in zip(node.keys, node.children[1:]))
    header = PAGE_HEADER.pack(b'BPI1', 1 if node.leaf else 2, 0, len(node.keys), node.page_id, link)
    body = (header + cells).ljust(page_size - CRC.size, b'\0')
    return body + CRC.pack(zlib.crc32(body) & 0xffffffff)


def decode_node(raw, page_size, expected_id=None):
    capacities(page_size)
    if type(raw) is not bytes or len(raw) != page_size:
        raise ValueError('one exact byte page required')
    body = raw[:-CRC.size]
    if CRC.unpack(raw[-CRC.size:])[0] != zlib.crc32(body) & 0xffffffff:
        raise ValueError('page checksum mismatch')
    magic, kind, reserved, count, page_id, link = PAGE_HEADER.unpack_from(body)
    if magic != b'BPI1' or kind not in (1, 2) or reserved != 0:
        raise ValueError('unknown page header')
    if expected_id is not None and page_id != expected_id:
        raise ValueError('page id does not match its position')
    leaf = kind == 1
    if count > capacities(page_size)[0 if leaf else 1]:
        raise ValueError('unbounded page count')
    keys, values, children = [], [], [link] if not leaf else []
    cursor = PAGE_HEADER.size
    for _ in range(count):
        if leaf:
            key, length, value = LEAF_CELL.unpack_from(body, cursor)
            if length > MAX_VALUE or any(value[length:]):
                raise ValueError('invalid value length or noncanonical value padding')
            keys.append(key); values.append(value[:length]); cursor += LEAF_CELL.size
        else:
            key, child = INNER_CELL.unpack_from(body, cursor)
            keys.append(key); children.append(child); cursor += INNER_CELL.size
    if any(body[cursor:]):
        raise ValueError('nonzero unallocated bytes')
    node = Node(page_id, leaf, tuple(keys), tuple(values), tuple(children), link if leaf else 0)
    # Reuse all local type/order/range constraints and enforce one canonical image.
    if encode_node(node, page_size) != raw:
        raise ValueError('noncanonical page')
    return node


class _Pages:
    def __init__(self, page_size, max_pages):
        self.page_size = page_size_number(page_size)
        if type(max_pages) is not int or not 1 <= max_pages <= MAX_PAGES:
            raise ValueError('max_pages must be an actual integer from 1 through 65535')
        self.max_pages = max_pages
        self.raw = {}
        self.next_id = 1
        self.reads = self.writes = 0

    def read(self, page_id):
        self.reads += 1
        try:
            return decode_node(self.raw[page_id], self.page_size, page_id)
        except KeyError:
            raise ValueError('dangling child or leaf link') from None


class _Edit:
    """Staged bytes avoid exposing ordinary validation/capacity failures mid-put.

    This is not process-crash recovery or a multi-thread transaction. Python
    MemoryError during commit is outside the teaching contract.
    """
    def __init__(self, pages):
        self.pages, self.pending, self.next_id = pages, {}, pages.next_id

    def read(self, page_id):
        if page_id in self.pending:
            self.pages.reads += 1
            return decode_node(self.pending[page_id], self.pages.page_size, page_id)
        return self.pages.read(page_id)

    def write(self, node):
        self.pending[node.page_id] = encode_node(node, self.pages.page_size)

    def allocate(self, leaf, keys, values=(), children=(), next_leaf=0):
        if self.next_id > self.pages.max_pages:
            raise ValueError('configured page budget exhausted')
        page_id = self.next_id
        self.next_id += 1
        self.write(Node(page_id, leaf, tuple(keys), tuple(values), tuple(children), next_leaf))
        return page_id

    def commit(self):
        self.pages.raw.update(self.pending)
        self.pages.next_id = self.next_id
        self.pages.writes += len(self.pending)


class BPlusIndex:
    def __init__(self, page_size=128, max_pages=MAX_PAGES):
        self._pages = _Pages(page_size, max_pages)
        self.leaf_capacity, self.inner_capacity = capacities(page_size)
        edit = _Edit(self._pages)
        self.root = edit.allocate(True, (), ())
        edit.commit()
        self.size = 0

    def _insert(self, edit, page_id, key, value):
        node = edit.read(page_id)
        keys = list(node.keys)
        if node.leaf:
            i = bisect_left(keys, key)
            values = list(node.values)
            if i < len(keys) and keys[i] == key:
                values[i] = value
                edit.write(Node(page_id, True, tuple(keys), tuple(values), next_leaf=node.next_leaf))
                return None, False
            keys.insert(i, key); values.insert(i, value)
            if len(keys) <= self.leaf_capacity:
                edit.write(Node(page_id, True, tuple(keys), tuple(values), next_leaf=node.next_leaf))
                return None, True
            middle = len(keys) // 2
            right = edit.allocate(True, keys[middle:], values[middle:], next_leaf=node.next_leaf)
            edit.write(Node(page_id, True, tuple(keys[:middle]), tuple(values[:middle]), next_leaf=right))
            return (keys[middle], right), True
        i = bisect_right(keys, key)
        children = list(node.children)
        split, added = self._insert(edit, children[i], key, value)
        if split is None:
            return None, added
        separator, right = split
        keys.insert(i, separator); children.insert(i + 1, right)
        if len(keys) <= self.inner_capacity:
            edit.write(Node(page_id, False, tuple(keys), children=tuple(children)))
            return None, added
        middle = len(keys) // 2
        promoted = keys[middle]
        right = edit.allocate(False, keys[middle + 1:], children=children[middle + 1:])
        edit.write(Node(page_id, False, tuple(keys[:middle]), children=tuple(children[:middle + 1])))
        return (promoted, right), added

    def put(self, key, value):
        key_number(key); value_bytes(value)
        # If at the row budget, an overwrite is still permitted. This extra
        # lookup occurs only at that boundary and is included in page counters.
        if self.size >= MAX_ITEMS and self.get(key) is None:
            raise ValueError('configured row budget exhausted')
        edit = _Edit(self._pages)
        split, added = self._insert(edit, self.root, key, value)
        new_root = self.root if split is None else edit.allocate(False, (split[0],), children=(self.root, split[1]))
        edit.commit()
        self.root = new_root
        self.size += int(added)

    def _leaf(self, key):
        node = self._pages.read(self.root)
        while not node.leaf:
            node = self._pages.read(node.children[bisect_right(node.keys, key)])
        return node

    def get(self, key):
        key_number(key)
        node = self._leaf(key)
        i = bisect_left(node.keys, key)
        return node.values[i] if i < len(node.keys) and node.keys[i] == key else None

    def range(self, start=None, stop=None):
        """Materialized ordered [start,stop); None means an unbounded endpoint."""
        if start is not None:
            key_number(start)
        if stop is not None:
            key_number(stop)
        if start is not None and stop is not None and start >= stop:
            return []
        node = self._leaf(MIN_KEY if start is None else start)
        result = []
        seen = set()
        while True:
            if node.page_id in seen:
                raise ValueError('leaf-link cycle')
            seen.add(node.page_id)
            for key, value in zip(node.keys, node.values):
                if stop is not None and key >= stop:
                    return result
                if start is None or key >= start:
                    result.append((key, value))
            if node.next_leaf == 0:
                return result
            node = self._pages.read(node.next_leaf)
            if not node.leaf:
                raise ValueError('leaf link targets an internal page')

    def reset_metrics(self):
        self._pages.reads = self._pages.writes = 0

    def metrics(self):
        return {'page_decode_requests': self._pages.reads,
                'committed_page_images': self._pages.writes,
                'allocated_pages': len(self._pages.raw), 'rows': self.size}

    def validate(self):
        """Check every reachable page, bounds, occupancies, equal depth and links.

        Iterative traversal also rejects maliciously deep snapshots without
        depending on Python's recursion limit. These reads are audit work,
        excluded from query counters; validation costs O(all stored bytes).
        """
        pages = self._pages
        if type(self.root) is not int or self.root not in pages.raw:
            raise ValueError('missing root')
        if set(pages.raw) != set(range(1, pages.next_id)):
            raise ValueError('noncontiguous page identifiers')
        pending = [(self.root, False, None, None)]
        visited, facts, leaves = set(), {}, []
        while pending:
            page_id, expanded, lower, upper = pending.pop()
            if not expanded:
                if page_id in visited:
                    raise ValueError('cycle or page shared by multiple parents')
                visited.add(page_id)
                if page_id not in pages.raw:
                    raise ValueError('dangling child')
                node = decode_node(pages.raw[page_id], pages.page_size, page_id)
                if any((lower is not None and key < lower) or
                       (upper is not None and key >= upper) for key in node.keys):
                    raise ValueError('subtree outside separator interval')
                if page_id != self.root:
                    minimum = (self.leaf_capacity + 1) // 2 if node.leaf else self.inner_capacity // 2
                    if len(node.keys) < minimum:
                        raise ValueError('underfull nonroot page')
                elif not node.leaf and not node.keys:
                    raise ValueError('internal root must branch')
                if node.leaf:
                    leaves.append(node)
                    facts[page_id] = (node.keys[0] if node.keys else None,
                                      node.keys[-1] if node.keys else None, 0, len(node.keys))
                else:
                    pending.append((page_id, True, lower, upper))
                    limits = (lower,) + node.keys + (upper,)
                    for i in range(len(node.children) - 1, -1, -1):
                        pending.append((node.children[i], False, limits[i], limits[i + 1]))
            else:
                node = decode_node(pages.raw[page_id], pages.page_size, page_id)
                children = [facts[child] for child in node.children]
                if any(child[0] is None for child in children):
                    raise ValueError('empty subtree below internal page')
                if len({child[2] for child in children}) != 1:
                    raise ValueError('unequal leaf depth')
                if tuple(child[0] for child in children[1:]) != node.keys:
                    raise ValueError('separator is not right-subtree minimum')
                facts[page_id] = (children[0][0], children[-1][1], children[0][2] + 1,
                                  sum(child[3] for child in children))
        if visited != set(pages.raw):
            raise ValueError('orphan pages')
        for i, leaf in enumerate(leaves):
            expected = leaves[i + 1].page_id if i + 1 < len(leaves) else 0
            if leaf.next_leaf != expected:
                raise ValueError('leaf links disagree with tree order')
        if facts[self.root][3] != self.size:
            raise ValueError('stored row count mismatch')
        return {'height_edges': facts[self.root][2], 'leaf_pages': len(leaves),
                'pages': len(visited), 'rows': self.size}

    @classmethod
    def from_sorted(cls, items, page_size=128, max_pages=MAX_PAGES):
        """Bottom-up packing; caller must supply strictly increasing keys."""
        tree = cls(page_size, max_pages)
        rows, previous = [], None
        for row in items:
            if not isinstance(row, (tuple, list)) or len(row) != 2:
                raise ValueError('bulk rows must be key/value pairs')
            key, value = row
            key_number(key); value_bytes(value)
            if previous is not None and key <= previous:
                raise ValueError('bulk input must have strictly increasing keys')
            if len(rows) >= MAX_ITEMS:
                raise ValueError('configured row budget exhausted')
            rows.append((key, value)); previous = key
        if not rows:
            return tree

        def groups(sequence, capacity):
            count = math.ceil(len(sequence) / capacity)
            small, extra = divmod(len(sequence), count)
            cursor = 0
            for i in range(count):
                length = small + (i < extra)
                yield sequence[cursor:cursor + length]
                cursor += length

        edit = _Edit(tree._pages)
        level, minimum = [], {}
        for i, chunk in enumerate(groups(rows, tree.leaf_capacity)):
            keys = tuple(x[0] for x in chunk); values = tuple(x[1] for x in chunk)
            page_id = 1 if i == 0 else edit.allocate(True, keys, values)
            edit.write(Node(page_id, True, keys, values))
            if level:
                old = edit.read(level[-1])
                edit.write(Node(old.page_id, True, old.keys, old.values, next_leaf=page_id))
            level.append(page_id); minimum[page_id] = keys[0]
        while len(level) > 1:
            next_level = []
            for children in groups(level, tree.inner_capacity + 1):
                page_id = edit.allocate(False, tuple(minimum[x] for x in children[1:]), children=tuple(children))
                minimum[page_id] = minimum[children[0]]
                next_level.append(page_id)
            level = next_level
        edit.commit(); tree.root = level[0]; tree.size = len(rows)
        tree.validate()
        return tree

    def dumps(self):
        self.validate()
        pages = self._pages
        header = IMAGE_HEADER.pack(b'MMBPLUS1', 1, pages.page_size, self.root,
                                   len(pages.raw), pages.max_pages, self.size)
        size = len(header) + CRC.size + len(pages.raw) * pages.page_size
        if size > MAX_IMAGE_BYTES:
            raise ValueError('snapshot exceeds 16 MiB input/output limit')
        return header + CRC.pack(zlib.crc32(header) & 0xffffffff) + b''.join(pages.raw[i] for i in range(1, pages.next_id))

    @classmethod
    def loads(cls, image):
        if type(image) is not bytes or not IMAGE_HEADER.size + CRC.size <= len(image) <= MAX_IMAGE_BYTES:
            raise ValueError('bounded snapshot bytes required')
        header, crc = image[:IMAGE_HEADER.size], image[IMAGE_HEADER.size:IMAGE_HEADER.size + CRC.size]
        if CRC.unpack(crc)[0] != zlib.crc32(header) & 0xffffffff:
            raise ValueError('snapshot header checksum mismatch')
        magic, version, page_size, root, count, max_pages, rows = IMAGE_HEADER.unpack(header)
        if magic != b'MMBPLUS1' or version != 1:
            raise ValueError('unknown snapshot version')
        page_size_number(page_size)
        pages = _Pages(page_size, max_pages)
        if not 1 <= root <= count <= max_pages or rows > MAX_ITEMS:
            raise ValueError('invalid snapshot counts/root')
        offset = IMAGE_HEADER.size + CRC.size
        if len(image) != offset + count * page_size:
            raise ValueError('truncated or trailing snapshot bytes')
        for page_id in range(1, count + 1):
            raw = image[offset:offset + page_size]
            decode_node(raw, page_size, page_id)
            pages.raw[page_id] = raw; offset += page_size
        pages.next_id = count + 1
        tree = cls.__new__(cls)
        tree._pages, tree.root, tree.size = pages, root, rows
        tree.leaf_capacity, tree.inner_capacity = capacities(page_size)
        tree.validate()
        return tree
