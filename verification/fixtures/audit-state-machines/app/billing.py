"""Shop subscription plans. Every change of plan goes through fire(), keyed by event and plan."""

from enum import Enum


class Plan(Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    LAPSED = "lapsed"


EVENTS: dict[str, dict[Plan, Plan]] = {
    "paid": {Plan.TRIAL: Plan.ACTIVE, Plan.ACTIVE: Plan.ACTIVE, Plan.LAPSED: Plan.ACTIVE},
    "card_expired": {Plan.TRIAL: Plan.LAPSED, Plan.ACTIVE: Plan.LAPSED, Plan.LAPSED: Plan.LAPSED},
}


def fire(shop: dict, event: str) -> None:
    shop["plan"] = EVENTS[event][shop["plan"]]


def on_payment(shop: dict) -> None:
    fire(shop, "paid")


def on_card_expired(shop: dict) -> None:
    fire(shop, "card_expired")
