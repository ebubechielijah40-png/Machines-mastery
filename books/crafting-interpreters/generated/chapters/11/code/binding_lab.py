"""Original bounded AST language: lexical resolution, closures, mutable cells.

This is not Nystrom's Lox implementation. No parser, classes, native calls or I/O
are exposed. The mutable-chain mode is an intentional experimental control.
"""
from dataclasses import dataclass
from types import MappingProxyType
import re


class BindingError(ValueError):
    """Invalid AST or statically invalid declaration/use."""


class ExecutionError(ValueError):
    """Undefined runtime name, type/arity mismatch, or exceeded execution bound."""


@dataclass(frozen=True, eq=False)
class Literal:
    value: object


@dataclass(frozen=True, eq=False)
class Name:
    name: str


@dataclass(frozen=True, eq=False)
class Assign:
    name: str
    value: object


@dataclass(frozen=True, eq=False)
class Add:
    left: object
    right: object


@dataclass(frozen=True, eq=False)
class Subtract:
    left: object
    right: object


@dataclass(frozen=True, eq=False)
class Equal:
    left: object
    right: object


@dataclass(frozen=True, eq=False)
class Call:
    callee: object
    arguments: tuple = ()


@dataclass(frozen=True, eq=False)
class Let:
    name: str
    initializer: object


@dataclass(frozen=True, eq=False)
class Function:
    name: str
    parameters: tuple
    body: tuple


@dataclass(frozen=True, eq=False)
class Block:
    body: tuple


@dataclass(frozen=True, eq=False)
class Return:
    value: object


@dataclass(frozen=True, eq=False)
class Print:
    value: object


@dataclass(frozen=True, eq=False)
class Expression:
    value: object


@dataclass(frozen=True, eq=False)
class If:
    condition: object
    consequent: object
    alternative: object


EXPRESSIONS = (Literal, Name, Assign, Add, Subtract, Equal, Call)
STATEMENTS = (Let, Function, Block, Return, Print, Expression, If)


def _identifier(name):
    if type(name) is not str or re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]{0,63}', name) is None:
        raise BindingError('identifier must contain 1..64 ASCII identifier characters')


def _validate(body):
    if type(body) is not tuple:
        raise BindingError('a program/body/argument list must be an immutable tuple')
    seen = set()

    def visit(node, depth, expected):
        if type(node) not in expected:
            raise BindingError('AST node is in the wrong grammatical position')
        if id(node) in seen:
            raise BindingError('each AST occurrence must be a distinct node; shared/cyclic AST rejected')
        seen.add(id(node))
        if depth > 80 or len(seen) > 2000:
            raise BindingError('AST exceeds depth80/node2000 teaching bound')
        if isinstance(node, Literal):
            if type(node.value) not in (int, str, bool, type(None)):
                raise BindingError('literal must be integer, text, Boolean or None')
            if type(node.value) is int and node.value.bit_length() > 4096:
                raise BindingError('integer literal exceeds 4096 bits')
            if type(node.value) is str and len(node.value) > 1000:
                raise BindingError('text literal exceeds1000 characters')
        if isinstance(node, (Name, Assign, Let, Function)):
            _identifier(node.name)
        if isinstance(node, Function):
            if type(node.parameters) is not tuple or len(node.parameters) > 32:
                raise BindingError('function parameters must be a tuple of at most32 names')
            for name in node.parameters:
                _identifier(name)
            if len(set(node.parameters)) != len(node.parameters):
                raise BindingError('duplicate parameter')
        if isinstance(node, (Function, Block)):
            if type(node.body) is not tuple:
                raise BindingError('body must be a tuple')
            for child in node.body:
                visit(child, depth + 1, STATEMENTS)
        elif isinstance(node, Call):
            if type(node.arguments) is not tuple or len(node.arguments) > 32:
                raise BindingError('arguments must be a tuple of at most32 expressions')
            visit(node.callee, depth + 1, EXPRESSIONS)
            for child in node.arguments:
                visit(child, depth + 1, EXPRESSIONS)
        elif isinstance(node, If):
            visit(node.condition, depth + 1, EXPRESSIONS)
            visit(node.consequent, depth + 1, STATEMENTS)
            visit(node.alternative, depth + 1, STATEMENTS)
        elif isinstance(node, Let):
            visit(node.initializer, depth + 1, EXPRESSIONS)
        elif isinstance(node, (Return, Print, Expression, Assign)):
            visit(node.value, depth + 1, EXPRESSIONS)
        elif isinstance(node, (Add, Subtract, Equal)):
            visit(node.left, depth + 1, EXPRESSIONS)
            visit(node.right, depth + 1, EXPRESSIONS)
    for statement in body:
        visit(statement, 0, STATEMENTS)


@dataclass(frozen=True)
class Program:
    body: tuple
    addresses: object

    def run(self, *, lookup='resolved', steps=10000, call_limit=64):
        if lookup not in ('resolved', 'mutable-chain'):
            raise ExecutionError('unknown lookup mode')
        if type(steps) is not int or not 1 <= steps <= 100000:
            raise ExecutionError('steps must be integer1..100000')
        if type(call_limit) is not int or not 1 <= call_limit <= 64:
            raise ExecutionError('call_limit must be integer1..64')
        machine = _Machine(self.addresses, lookup, steps, call_limit)
        try:
            machine.statements(self.body, machine.globals)
        except RecursionError as exc:
            raise ExecutionError('host traversal stack exhausted before explicit call bound') from exc
        return {'output': machine.output, 'steps': steps - machine.remaining,
                'lookup': lookup}


def compile_program(body):
    """Validate then resolve without evaluating a program or its branches."""
    _validate(body)
    scopes = []
    addresses = {}
    function_depth = 0

    def declare(name):
        if scopes:
            if name in scopes[-1]:
                raise BindingError('duplicate local declaration: ' + name)
            scopes[-1][name] = False

    def define(name):
        if scopes:
            scopes[-1][name] = True

    def reference(node):
        if scopes and scopes[-1].get(node.name) is False:
            raise BindingError('local read/write in its own initializer: ' + node.name)
        for distance, scope in enumerate(reversed(scopes)):
            if node.name in scope:
                addresses[node] = distance
                return
        addresses[node] = None  # A runtime global slot, never caller-local search.

    def expression(node):
        if isinstance(node, Name):
            reference(node)
        elif isinstance(node, Assign):
            expression(node.value)
            reference(node)
        elif isinstance(node, (Add, Subtract, Equal)):
            expression(node.left)
            expression(node.right)
        elif isinstance(node, Call):
            expression(node.callee)
            for item in node.arguments:
                expression(item)

    def statements(body):
        for statement in body:
            resolve(statement)

    def resolve(node):
        nonlocal function_depth
        if isinstance(node, Let):
            declare(node.name)
            expression(node.initializer)
            define(node.name)
        elif isinstance(node, Function):
            declare(node.name)
            define(node.name)  # Self-reference is legal in the body.
            scopes.append({})
            function_depth += 1
            try:
                for parameter in node.parameters:
                    declare(parameter)
                    define(parameter)
                statements(node.body)
            finally:
                function_depth -= 1
                scopes.pop()
        elif isinstance(node, Block):
            scopes.append({})
            try:
                statements(node.body)
            finally:
                scopes.pop()
        elif isinstance(node, Return):
            if not function_depth:
                raise BindingError('return outside a function')
            expression(node.value)
        elif isinstance(node, If):
            expression(node.condition)
            resolve(node.consequent)
            resolve(node.alternative)
        elif isinstance(node, (Print, Expression)):
            expression(node.value)
    statements(body)
    return Program(body, MappingProxyType(addresses))


class _Frame:
    def __init__(self, parent=None):
        self.parent = parent
        self.values = {}


@dataclass
class _Closure:
    declaration: Function
    captured: _Frame


class _Returned(Exception):
    def __init__(self, value):
        self.value = value


class _Machine:
    def __init__(self, addresses, lookup, steps, call_limit):
        self.addresses = addresses
        self.lookup = lookup
        self.globals = _Frame()
        self.output = []
        self.remaining = steps
        self.call_limit = call_limit
        self.call_depth = 0

    def tick(self):
        if self.remaining == 0:
            raise ExecutionError('step budget exhausted; prior effects are not rolled back')
        self.remaining -= 1

    def target(self, node, environment):
        if self.lookup == 'mutable-chain':
            frame = environment
            while frame is not None:
                if node.name in frame.values:
                    return frame
                frame = frame.parent
            raise ExecutionError('undefined name: ' + node.name)
        depth = self.addresses[node]
        frame = self.globals if depth is None else environment
        if depth is not None:
            for _ in range(depth):
                if frame.parent is None:
                    raise ExecutionError('resolver/runtime frame mismatch')
                frame = frame.parent
        if node.name not in frame.values:
            raise ExecutionError('undefined resolved name: ' + node.name)
        return frame

    def expression(self, node, environment):
        self.tick()
        if isinstance(node, Literal):
            return node.value
        if isinstance(node, Name):
            return self.target(node, environment).values[node.name]
        if isinstance(node, Assign):
            value = self.expression(node.value, environment)
            self.target(node, environment).values[node.name] = value
            return value
        if isinstance(node, (Add, Subtract, Equal)):
            left = self.expression(node.left, environment)
            right = self.expression(node.right, environment)
            if isinstance(node, Equal):
                if type(left) is not type(right):
                    return False
                if type(left) not in (int, str, bool, type(None)):
                    raise ExecutionError('equality accepts primitive values only')
                return left == right
            if type(left) is not int or type(right) is not int:
                raise ExecutionError('arithmetic requires integer operands, excluding Booleans')
            result = left + right if isinstance(node, Add) else left - right
            if result.bit_length() > 4096:
                raise ExecutionError('arithmetic result exceeds4096 bits')
            return result
        if isinstance(node, Call):
            closure = self.expression(node.callee, environment)
            arguments = [self.expression(x, environment) for x in node.arguments]
            if not isinstance(closure, _Closure):
                raise ExecutionError('callee is not a function')
            declaration = closure.declaration
            if len(arguments) != len(declaration.parameters):
                raise ExecutionError('argument count differs from parameter count')
            if self.call_depth >= self.call_limit:
                raise ExecutionError('call depth bound exhausted')
            frame = _Frame(closure.captured)
            frame.values.update(zip(declaration.parameters, arguments))
            self.call_depth += 1
            try:
                self.statements(declaration.body, frame)
            except _Returned as returned:
                return returned.value
            finally:
                self.call_depth -= 1
            return None
        raise ExecutionError('invalid expression after validation')

    def statements(self, body, environment):
        for statement in body:
            self.statement(statement, environment)

    def statement(self, node, environment):
        self.tick()
        if isinstance(node, Let):
            environment.values[node.name] = self.expression(node.initializer, environment)
        elif isinstance(node, Function):
            environment.values[node.name] = _Closure(node, environment)
        elif isinstance(node, Block):
            self.statements(node.body, _Frame(environment))
        elif isinstance(node, Expression):
            self.expression(node.value, environment)
        elif isinstance(node, Print):
            value = self.expression(node.value, environment)
            if isinstance(value, _Closure):
                raise ExecutionError('printing closure objects is outside the primitive-output language')
            self.output.append(value)
        elif isinstance(node, Return):
            raise _Returned(self.expression(node.value, environment))
        elif isinstance(node, If):
            condition = self.expression(node.condition, environment)
            if type(condition) is not bool:
                raise ExecutionError('condition must be Boolean')
            self.statement(node.consequent if condition else node.alternative, environment)
        else:
            raise ExecutionError('invalid statement after validation')
