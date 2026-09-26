# General-purpose authoring excerpts

These artifact excerpts come from the candidate-only text exercise described in
[the verification report](README.md). They are proposed content, not deployed files.

## Reusable onboarding

Acceptance required all role links to reach the common facts and a common requirement
to change through one edit. The constraint allowed Markdown only.

### Finished guide text

Keep these Markdown files in the same directory. For the two existing guides, the snippets replace their repeated common setup sections; other content is preserved. File names are proposed for the exercise because actual paths were not supplied.

`setup.md`:

````markdown
# Common setup

This guide covers common setup for engineers, analysts, and support staff. It does not cover role-specific workflows.

## Installation

Run the installation command:

```sh
acme init
```

## Token requirements

A token is the credential used to access a project. Its scope is the access it permits.

Use a token with read-only project scope. Rotate the token every 90 days by replacing it with a new token.

Token creation, where to enter the token, and the steps for replacing it are not specified in this guide.
````

Replacement common setup section in `engineer.md`:

```markdown
## Common setup

Follow [Common setup](setup.md) for installation and token requirements.
```

Replacement common setup section in `analyst.md`:

```markdown
## Common setup

Follow [Common setup](setup.md) for installation and token requirements.
```

`support.md`:

```markdown
# Support onboarding

This guide covers common setup for support staff. It does not cover support workflows.

Follow [Common setup](setup.md) for installation and token requirements.
```


## One-off meeting note

Acceptance required the supplied date, room, decision topic, and attendee count,
without invented logistics or a reusable system.

### Finished artifact

```markdown
# Budget allocation meeting: 2026-09-27

The meeting is in Cedar with three attendees. The decision is how to allocate the budget.
```


## Feature using a sound existing dispatcher

Acceptance required gamma arithmetic, unchanged alpha/beta behavior, and use of the
existing success-recording path. Runtime verification remained unperformed because
the application and recording interface were not supplied.

### Implementation text

The finished registry is:

```python
transformations = {
    'alpha': lambda x: x + 1,
    'beta': lambda x: x * 2,
    'gamma': lambda x: x - 1,
}
```

In the actual source, preserve existing formatting and add only `'gamma': lambda x: x - 1`. Leave `run(name, value)` unchanged. Call the new operation through `run("gamma", value)` just as alpha and beta are called. The stated dispatcher already records every successful result before returning, so routing through it preserves that property without an extra wrapper or recorder.
