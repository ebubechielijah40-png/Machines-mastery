"""Finite one-producer/one-consumer predicate/wakeup transition model.

Atomic wait registration releases the mutex and records a waiter together.
A bounded optional spurious wake is an explicit model event, not a probability.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class ConditionState:
    consumer: str = 'lock'
    producer: int = 0
    owner: str | None = None
    full: bool = False
    waiting: bool = False
    spurious_left: int = 0
    consumed: int = 0
    fault: bool = False


def transitions(state, protocol):
    options = []

    def add(actor, operation, **changes):
        result = replace(state, **changes)
        options.append((result, dict(actor=actor, operation=operation,
                                     owner_after=result.owner, full_after=result.full,
                                     waiting_after=result.waiting)))

    consumer = state.consumer
    if consumer in {'lock', 'relock'} and state.owner is None:
        following = 'consume' if consumer == 'relock' and protocol == 'if' else 'check'
        add('consumer', 'acquire', owner='consumer', consumer=following)
    elif consumer == 'check':
        assert state.owner == 'consumer'
        add('consumer', 'check_predicate', consumer='consume' if state.full else 'wait')
    elif consumer == 'wait':
        assert state.owner == 'consumer'
        if protocol == 'split_wait':
            add('consumer', 'release_without_register', owner=None, consumer='register')
        else:
            add('consumer', 'atomic_release_and_register', owner=None,
                waiting=True, consumer='blocked')
    elif consumer == 'register':
        add('consumer', 'register_too_late', waiting=True, consumer='blocked')
    elif consumer == 'consume':
        assert state.owner == 'consumer'
        if not state.full:
            add('consumer', 'consume_empty', fault=True)
        else:
            add('consumer', 'consume', full=False, consumed=1, consumer='unlock')
    elif consumer == 'unlock':
        add('consumer', 'release', owner=None, consumer='done')

    producer = state.producer
    if producer == 0 and state.owner is None:
        add('producer', 'acquire', owner='producer', producer=1)
    elif producer == 1:
        assert state.owner == 'producer'
        add('producer', 'put_item', full=True, producer=2)
    elif producer == 2:
        changes = dict(producer=3)
        if state.waiting:
            changes.update(waiting=False, consumer='relock')
        add('producer', 'notify_waiter' if state.waiting else 'notify_no_waiter', **changes)
    elif producer == 3:
        add('producer', 'release', owner=None, producer=4)

    if state.waiting and state.spurious_left:
        add('environment', 'spurious_wake', waiting=False, consumer='relock',
            spurious_left=state.spurious_left - 1)
    return options


def enumerate_conditions(protocol='while', spurious_budget=0):
    if protocol not in {'while', 'if', 'split_wait'}:
        raise ValueError('unknown condition protocol')
    if type(spurious_budget) is not int or not 0 <= spurious_budget <= 1:
        raise ValueError('spurious budget is zero or one')
    completed = []

    def explore(state, trace):
        if state.fault:
            outcome = 'safety_failure'
        elif state.consumer == 'done' and state.producer == 4:
            outcome = 'complete'
        else:
            choices = transitions(state, protocol)
            if choices:
                for next_state, event in choices:
                    explore(next_state, trace + [event])
                return
            outcome = 'blocked'
        completed.append(dict(outcome=outcome, consumed=state.consumed,
                              full=state.full, trace=trace))

    explore(ConditionState(spurious_left=spurious_budget), [])
    return completed
