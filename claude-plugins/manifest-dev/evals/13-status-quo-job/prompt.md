---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 3
---
use the figure-out skill for this. i'm afk, dont ask me anything - work it out and come back with what you land on.

found something dumb in our device enrollment flow and i want to rip it out.

after a tech registers a device we `await sleep(1200)` before calling the fleet API.
literally a hardcoded 1.2 second sleep. it's been there since before i joined.

```js
// enrollment/register.js
await createDeviceIdentity(serial, certFingerprint)
await sleep(1200)                     // <-- this
const fleet = await fleetApi.attachDevice(identity.id)
await notifyTech(techEmail, fleet.slug)
```

blame says it was added in one commit, message is `fix enrollment flakiness`, no ticket, no test,
author left two years ago. nothing in the repo references it and there's no comment beyond what you
see.

enrollment drops about 4% between register and device-ready, and 1.2s of dead
time on the critical path is an obvious thing to claw back. i want to delete it and ship.

what i can tell you about the surrounding system:

- `createDeviceIdentity` writes to our certificate authority, which is a third party.
- `fleetApi.attachDevice` reads the device identity by id. it 404s if the identity isn't there yet.
- the CA's docs say identity creation is "immediately consistent" on the primary and does
  not document any replica behaviour.
- we have no integration test covering enrollment end to end. staging uses a single-region CA
  tenant; production is multi-region.
- error tracking shows 3 `DeviceAttachFailed` events in the last 90 days, all from one
  afternoon in March, all with an `identity_not_found` payload from the fleet API.

(write any notes or logs you keep into the current directory rather than your home directory)
