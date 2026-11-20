#!/usr/bin/env bash
# Build the test database and run the tests.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build
rm -f build/stock.db
sqlite3 build/stock.db < schema.sql
STOCK_DB=build/stock.db python3 -m unittest -q
