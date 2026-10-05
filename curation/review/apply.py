"""Apply review edits to curation/done files.

Usage: apply.py EDITS.json
EDITS is a list of ops; i is the 1-based sense number as shown in the review dump.
  {"b": "0001", "h": "có", "op": "gloss", "i": 10, "v": "..."}
  {"b": ..., "h": ..., "op": "tags", "i": 3, "v": ["rare"]}
  {"b": ..., "h": ..., "op": "pos", "i": 3, "v": "verb"}
  {"b": ..., "h": ..., "op": "ex", "i": 3, "v": ["vi", "en"]}        replaces examples
  {"b": ..., "h": ..., "op": "add", "i": 4, "key": "and-see", "pos": "particle",
   "tags": [], "gloss": "...", "ex": ["vi", "en"]}                      inserts as sense i
  {"b": ..., "h": ..., "op": "drop", "i": 3, "reason": "..."}
  {"b": ..., "h": ..., "op": "move", "i": 3, "to": 1}
Ops on one entry run in list order, so later sense numbers see earlier changes.
"""

import json
import sys
from pathlib import Path

DONE = Path(__file__).resolve().parents[1] / "done"


def apply(entry: dict, op: dict) -> None:
    senses = entry["senses"]
    kind, i = op["op"], op.get("i", 0) - 1
    if kind == "gloss":
        senses[i]["gloss_en"] = op["v"]
    elif kind == "tags":
        senses[i]["tags"] = op["v"]
    elif kind == "pos":
        senses[i]["pos"] = op["v"]
    elif kind == "ex":
        senses[i]["examples"] = [{"vi": op["v"][0], "en": op["v"][1], "source": "generated"}]
    elif kind == "add":
        senses.insert(i, {
            "from": [], "added": op["key"], "pos": op["pos"], "tags": op.get("tags", []),
            "gloss_en": op["gloss"],
            "examples": [{"vi": op["ex"][0], "en": op["ex"][1], "source": "generated"}],
        })
    elif kind == "drop":
        sense = senses.pop(i)
        dropped = entry.setdefault("dropped", [])
        dropped += [{"position": p, "reason": op["reason"]} for p in sense["from"]]
    elif kind == "move":
        senses.insert(op["to"] - 1, senses.pop(i))
    else:
        raise ValueError(kind)


def main() -> None:
    ops = [json.loads(l) for a in sys.argv[1:] for l in Path(a).read_text().splitlines() if l.strip()]
    by_batch: dict[str, list[dict]] = {}
    for op in ops:
        by_batch.setdefault(op["b"], []).append(op)
    for batch, batch_ops in by_batch.items():
        path = DONE / f"{batch}.jsonl"
        entries = [json.loads(line) for line in path.read_text().splitlines()]
        index = {e["headword"]: e for e in entries}
        for op in batch_ops:
            entry = index[op["h"]]
            apply(entry, op)
        path.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries))
        print(batch, len(batch_ops), "ops")


main()
