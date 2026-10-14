#!/usr/bin/env bash
# A folder that is not a project: two bank exports downloaded for one task, no repository, no context file.
set -euo pipefail
cat > checking-export.csv <<'CSV'
date,description,amount
2026-09-03,Corner Bean Cafe,-4.50
2026-09-01,Salary,2400.00
CSV
cat > savings-export.csv <<'CSV'
Date;Details;Amount
02/09/2026;Transfer in;150,00
05/09/2026;Interest;1,20
CSV
