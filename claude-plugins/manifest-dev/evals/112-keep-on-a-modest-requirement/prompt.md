---
# Holds the decision in docs/adr/20261116-figure-out-presses-on-need-by-what-rests-on-it.md — that record's Enforced by line names this case; weakening or removing it means updating that line in the same change.
tags: [figure-out-multi-turn]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this — we're continuing a session. here is where we were, then my answer.

---
**my request, earlier:**

> we're adding a proper recipe page to our cooking blog: the ingredients, the steps, a jump-to-recipe link at the top of the post, metric and US units (about half our readers are in the US), and a print view.

**then you said:**

> The print view adds a print stylesheet that hides the story, the ads and the comments, and a print button on each recipe. I found no reader asking for it, and browsers already print the page as it is. Without it, a reader who prints gets the whole post. I would leave it out.
>
> **Ask:** keep the print view, or cut it? My recommended answer: cut.

**my answer:**

> keep.
---

(write any notes or logs you keep into the current directory rather than your home directory)
<!-- next turn -->
next thing: the ingredient amounts should scale when someone changes the number of servings. how should that work?
<!-- next turn -->
thanks. name the read.
