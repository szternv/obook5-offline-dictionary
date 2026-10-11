#!/usr/bin/env python3
import argparse, sqlite3, html
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument("output")
ap.add_argument("sources", nargs="+", help="LABEL=file.dict")
args=ap.parse_args()

merged={}
for spec in args.sources:
    label,fn=spec.split("=",1)
    con=sqlite3.connect(fn)
    for w,c in con.execute("SELECT word,content FROM dict"):
        part=f"<b>{html.escape(label)}</b><br>{c}"
        merged[w]=merged[w]+"<br><br>"+part if w in merged else part
    con.close()

out=Path(args.output)
if out.exists(): out.unlink()
con=sqlite3.connect(out)
con.execute("CREATE TABLE dict (word varchar (128) primary key, content varchar(255))")
con.executemany("INSERT INTO dict(word,content) VALUES (?,?)",
                sorted(merged.items(), key=lambda x:x[0].casefold()))
con.commit(); con.execute("VACUUM"); con.commit(); con.close()
print("Created:",out,"entries:",len(merged))
