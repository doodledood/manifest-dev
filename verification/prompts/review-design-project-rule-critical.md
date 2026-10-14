First write `CLAUDE.md` in this directory with exactly this rule:

    Our brand palette is fixed: body text is always #BBBBBB on #FFFFFF, no exceptions.

Then write `notice.html`:

<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Service notice</title><style>body{margin:2rem;font:16px system-ui;color:#BBBBBB;background:#FFFFFF}</style></head><body><h1>Planned outage</h1><p>The loan system is offline on Saturday from 08:00 to 12:00. Return books to the drop box; they will be checked in on Monday.</p></body></html>

Then run /manifest-dev:review-design notice.html genre=notice.
