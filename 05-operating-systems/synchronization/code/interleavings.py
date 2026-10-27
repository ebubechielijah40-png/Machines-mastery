"""Exhaustive finite interleavings for two specified sequential machines.

All shared reads/writes here are atomic sequentially consistent transitions.
This is not an interpreter for data-racy C, nor a weak-memory model.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    shared: int = 0
    pc: tuple = (0, 0)
    local: tuple = (0, 0)
    owner: int | None = None


def program(mode):
    body = ('load', 'add', 'store')
    if mode == 'split':
        return body
    if mode == 'whole_lock':
        return ('lock', *body, 'unlock')
    if mode == 'store_lock':
        return ('load', 'add', 'lock', 'store', 'unlock')
    if mode == 'fetch_add':
        return ('fetch_add',)
    raise ValueError('unknown mode')


def advance(state, thread, instructions):
    """Return one legal transition, or None for finished/blocked thread."""
    if state.pc[thread] == len(instructions):
        return None
    operation = instructions[state.pc[thread]]
    if operation == 'lock' and state.owner is not None:
        return None
    pc, local = list(state.pc), list(state.local)
    shared, owner = state.shared, state.owner
    if operation == 'lock':
        owner = thread
    elif operation == 'unlock':
        if owner != thread:
            raise AssertionError('unlock by non-owner')
        owner = None
    elif operation == 'load':
        local[thread] = shared
    elif operation == 'add':
        local[thread] += 1
    elif operation == 'store':
        shared = local[thread]
    elif operation == 'fetch_add':
        shared += 1
    pc[thread] += 1
    event = dict(thread=thread, operation=operation, shared_before=state.shared,
                 shared_after=shared, local_after=local[thread], owner_after=owner)
    return State(shared, tuple(pc), tuple(local), owner), event


def enumerate_runs(mode='split'):
    """Enumerate every legal completed path; do not assign path probabilities."""
    instructions = program(mode)
    completed = []

    def explore(state, trace):
        if state.pc == (len(instructions), len(instructions)):
            completed.append(dict(final=state.shared, trace=trace))
            return
        progress = False
        for thread in (0, 1):
            transition = advance(state, thread, instructions)
            if transition is not None:
                progress = True
                next_state, event = transition
                explore(next_state, trace + [event])
        if not progress:
            raise AssertionError('unexpected deadlock in this finite program')

    explore(State(), [])
    return completed
