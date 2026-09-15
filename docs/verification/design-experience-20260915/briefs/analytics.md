# Harbor ferry operations

Create a complete, self-contained HTML analytical app view for a ferry operations lead. At the start of a shift they compare three routes, decide which needs investigation, and change the day-type cohort to check whether the pattern persists. The same view is used repeatedly on a desktop and occasionally on a phone.

The data below is a fictional demonstration, not live service data. It covers the latest four weeks and a comparison with the preceding four weeks. A trip is on time when it arrives no more than five minutes after its scheduled arrival. **On-time percentage uses all scheduled trips as its denominator, including cancellations.** Cancellations are separate counts, not additional late arrivals to add to a percentage. These counts establish no causal explanation for delay.

| Day type | Route | Scheduled trips | On-time trips | Cancellations | Previous on-time rate |
|---|---|---:|---:|---:|---:|
| Weekday | West Pier | 200 | 174 | 8 | 92% |
| Weekday | East Bank | 160 | 152 | 2 | 94% |
| Weekday | North Quay | 120 | 108 | 4 | 90% |
| Weekend | West Pier | 80 | 76 | 1 | 93% |
| Weekend | East Bank | 96 | 84 | 3 | 91% |
| Weekend | North Quay | 60 | 57 | 1 | 94% |

Initial state: Weekday, with West Pier selected. Users must be able to compare all three routes within the selected cohort, select a route to inspect its counts and rate change, and switch between Weekday and Weekend. Keep the displayed route and cohort clear. All displayed measures must update consistently. No live fetch, account, save flow or simulated loading is needed.

Choose the information structure and visual language yourself. Preserve the evidence needed to interpret the numbers, including the denominator and the fact that this is sample data. The view should feel like a finished, distinctive analytical tool, not a collection of placeholder cards.

Delivery: one offline HTML file with embedded CSS and JavaScript; no external fonts, images, libraries or network requests. Use native HTML, CSS and SVG where useful. Support desktop and phone, keyboard and pointer input. No existing design system or visual mock is supplied.
