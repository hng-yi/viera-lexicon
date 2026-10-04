# viera-lexicon

Pinned dictionary sources for Viera, published as release assets so they can be downloaded
without credentials. Each file is used unchanged: Viera's importer checks it against the
sha256 pinned in its own lockfile.

Two kinds of file:

- the Wiktionary extract below, as downloaded;
- Viera's curation of it (`curation-*.jsonl.gz`), made from the `curation/` folder.

## kaikki-vi-2026-09-17.jsonl.gz

The Vietnamese entries of the English Wiktionary, as extracted by
[wiktextract](https://github.com/tatuylonen/wiktextract) and published at
<https://kaikki.org/dictionary/Vietnamese/>, downloaded on 2026-09-17 (kaikki does not
version its extracts).

- Release: `lexicon-2026-09-17`
- sha256: `745bf37ac97082a4710c536d0d493d5b33f912e1f703c22596a8756613bf00f3`

## Curation

Each Wiktionary entry is reviewed so a learner can rely on it: glosses rewritten in plain
English, senses ordered most common first, duplicates merged, a fixed set of tags, common
meanings Wiktionary lacks added, and one or two short example sentences per sense. Kept
Wiktionary examples are quoted word for word; others are written by the reviewer and marked
`generated`. The rules are in [`curation/GUIDE.md`](curation/GUIDE.md).

- `curation/order.txt`: headwords in review order, most frequent in a sample of Vietnamese
  subtitles first (OpenSubtitles 2018, segmented with underthesea), then the rest A-Z.
- `curation/todo/NNNN.json`: a batch of Wiktionary entries as Viera parses them.
- `curation/done/NNNN.jsonl`: the reviewed entries.

Entries are reviewed by Claude (Anthropic) following the guide, and checked by Viera's
`back-end/scripts/curate_lexicon.py`. A release file holds every reviewed entry so far.

## License

Wiktionary text added before 1 June 2023 is available under the
[Creative Commons Attribution-ShareAlike 3.0 Unported license (CC BY-SA 3.0)](https://creativecommons.org/licenses/by-sa/3.0/),
text added since under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: <https://en.wiktionary.org/>, extracted by wiktextract and published by kaikki.org.

The curation is an adaptation of that text and is released under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
