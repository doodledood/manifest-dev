import db


def open_ticket(ticket_id: str, text: str) -> None:
    db.TICKETS[ticket_id] = {"status": "open", "messages": [text]}


def close_ticket(ticket_id: str) -> None:
    db.TICKETS[ticket_id]["status"] = "closed"
