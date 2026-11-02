# Orders service

Every amount — in this code, in the live orders database (about 4 million rows) and in the
reporting jobs another team runs against that database — is a float number of dollars. Floats
round, so totals can drift by a cent. Moving to integer cents means migrating the live database
and the other team's reports together, with a rollout plan both teams agree; nobody has scheduled
that yet.
