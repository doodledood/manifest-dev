---
tags: [figure-out]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this.

we're adding servings scaling to recipes in our cooking app, Simmer. phone only. the why is settled: most recipes are written for four, most of our cooks cook for one or two, and today they do the maths in their heads — they scale while writing a shopping list and again at the stove, often with wet or floury hands. the quantity maths is built and tested, and Simmer already remembers each cook's usual number of servings and opens every recipe scaled to it — so this control is only for the exceptions: guests, batch cooking, halving a recipe. a one-off change is also settled: it sticks to that recipe until the cook resets it, and the recipe then shows a "scaled for 6 · usually 2" label with a reset. the recipe screen is one scrolling page — photo, title, the ingredients list, then the steps — and there's no separate cooking mode; the steps repeat their quantities inline. what's still open is the interface: where the servings control lives on the recipe screen and how many taps it takes to change it. let's figure out the design.
