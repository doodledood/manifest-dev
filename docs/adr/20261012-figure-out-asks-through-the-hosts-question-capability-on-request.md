# ADR: figure-out asks through the host's question capability when the user asks for it

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context
figure-out writes its one ask per turn in plain text. `20260727-figure-out-adopts-a-default-turn-shape` rejected delivering asks through the harness's question-selection primitive on three grounds: a reader typed free text through it, so its convenience went unused; it is harness-bound where the skill names capabilities in universal language; and a menu invites a rubber-stamp. Those grounds hold for most users. Some users still prefer to answer by choosing an option, and they had no way to get it.

## Decision
Plain text stays the default. When the user's instructions ask for it and the host offers a question-selection capability, figure-out delivers the ask through that capability, with its recommended answer as the first option. The rule names the capability in universal language, so it binds no single harness. Autonomous runs still never ask, and team mode still asks in its channel.

## Alternatives Considered
- **Keep plain text for everyone**: users who prefer to choose from options keep retyping answers the run already proposed.
- **Use the capability by default**: the 2026-07-27 grounds still hold for the default reader — a menu invites the rubber-stamp.
- **A flag**: a flag is one more thing to remember; the user's standing instructions already carry preferences like this.

## Consequences

### Positive
- A user who prefers options gets them through one line in their own instructions.
- The default experience does not change.

### Negative
- A user who asks for the capability accepts the rubber-stamp risk the default avoids.
- Behavior differs between hosts that offer the capability and hosts that do not.

## Source
- Session: figure-out investigation of how figure-out reaches its user.
- Narrows 20260727-figure-out-adopts-a-default-turn-shape: its rejected alternative of delivering asks through the question-selection primitive is now taken on the user's request.
- Amends 20260803-figure-out-turn-carries-one-concrete-claim: the ask stays alone and carries its recommended answer; it is in prose by default rather than always.
