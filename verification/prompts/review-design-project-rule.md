First write `CLAUDE.md` in this directory with exactly this rule:

    Our internal dashboards are used only on the office's 1920px wall screens. Pages are built for a fixed 1920px width; we do not build narrow or mobile layouts.

Then write `dash.html`:

<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Loans</title><style>body{width:1920px;margin:0;font:18px system-ui;color:#111;background:#fff} main{display:grid;grid-template-columns:repeat(4,460px);gap:20px;padding:20px} h1{grid-column:1/-1} a:focus-visible{outline:3px solid #0050b3}</style></head><body><main><h1>Loans today</h1><section><h2>Out</h2><p>42</p></section><section><h2>Overdue</h2><p>7</p></section><section><h2>Returned</h2><p>15</p></section><section><h2>Members</h2><p>31</p></section><a href="#">Open the loan list</a></main></body></html>

Then run /manifest-dev:review-design dash.html genre=dashboard.
