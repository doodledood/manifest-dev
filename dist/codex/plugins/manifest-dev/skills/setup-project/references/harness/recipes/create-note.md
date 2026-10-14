---
kind: feature
covers: src/notes/create.ts, src/ui/editor.tsx
---
# Create a note

A user saves a titled note from the browser or the CLI, can cancel an unfinished draft, and finds
the saved note again from the note list.

## How a user reaches it

- The `New note` button in the browser toolbar.
- Pressing `n` in the browser while focus is outside a text field.
- `notes create --title <title> --body <body>` in a terminal.

## Scenarios

### browser-save
Run: `scripts/control-notes recipe create-note --flow browser-save --artifacts artifacts/create-note`
Proves: the `Note editor` opens from the button and from `n`, saves `Release checklist`, and the
note reads back from `All notes`; the snapshot and screenshot show it.

### cancel-draft
Run: `scripts/control-notes recipe create-note --flow cancel-draft`
Proves: a draft typed as `Discard me` and cancelled does not appear in the list.

### cli
Run: `scripts/control-notes cli -- notes create --title "CLI note" --body "From terminal" --format json`
Proves: exit code 0, and stdout holds the new note's ID and title.

## Gotchas

- Pressing `n` inside a text field types the letter instead of opening an editor.
- Titles are trimmed on save. Compare against the rendered title, not the typed value.
- `Note saved` alone proves nothing. Reopen the note from the list.
- `tests/e2e/create_note.spec.ts` covers the save path on every build but stops at the save
  toast; `browser-save` adopts the same launcher and goes on to reopen the note and keep the
  snapshot, which the spec does not.
