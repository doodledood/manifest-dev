# Ticket store

**Venue:** files, in this repository.

Tickets live at `tickets/<effort-slug>/NN-<ticket-slug>.md`, each effort carrying a front file
at `tickets/<effort-slug>/README.md`. Closed Tickets move to that effort's `done/`.

## Why files here

The venue question is whether the store must be a live surface that workers not sharing a
working tree can both read — that is what a hosted tracker buys, and it is the whole of what it
buys. This project is worked by one person, so no claim needs to be visible across clones.

A hosted tracker was considered and refused on two counts. On this repository's own issue
tracker the store would be public and writable by anyone, which the project does not want for
its working queue. In a second, private repository the store would be unreachable by outsiders
but split across two places, and the friction of maintaining it there outweighs what the live
surface would buy while nobody else picks work.

## What this venue cannot do

Claims do not cross clones, worktrees, or branches. A Ticket claimed in one checkout is
invisible to any session working from another until the claim is merged. Two sessions that do
not share a working tree can therefore pick the same Ticket.

That is the condition to watch: if unattended runs in fresh checkouts ever pick work from this
store, this venue stops being adequate and the store moves to a private repository's issue
tracker. Switching is a rewrite of this file plus a migration of the Ticket files, not a
redesign.
