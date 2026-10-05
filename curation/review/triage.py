"""Print flags from finished gpt-6.1-sol review chunks next to their full entries.

Usage: triage.py FIRST LAST   chunk numbers; chunks not yet reviewed are skipped.
Each flag shows the batch file that holds the entry, for apply.py.
"""

import glob
import json
import sys
from pathlib import Path

CURATION = Path(__file__).resolve().parents[1]
FLAGS = CURATION / "review/flags-gpt-6.1-sol"

entries = {}
for f in sorted(glob.glob(str(CURATION / "done/*.jsonl"))):
    for line in open(f):
        e = json.loads(line)
        entries[e["headword"]] = (Path(f).stem, e)

first, last = int(sys.argv[1]), int(sys.argv[2])
for n in range(first, last + 1):
    path = FLAGS / f"{n:04d}.json"
    if not path.exists():
        continue
    flags = json.loads(path.read_text())["flags"]
    by_word: dict[str, list] = {}
    for x in flags:
        # A few replies use word/meaning instead of headword/sense.
        x.setdefault("headword", x.get("word"))
        x.setdefault("sense", x.get("meaning"))
        by_word.setdefault(x["headword"], []).append(x)
    print(f"\n======== chunk {n:04d}: {len(flags)} flags")
    for h, xs in by_word.items():
        if h not in entries:
            print(f"\n### {h} (NOT FOUND)")
            continue
        b, e = entries[h]
        print(f"\n### {h} (batch {b})")
        flagged = {x["sense"] for x in xs}
        for i, s in enumerate(e["senses"], 1):
            print(f"  {i}. {s['pos']} {s['tags']} {s['gloss_en']}")
            if i in flagged:
                for ex in s["examples"]:
                    print(f"       {ex['vi']} = {ex['en']}")
        for x in xs:
            print(f"  >> s{x['sense']} {x['problem']}/{x['severity']}: {x['why']} | FIX: {x['fix']}")
