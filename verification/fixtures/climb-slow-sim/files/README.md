# trafficsim

A traffic simulation people watch as it plays: cars follow each other, stop at lights and merge.
`sim/` is the simulation; each `World.step()` advances one frame at 30 frames per second.

- `python3 -m measure.full` — the realism review: plays every preset for ten simulated minutes
  over several seeds and scores how real the motion is (smooth braking, no snapping, no
  collisions, no teleporting lane changes). It is slow. Higher is better; it also prints each
  preset's 99th-percentile frame time against the budget.
- `python3 -m measure.quick_check` — renders one still frame of the `grid` preset and checks car
  spacing and positions. It takes under a second.
- `python3 -m pytest -q` — behavior tests.

The simulation must keep 99% of frames under 20 ms with the `rush_hour` preset's cars, so it plays at
50 frames per second or better on a mid-range laptop.
