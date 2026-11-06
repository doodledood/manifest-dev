Use review-pr on four independent local PR snapshots: exception/, speculation/, missing/ and
manifest/. Each directory is its own project with its own git history and pr.json; do not
transfer one project's goals to another. For the first three use no-Manifest mode. For manifest/
use --manifest manifest.md within that project. Read the local state instead of GitHub and stop
before external actions. Save the proposed comments, thread actions and operator cycle summary
for each in controls.md at the scratch root. Do not edit application code or open snapshots/.
