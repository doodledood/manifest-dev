You are evaluating gates from a Manifest against a built app. Evaluate only the gates below, as
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

Return, for each gate, PASS or FAIL, and list every defect you found with the steps that show it and
what the person met.

## The gates

### INV-G14 — Two friends plan one trip end to end

Live drive in a real browser on the running server, roughly a few minutes against a local server
with seeded users. Person A (signed out, phone viewport) opens the trip link, signs in, lands back
on the same trip, and adds "Feira da Ladra". Person B, in another session, opens the same link,
sees that place in List, and switches to Day plan. B sets the start to 8:00. A reloads Day plan.

PASS when A gets back to the trip after signing in without retyping the link, B sees A's place in
both modes, B's plan starts at 8:00, A's plan is unchanged at A's own start time, and no step shows
an error.

Judgment gate.

### INV-G13 — The page works and reads well on a phone

Run the server with a seeded trip (3 days, 12–14 May; 10 places, some with long names and notes;
two users) and activate the `review-design` skill on `/trips/<id>` in both modes. Review it at a
360 px wide phone viewport and at a desktop width. Include the empty trip, the validation error
state, and the signed-out state. There are no mocks or reference designs to match.

The loop to judge against: a friend taps the link in a group chat on their phone, scans what
others have saved, adds a place with their thumb, flips to Day plan, and maybe changes their start
time. Done when the skill reports nothing at or above its threshold and there is no horizontal
page scroll at 360 px.

Judgment gate.
