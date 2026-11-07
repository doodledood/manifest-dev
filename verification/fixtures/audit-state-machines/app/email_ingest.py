import db


def on_reply(ticket_id: str, text: str) -> None:
    """A customer reply reopens a closed ticket; replies to open tickets just add a message."""
    t = db.TICKETS[ticket_id]
    t["messages"].append(text)
    t["status"] = "open"
