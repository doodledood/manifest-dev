"""Stock report. Reads the stock database named by STOCK_DB."""
import os
import sqlite3
import sys


def connect():
    return sqlite3.connect(os.environ["STOCK_DB"])


def all_items(conn):
    return conn.execute("SELECT name, qty FROM stock ORDER BY name").fetchall()


def main(argv):
    conn = connect()
    if argv[1:2] == ["all"]:
        for name, qty in all_items(conn):
            print(f"{name}: {qty}")
        return 0
    print("usage: report.py all", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
