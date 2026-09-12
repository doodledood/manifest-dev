---
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write]
model: opus
runs: 3
---
use the just-figure-out skill for this.

lets think this through before we do anything.

the app has a tab row at the top with five destinations: Analyze, Study, Drills, Leaks, Stats. the stats pages are public, no auth guard, and theyre where basically all our search traffic lands - everything else in that row is signed-in product.

stat pages i think need to go from the tab there - what do you think? they are kind of not a part of the app they are there for seo; i thoguht mabye to just link at the footer ot them isntead.

and also the bar there is completely messed up and not aligning with the rest of the app

(write any notes or logs you keep into the current directory rather than your home directory)
