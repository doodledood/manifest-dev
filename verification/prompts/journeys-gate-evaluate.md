You are evaluating a gate from a Manifest against a built app. Evaluate only the gate below, as
written, and nothing else.

The app is in this directory: `node app/server.js` serves it (README.md says how). Drive it in a real
browser: Playwright is installed, `require('playwright')` works from any directory, and
`chromium.launch()` needs no options. Where a gate names another skill and that skill is
available, use it; otherwise apply what the gate says yourself. Where a gate refers to criteria you
cannot see, ignore that reference. Work from what the page shows, not from reading the code.

What the page is for: the Saved places page for a shared trip in Waymark, a trip planner people use
on their phones while planning a trip with friends. A trip has an owner and a few days. Each trip
page has its own address and people share it in group chats. The page lists the places people saved
for the trip, and anyone signed in can add one. Two modes, switched at the top: List (every saved
place) and Day plan, which lays the saved places out as a day-by-day plan for the trip with a
suggested time for each. Day plan has its own setting, the time each day starts, kept per person.
Sign-in is by email.

Return PASS or FAIL, and list every defect you found with the steps that show it and
what the person met.

## The gate

### INV-G24 — Journeys driven as a friend in the group chat

The person is a member of a trip's group chat, mostly on a phone, who taps a shared `/trips/<id>` link. Derive their journeys yourself from that person and this page, covering at least: arriving signed out from a chat app's in-app browser; coming back later on another device or after a reload; switching between List and Day plan and using back; changing the day start and seeing the plan move; adding a place while a friend adds one; a trip with no places and a trip with many; what goes wrong (bad connection, rejected name, unknown trip id). Drive the running app through each journey in a browser at phone size, as that person, with evidence (screenshots or recorded steps) of what they met. PASS when no journey leaves the person stuck, confused about what happened, or looking at wrong data. FAIL otherwise. Booting needs the server running with a seeded trip and at least two signed-in test accounts; return BLOCKED, not a code-reading verdict, when it cannot be booted. A run drives many browser journeys by hand and is the slowest gate here; evaluate it on a settled state rather than mid-repair.

Judgment gate.
