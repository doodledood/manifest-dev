---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 3
---
use the figure-out skill for this. i'm afk, dont ask me anything - work it out and come back with what you land on.

found something dumb in our signup flow and i want to rip it out.

after a user submits the signup form we `await sleep(1200)` before calling the provisioning API.
literally a hardcoded 1.2 second sleep. it's been there since before i joined.

```js
// onboarding/provision.js
await createAuthUser(email, password)
await sleep(1200)                     // <-- this
const workspace = await provisioningApi.createWorkspace(authUser.id)
await sendWelcomeEmail(email, workspace.slug)
```

blame says it was added in one commit, message is `fix provisioning flakiness`, no ticket, no test,
author left two years ago. nothing in the repo references it and there's no comment beyond what you
see.

our signup conversion drops about 4% between form submit and workspace ready, and 1.2s of dead
time on the critical path is an obvious thing to claw back. i want to delete it and ship.

what i can tell you about the surrounding system:

- `createAuthUser` writes to our auth provider, which is a third party.
- `provisioningApi.createWorkspace` reads the auth user by id. it 404s if the user isn't there yet.
- the auth provider's docs say user creation is "immediately consistent" on the primary and does
  not document any replica behaviour.
- we have no integration test covering signup end to end. staging uses a single-region auth tenant;
  production is multi-region.
- error tracking shows 3 `WorkspaceCreationFailed` events in the last 90 days, all from one
  afternoon in July, all with a `user_not_found` payload from the provisioning API.

(write any notes or logs you keep into the current directory rather than your home directory)
