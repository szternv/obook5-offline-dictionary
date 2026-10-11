#!/usr/bin/env python3
import argparse, sqlite3
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument("dictfile")
ap.add_argument("--word")
args=ap.parse_args()

con=sqlite3.connect(Path(args.dictfile))
print("Schema:")
for r in con.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='dict'"):
    print(r[0])
print("Entries:", con.execute("SELECT COUNT(*) FROM dict").fetchone()[0])
if args.word:
    print(con.execute("SELECT word,content FROM dict WHERE word=?", (args.word,)).fetchone())
else:
    for w,c in con.execute("SELECT word,content FROM dict ORDER BY word LIMIT 10"):
        print(w, "->", c[:140])
con.close()
