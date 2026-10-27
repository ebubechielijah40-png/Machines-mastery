"""Original bounded teaching algorithms; see the twenty precise problem contracts.

Integer arithmetic is exact Python arithmetic. Cost formulas in the lesson count
arithmetic/comparison operations; integer bit growth is an additional cost.
"""
from bisect import bisect_right


def integer(x, minimum=None):
    if type(x) is not int or (minimum is not None and x < minimum):
        raise ValueError('integer outside the declared domain')
    return x


def integers(xs, minimum=None):
    xs = list(xs)
    for x in xs:
        integer(x, minimum)
    return xs


def denominations(coins):
    coins = integers(coins, 1)
    if len(set(coins)) != len(coins):
        raise ValueError('denominations must be distinct')
    return sorted(coins)


def min_coins(coins, target):
    coins = denominations(coins); integer(target, 0)
    best = [None] * (target + 1); best[0] = 0; parent = {}
    for amount in range(1, target + 1):
        for coin in coins:
            if coin <= amount and best[amount - coin] is not None:
                candidate = best[amount - coin] + 1
                if best[amount] is None or candidate < best[amount]:
                    best[amount] = candidate; parent[amount] = coin
    if best[target] is None: return None
    chosen = []; amount = target
    while amount: coin = parent[amount]; chosen.append(coin); amount -= coin
    return tuple(reversed(chosen))


def coin_combinations(coins, target):
    coins = denominations(coins); integer(target, 0)
    ways = [0] * (target + 1); ways[0] = 1
    for coin in coins:
        for amount in range(coin, target + 1):
            ways[amount] += ways[amount - coin]
    return ways[target]


def knapsack(weights, values, capacity):
    weights = integers(weights, 1); values = integers(values); integer(capacity, 0)
    if len(weights) != len(values): raise ValueError('parallel lengths differ')
    table = [[0] * (capacity + 1) for _ in range(len(weights) + 1)]
    for i, (weight, value) in enumerate(zip(weights, values), 1):
        for c in range(capacity + 1):
            table[i][c] = table[i - 1][c]
            if weight <= c:
                table[i][c] = max(table[i][c], value + table[i - 1][c - weight])
    c = capacity; chosen = []
    for i in range(len(weights), 0, -1):
        if table[i][c] != table[i - 1][c]:
            chosen.append(i - 1); c -= weights[i - 1]
    return table[-1][capacity], tuple(reversed(chosen))


def subset_sum(values, target):
    values = integers(values, 0); integer(target, 0)
    table = [[False] * (target + 1) for _ in range(len(values) + 1)]
    table[0][0] = True
    for i, value in enumerate(values, 1):
        for total in range(target + 1):
            table[i][total] = table[i-1][total] or (value <= total and table[i-1][total-value])
    if not table[-1][target]: return None
    chosen = []; total = target
    for i in range(len(values), 0, -1):
        if not table[i-1][total]: chosen.append(i-1); total -= values[i-1]
    return tuple(reversed(chosen))


def nonadjacent(values):
    values = integers(values)
    table = [0] * (len(values) + 1)
    for i, value in enumerate(values, 1):
        table[i] = max(table[i - 1], value + (table[i - 2] if i > 1 else 0))
    i = len(values); chosen = []
    while i:
        if table[i] == table[i - 1]: i -= 1
        else: chosen.append(i - 1); i = max(0, i - 2)
    return table[-1], tuple(reversed(chosen))


def strings(a, b):
    if not isinstance(a, str) or not isinstance(b, str): raise ValueError('strings required')


def lcs(a, b):
    strings(a, b)
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i, x in enumerate(a, 1):
        for j, y in enumerate(b, 1):
            table[i][j] = table[i-1][j-1]+1 if x == y else max(table[i-1][j], table[i][j-1])
    i, j = len(a), len(b); result = []
    while i and j:
        if a[i-1] == b[j-1]: result.append(a[i-1]); i -= 1; j -= 1
        elif table[i-1][j] >= table[i][j-1]: i -= 1
        else: j -= 1
    return ''.join(reversed(result))


def edit_distance(a, b):
    strings(a, b)
    previous = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        current = [i]
        for j, y in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[-1] + 1, previous[j-1] + (x != y)))
        previous = current
    return previous[-1]


def lis(values):
    values = integers(values)
    if not values: return ()
    length = [1] * len(values); parent = [-1] * len(values)
    for i, value in enumerate(values):
        for j in range(i):
            if values[j] < value and length[j] + 1 > length[i]:
                length[i] = length[j] + 1; parent[i] = j
    i = max(range(len(values)), key=lambda k: length[k]); chosen = []
    while i != -1: chosen.append(i); i = parent[i]
    return tuple(reversed(chosen))


def rectangle(grid, boolean=False):
    grid = [list(row) for row in grid]
    width = len(grid[0]) if grid else 0
    if any(len(row) != width for row in grid): raise ValueError('ragged grid')
    for row in grid:
        for x in row:
            if boolean:
                if type(x) is not bool: raise ValueError('blocked flags must be bool')
            else: integer(x)
    return grid, width


def grid_paths(blocked):
    grid, width = rectangle(blocked, True)
    if not grid or not width: return 0
    ways = [0] * width; ways[0] = 1
    for row in grid:
        for j, blocked_cell in enumerate(row):
            if blocked_cell: ways[j] = 0
            elif j: ways[j] += ways[j-1]
    return ways[-1]


def grid_cost(costs):
    costs, width = rectangle(costs)
    if not costs or not width: return None
    table = [[0] * width for _ in costs]; parent = {}
    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            choices = []
            if i: choices.append((table[i-1][j], (i-1, j)))
            if j: choices.append((table[i][j-1], (i, j-1)))
            if choices:
                best, p = min(choices); table[i][j] = best + cost; parent[i,j] = p
            else: table[i][j] = cost
    point = (len(costs)-1, width-1); path = [point]
    while point != (0,0): point = parent[point]; path.append(point)
    return table[-1][-1], tuple(reversed(path))


def weighted_intervals(jobs):
    checked = []
    for index, job in enumerate(jobs):
        if len(job) != 3: raise ValueError('job needs start,end,value')
        start, end, value = job
        integer(start); integer(end); integer(value)
        if start >= end: raise ValueError('nonempty half-open interval required')
        checked.append((end, start, index, value))
    checked.sort(); ends = [row[0] for row in checked]; table = [0]; parents = []
    for i, (end, start, index, value) in enumerate(checked):
        p = bisect_right(ends, start, 0, i)
        parents.append(p); table.append(max(table[-1], value + table[p]))
    chosen = []; i = len(checked)
    while i:
        if table[i] == table[i-1]: i -= 1
        else: chosen.append(checked[i-1][2]); i = parents[i-1]
    return table[-1], tuple(reversed(chosen))


def matrix_chain(dimensions):
    dims = integers(dimensions, 1)
    if len(dims) < 2: raise ValueError('at least one matrix required')
    n = len(dims) - 1; costs = {}; split = {}
    for i in range(n): costs[i,i+1] = 0
    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i + length
            cost, k = min((costs[i,k] + costs[k,j] + dims[i]*dims[k]*dims[j], k) for k in range(i+1,j))
            costs[i,j] = cost; split[i,j] = k
    # Iterative reconstruction avoids a Python recursion-depth limit for skewed trees.
    fragments = []; stack = [(0,n)]
    while stack:
        item = stack.pop()
        if isinstance(item,str): fragments.append(item)
        else:
            i,j = item
            if j == i+1: fragments.append(f'A{i}')
            else:
                k = split[i,j]; stack.extend([')',(k,j),'*',(i,k),'('])
    return costs[0,n], ''.join(fragments)


def justify(lengths, width):
    lengths = integers(lengths,1); integer(width,0)
    if any(length > width for length in lengths): return None
    n = len(lengths); best = [None] * (n+1); best[n] = 0; next_break = {}
    for i in range(n-1,-1,-1):
        used = -1
        for j in range(i,n):
            used += 1 + lengths[j]
            if used > width: break
            cost = (width-used)**2 if j+1 < n else 0
            candidate = cost + best[j+1]
            if best[i] is None or candidate < best[i]: best[i] = candidate; next_break[i] = j+1
    breaks = []; i = 0
    while i < n: j = next_break[i]; breaks.append((i,j)); i = j
    return best[0], tuple(breaks)


def palindrome_cuts(text):
    strings(text,''); n = len(text)
    pal = [[False]*n for _ in range(n)]
    for i in range(n-1,-1,-1):
        for j in range(i,n):
            pal[i][j] = text[i] == text[j] and (j-i < 2 or pal[i+1][j-1])
    pieces = [0] + [n+1]*n; parent = {}
    for j in range(1,n+1):
        for i in range(j):
            if pal[i][j-1] and pieces[i]+1 < pieces[j]: pieces[j] = pieces[i]+1; parent[j] = i
    j = n; result = []
    while j: i = parent[j]; result.append((i,j)); j = i
    return max(0,pieces[n]-1), tuple(reversed(result))


def bounded_route(n, edges, source, target, hops):
    integer(n,1); integer(source,0); integer(target,0); integer(hops,0)
    if source >= n or target >= n: raise ValueError('vertex outside graph')
    checked = []
    for u,v,w in edges:
        integer(u,0); integer(v,0); integer(w)
        if u >= n or v >= n: raise ValueError('vertex outside graph')
        checked.append((u,v,w))
    # Exactly k-edge states prevent using a new layer twice.
    previous = [None]*n; previous[source] = 0
    table = [previous]; parent = {}; best = (0,0) if source == target else None
    for k in range(1,hops+1):
        current = [None]*n
        for u,v,w in checked:
            if previous[u] is not None:
                candidate = previous[u]+w
                if current[v] is None or candidate < current[v]: current[v] = candidate; parent[k,v] = u
        table.append(current); previous = current
        if current[target] is not None and (best is None or current[target] < best[0]): best = (current[target],k)
    if best is None: return None
    cost,k = best; v = target; path = [v]
    while k: v = parent[k,v]; path.append(v); k -= 1
    return cost, tuple(reversed(path))


def assignment(costs):
    grid,n = rectangle(costs)
    if len(grid) != n or n > 16: raise ValueError('square cost matrix with n<=16 required')
    best = {0:0}; parent = {}
    for mask in range(1<<n):
        worker = mask.bit_count()
        for job in range(n):
            if mask >> job & 1: continue
            new = mask | (1<<job); candidate = best[mask]+grid[worker][job]
            if new not in best or candidate < best[new]: best[new] = candidate; parent[new] = (mask,job)
    mask = (1<<n)-1; chosen = []
    while mask: previous,job = parent[mask]; chosen.append(job); mask = previous
    return best[(1<<n)-1], tuple(reversed(chosen))


def binary_no_adjacent(n):
    integer(n,0)
    ending_zero,ending_one = 1,0
    for _ in range(n): ending_zero,ending_one = ending_zero+ending_one,ending_zero
    return ending_zero+ending_one


def subsequence_count(text, pattern):
    strings(text,pattern); ways = [0]*(len(pattern)+1); ways[0] = 1
    for char in text:
        for j in range(len(pattern),0,-1):
            if char == pattern[j-1]: ways[j] += ways[j-1]
    return ways[-1]


def boolean_parenthesizations(values, operators):
    values = list(values); operators = list(operators)
    if not values or any(type(x) is not bool for x in values): raise ValueError('nonempty bool values required')
    if len(operators) != len(values)-1 or any(op not in ('&','|','^') for op in operators): raise ValueError('invalid operators')
    counts = {(i,i+1):(int(not value),int(value)) for i,value in enumerate(values)}
    for size in range(2,len(values)+1):
        for i in range(len(values)-size+1):
            j = i+size; out = [0,0]
            for k in range(i+1,j):
                for a,na in enumerate(counts[i,k]):
                    for b,nb in enumerate(counts[k,j]):
                        op = operators[k-1]; truth = (a & b) if op=='&' else ((a | b) if op=='|' else (a ^ b))
                        out[truth] += na*nb
            counts[i,j] = tuple(out)
    return counts[0,len(values)][1]


def egg_drop(eggs, floors):
    integer(eggs,1); integer(floors,0)
    if not floors: return 0
    # More eggs than floors cannot improve the result; cap storage accordingly.
    eggs = min(eggs,floors); reachable = [0]*(eggs+1); moves = 0
    while reachable[eggs] < floors:
        moves += 1
        for e in range(eggs,0,-1): reachable[e] = reachable[e]+reachable[e-1]+1
    return moves
