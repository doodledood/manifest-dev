import logging

import db

log = logging.getLogger(__name__)


def request_refund(delivery_id: str) -> bool:
    r = db.REFUNDS.get(delivery_id)
    if r is not None:
        return False
    db.REFUNDS[delivery_id] = {"status": "refund_pending"}
    return True


def on_processor_result(delivery_id: str, ok: bool) -> None:
    r = db.REFUNDS[delivery_id]
    if ok:
        r["status"] = "refunded"
    else:
        log.warning("refund for %s declined by processor", delivery_id)
