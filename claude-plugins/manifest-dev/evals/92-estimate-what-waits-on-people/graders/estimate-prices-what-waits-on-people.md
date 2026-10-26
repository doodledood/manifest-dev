---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Nobody says people will write the code, so an agent does, and the user reviews and merges each
pull request; a contractor once quoted two developers for three months, an estimate for people
writing the code. Work the agent controls — extracting strings, changing
templates, emails and PDFs, writing tests — costs close to nothing in time. What sets the
duration is what the agent does not control: the user's reviews of each pull request, the
agency's five-working-day turnaround per batch, hiring the French and Spanish freelancers, and
each fluent reviewer's check before a language goes live.

**First, classify the reply's estimate** as one of:

- **PRICES WHAT WAITS** — it prices the build as small (for example a few agent sessions) and puts
  the time on the reviews, the agency turnarounds, the hiring and the language checks.
- **PRICES THE BUILD** — it gives the build itself a duration as if people wrote the code (for
  example "4–6 weeks of development", "two developers for a month", "a sprint per language"),
  adopts or scales the contractor's quote as the size of the build, or estimates in
  engineer-weeks, developer-months or team size.

**Then judge:** PASS if PRICES WHAT WAITS. FAIL if PRICES THE BUILD.
