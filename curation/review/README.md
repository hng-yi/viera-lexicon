# Second-model review

After the curation run, a second model read every curated entry and flagged
likely mistakes. Claude then triaged each flag by hand and applied the accepted
ones to `../done/`. The model only flags; it never edits.

## Files

- `prompt.txt`: the review prompt (checks: wrong_meaning, missing_meaning,
  bad_example, bad_translation, order, and tags limited to missing_warning,
  region, currency and register).
- `review_codex.py MODEL EFFORT FIRST LAST [WORKERS]`: runs the review through
  the Codex CLI, 40 entries per chunk, writing `flags-MODEL/NNNN.json`. Chunks
  that already have a file are skipped, so a run can be resumed.
- `review.py`: the same review through OpenRouter (pilot only; reads the key
  from `~/.config/openrouter/key`).
- `flags/`: pilot flags from Qwen3.7-Plus (chunks 1-5).
- `flags-gpt-6.1-sol/`: the full run, gpt-6.1-sol at medium effort, chunks 1-650.
  A few replies use `word`/`meaning` instead of `headword`/`sense`.
- `full-run.log`: the full run's log.
- `triage.py FIRST LAST`: prints each chunk's flags next to the full entry.
- `apply.py EDITS.jsonl...`: applies edit ops (gloss, tags, pos, ex, add, drop,
  move) to the done files; see its docstring.
- `edits/`: every edit list that was applied, in order (`e00` to `e49`; a `b`
  suffix is a follow-up fix to the file of the same number).

## Outcome (2026-10-05)

About 2,750 flags; about 2,730 edits applied: 965 example rewrites, 681 tag
fixes, 485 corrected glosses, 308 added senses, 246 dropped senses, and 48
reorders or part-of-speech changes. Released as `curation-2026-10-05a` through
`curation-2026-10-05o`.

Flags that mostly held up: wrong or missing meanings, regional tags, and
missing derogatory or vulgar warnings. Flags that were mostly rejected: adding
"formal" or "literary" to ordinary words, and reordering senses.
