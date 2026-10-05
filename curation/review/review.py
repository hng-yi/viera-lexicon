"""Second-opinion review of the curated dictionary by another model, through OpenRouter.

The model only flags problems; nothing here edits the dictionary. Flags land in
flags/CHUNK.json (one file per request, so a run can be stopped and resumed).

Usage: review.py FIRST LAST [WORKERS=8]   reviews chunks FIRST..LAST (40 entries each,
                                          most frequent headwords first)
The key is read from ~/.config/openrouter/key and never printed.
"""

import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
DONE = HERE.parent / "done"
FLAGS = HERE / "flags"
MODEL = "qwen/qwen3.7-plus"
CHUNK = 40
SYSTEM = (HERE / "prompt.txt").read_text()
KEY = (Path.home() / ".config/openrouter/key").read_text().strip()


def entries() -> list[dict]:
    """Every curated entry with senses, in batch order (most frequent first)."""
    out = []
    for path in sorted(DONE.glob("*.jsonl")):
        for line in path.read_text().splitlines():
            e = json.loads(line)
            if e["senses"]:
                out.append(e)
    return out


def render(e: dict) -> str:
    lines = [f"## {e['headword']}"]
    for n, s in enumerate(e["senses"], start=1):
        tags = f" [{', '.join(s['tags'])}]" if s["tags"] else ""
        lines.append(f"{n}. {s['pos']}{tags} | {s['gloss_en']}")
        lines += [f"   ex: {x['vi']} = {x['en']}" for x in s["examples"]]
    return "\n".join(lines)


def ask(text: str) -> dict:
    body = {
        "model": MODEL,
        "temperature": 0.2,
        "reasoning": {"effort": "medium"},
        "response_format": {"type": "json_object"},
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}],
    }
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=600) as response:
        return json.load(response)


def review(n: int, chunk: list[dict]) -> str:
    out = FLAGS / f"{n:04d}.json"
    if out.exists():
        return f"{n:04d} skipped (done)"
    text = "\n\n".join(render(e) for e in chunk)
    for attempt in range(3):
        try:
            reply = ask(text)
            content = reply["choices"][0]["message"]["content"]
            flags = json.loads(content[content.index("{") : content.rindex("}") + 1])["flags"]
            usage = reply.get("usage", {})
            out.write_text(
                json.dumps(
                    {"headwords": [e["headword"] for e in chunk], "flags": flags, "usage": usage},
                    ensure_ascii=False,
                    indent=1,
                )
            )
            return f"{n:04d} {len(flags)} flags, cost {usage.get('cost')}"
        except Exception as error:  # retry transient API or JSON failures
            last = error
            time.sleep(5 * (attempt + 1))
    return f"{n:04d} FAILED: {last!r}"


def main() -> None:
    first, last = int(sys.argv[1]), int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    FLAGS.mkdir(exist_ok=True)
    all_entries = entries()
    chunks = [all_entries[i : i + CHUNK] for i in range(0, len(all_entries), CHUNK)]
    print(f"{len(chunks)} chunks in all; reviewing {first}..{last}")
    with ThreadPoolExecutor(workers) as pool:
        jobs = [pool.submit(review, n, chunks[n - 1]) for n in range(first, min(last, len(chunks)) + 1)]
        for job in jobs:
            print(job.result(), flush=True)


main()
