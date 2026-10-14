use the define skill for this. the project is this repo.

add renewals: `shelfnote renew --book X` extends a loan by another loan period and records the renewal on the loan in data/loans.json (when it happened), and `shelfnote overdue` uses the renewed due date. a loan can be renewed at most twice. scope is settled. the tool is installed on three club laptops that share the same loans.json through a synced folder, and they won't all update the same day. i'm afk, dont ask me anything. write the spec to ./manifest.md in the current directory, not your home directory.
