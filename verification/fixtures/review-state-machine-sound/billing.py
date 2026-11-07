from subscription import Status, fire


def on_trial_converted(sub: dict) -> None:
    fire(sub, "convert")


def on_cancel_requested(sub: dict) -> None:
    fire(sub, "cancel")


def should_charge(sub: dict) -> bool:
    return sub["status"] is Status.ACTIVE
