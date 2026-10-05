"""Same review as review.py, run through the Codex CLI on the ChatGPT subscription.

Usage: review_codex.py MODEL EFFORT FIRST LAST [WORKERS=5]
Flags land in flags-<MODEL>/CHUNK.json. Codex runs read-only in an empty folder.
"""

import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
SYSTEM = (HERE / "prompt.txt").read_text()
CHUNK = 40


def entries() -> list[dict]:
    out = []
    for path in sorted((HERE.parent / "done").glob("*.jsonl")):
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


def review(model: str, effort: str, out_dir: Path, n: int, chunk: list[dict]) -> str:
    out = out_dir / f"{n:04d}.json"
    if out.exists():
        return f"{n:04d} skipped (done)"
    prompt = SYSTEM + "\n\nThe entries to review:\n\n" + "\n\n".join(render(e) for e in chunk)
    with tempfile.TemporaryDirectory() as work:
        last = Path(work) / "answer.txt"
        result = subprocess.run(
            ["codex", "exec", "-m", model, "-c", f'model_reasoning_effort="{effort}"',
             "-s", "read-only", "--ephemeral", "--skip-git-repo-check", "-C", work,
             "-o", str(last), "-"],
            input=prompt, capture_output=True, text=True, timeout=1800, env=os.environ,
        )
        if result.returncode or not last.exists():
            return f"{n:04d} FAILED: {result.stderr[-300:]}"
        content = last.read_text()
    try:
        flags = json.loads(content[content.index("{") : content.rindex("}") + 1])["flags"]
    except (ValueError, KeyError) as error:
        return f"{n:04d} FAILED to parse: {error!r}"
    out.write_text(json.dumps({"headwords": [e["headword"] for e in chunk], "flags": flags},
                              ensure_ascii=False, indent=1))
    return f"{n:04d} {len(flags)} flags"


def main() -> None:
    model, effort, first, last = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 5
    out_dir = HERE / f"flags-{model}"
    out_dir.mkdir(exist_ok=True)
    all_entries = entries()
    chunks = [all_entries[i : i + CHUNK] for i in range(0, len(all_entries), CHUNK)]
    with ThreadPoolExecutor(workers) as pool:
        jobs = [pool.submit(review, model, effort, out_dir, n, chunks[n - 1])
                for n in range(first, last + 1)]
        for job in jobs:
            print(job.result(), flush=True)


main()
