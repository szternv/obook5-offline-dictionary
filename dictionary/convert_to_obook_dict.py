#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, json, sqlite3, sys

def norm(v):
    if v is None:
        return ""
    return str(v).replace("\r\n","\n").replace("\r","\n").strip()

def csv_rows(path, delim, wf, cf):
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=delim):
            yield norm(r.get(wf)), norm(r.get(cf))

def json_rows(path, wf, cf):
    obj = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(obj, dict) and "entries" not in obj:
        for k,v in obj.items():
            yield norm(k), norm(v)
        return
    if isinstance(obj, dict):
        obj = obj["entries"]
    for r in obj:
        yield norm(r.get(wf)), norm(r.get(cf))

def jsonl_rows(path, wf, cf):
    with open(path, "r", encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            line=line.strip()
            if not line: continue
            try: r=json.loads(line)
            except Exception as e:
                print(f"Skipping line {n}: {e}", file=sys.stderr); continue
            yield norm(r.get(wf)), norm(r.get(cf))

ap=argparse.ArgumentParser()
ap.add_argument("input")
ap.add_argument("output")
ap.add_argument("--word-field", default="word")
ap.add_argument("--content-field", default="content")
ap.add_argument("--delimiter", default=",")
ap.add_argument("--lowercase-aliases", action="store_true")
args=ap.parse_args()

src=Path(args.input); out=Path(args.output)
ext=src.suffix.lower()
if ext==".csv":
    rows=csv_rows(src,args.delimiter,args.word_field,args.content_field)
elif ext==".tsv":
    rows=csv_rows(src,"\t",args.word_field,args.content_field)
elif ext==".json":
    rows=json_rows(src,args.word_field,args.content_field)
elif ext in {".jsonl",".ndjson"}:
    rows=jsonl_rows(src,args.word_field,args.content_field)
else:
    raise SystemExit("Supported: .csv .tsv .json .jsonl .ndjson")

entries={}
for w,c in rows:
    if not w or not c or len(w)>128: continue
    entries[w]=c.replace("\n","<br>")
    if args.lowercase_aliases and w.lower()!=w:
        entries.setdefault(w.lower(), entries[w])

if not entries: raise SystemExit("No valid entries.")

if out.exists(): out.unlink()
con=sqlite3.connect(out)
con.execute("PRAGMA journal_mode=OFF")
con.execute("PRAGMA synchronous=OFF")
con.execute("CREATE TABLE dict (word varchar (128) primary key, content varchar(255))")
con.executemany("INSERT OR REPLACE INTO dict(word,content) VALUES (?,?)",
                sorted(entries.items(), key=lambda x:x[0].casefold()))
con.commit(); con.execute("VACUUM"); con.commit(); con.close()

print("Created:", out)
print("Entries:", len(entries))
print("Size MB:", round(out.stat().st_size/1024/1024,2))
