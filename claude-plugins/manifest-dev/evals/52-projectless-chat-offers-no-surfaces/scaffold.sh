#!/usr/bin/env bash
# A folder that is not a project: holiday photos and a note, no repository, no context file.
set -euo pipefail
for name in IMG_0412 IMG_0413 IMG_0420 DSC_7781; do
  printf 'placeholder image\n' > "$name.jpg"
done
cat > note.txt <<'TXT'
lisbon trip, may. want these sorted by when they were taken.
TXT
