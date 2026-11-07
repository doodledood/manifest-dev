"""Subscription lifecycle. Every status change goes through fire(), keyed by event and status."""

from enum import Enum


class Status(Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"


EVENTS: dict[str, dict[Status, Status]] = {
    "convert": {Status.TRIAL: Status.ACTIVE},
    "cancel": {
        Status.TRIAL: Status.CANCELLED,
        Status.ACTIVE: Status.CANCELLED,
        Status.PAUSED: Status.CANCELLED,
    },
    "pause": {Status.ACTIVE: Status.PAUSED},
    "resume": {Status.PAUSED: Status.ACTIVE},
}


class IllegalTransition(Exception):
    pass


def fire(sub: dict, event: str) -> None:
    current = sub["status"]
    moves = EVENTS[event]
    if current not in moves:
        raise IllegalTransition(f"{event} from {current.value}")
    sub["status"] = moves[current]
