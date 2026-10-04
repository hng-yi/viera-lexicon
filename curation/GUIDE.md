# Curating the Viera dictionary

Viera's dictionary is the Vietnamese section of the English Wiktionary. This guide is how each
entry is reviewed so that an English-speaking learner, from beginner to upper intermediate,
can rely on it. The reviewed entries replace the Wiktionary ones when Viera imports them.

Who reads it: a learner looks a word up, picks the meaning they met, and banks it. The gloss
becomes the back of a flashcard. The example shows the word in use. So a gloss must say what
the word means in plain English, in a few words, and the example must show that meaning in a
sentence a learner could hear or say.

## What you get and what you write

A batch file `todo/NNNN.json` holds Wiktionary entries as Viera parsed them:

```json
{"headword": "hay", "base": "1c0f…",
 "senses": [{"position": 1, "pos": "verb", "tags": [], "gloss": "to know; to get to know; to learn"}, …],
 "examples": [{"sense": 4, "vi": "Phim hay quá ha !", "en": "That was a great movie!"}, …]}
```

Write `done/NNNN.jsonl`: one line per entry of the batch, every entry, in the same order:

```json
{"headword": "hay", "base": "1c0f…",
 "senses": [
  {"from": [4], "pos": "adj", "tags": [], "gloss_en": "good; interesting; entertaining",
   "examples": [{"vi": "Phim này hay quá!", "en": "This film is really good!", "source": "generated"}]},
  {"from": [6], "pos": "adv", "tags": [], "gloss_en": "often; usually",
   "examples": [{"vi": "Con hay nói nhiều lắm.", "en": "You talk a lot, child.", "source": "wiktionary"}]}
 ],
 "dropped": [{"position": 9, "reason": "a Sino-Vietnamese reading, not a meaning"}],
 "notes": "optional: anything a human should look at"}
```

- `headword` and `base`: copied unchanged.
- `senses`: the reviewed meanings, **most common first** (see Order).
- `from`: the Wiktionary positions this sense rewrites. Usually one; several when you merge
  duplicates; empty for a meaning you add (below). Every Wiktionary position appears exactly
  once, in some `from` or in `dropped`.
- `pos`: one of noun, verb, adj, adv, num, pron, classifier, particle, conj, prep, intj,
  phrase, proverb, idiom, det, prefix, suffix, adnominal, postp. Keep Wiktionary's unless it
  is wrong.
- `tags`: only from the list under Tags.
- `examples`: one or two per sense. `source` is `wiktionary` for an example copied from the
  batch (its `vi` character for character) or `generated` for one you wrote.
- `dropped`: Wiktionary senses that are not meanings, each with a short reason.
- `notes`: optional. Use it to flag a sense you could not verify, or anything else a human
  should check.

**Adding a meaning Wiktionary lacks.** When a word has a common meaning that a learner will
meet in everyday Vietnamese and Wiktionary does not list it (`làm` "to make, to cause"; `chúa`
"God"; `đồng` "coin"), add it as a sense with `"from": []` and `"added": "<key>"`, a short
lowercase key in English words joined by hyphens (`make-cause`, `god`, `coin`). Place it in
frequency order like any other sense, give it a gloss, tags and a written example. Add only
meanings you are sure of and that are common; never add rare, archaic or technical ones, and
never add a meaning that only exists inside a compound (that belongs to the compound's own
entry). List the keys you added in `notes` so a human can find them.

Check your file with `uv run python scripts/curate_lexicon.py check NNNN` from Viera's
`back-end/` and fix every error. Read every warning and fix it unless you have a reason.

## Glosses

Write what the word means, the way a good learner's dictionary would.

- Plain, current English. Two to four close equivalents separated by `; ` when one word is not
  enough: `to know; to realise`. Not a list of every near-synonym.
- Verbs start with `to`. Nouns without an article unless it is needed (`a saw` is fine, but
  prefer `saw (tool)`). Adjectives as adjectives. No full stop at the end.
- Lowercase unless the word itself is capitalised in English (`Italian`, `Christmas`).
- A short parenthesis may say what the gloss alone cannot: the object of a verb, the domain,
  or how the word differs from a near-synonym. `to roast (in a dry pan)`. Keep it short.
- Function words (particles, pronouns, classifiers, conjunctions) get a gloss that says what
  the word does: `final particle softening a request`; `classifier for animals and some
  objects`; `I, me (friendly, between equals)`.
- Pronouns and kinship terms: give the relationship and when it is used, e.g. `older brother;
  you (to an older man, or a husband)`.
- No Chinese characters, ever. No Vietnamese in the gloss except where it is the clearest way
  to point at a related word, and then with its meaning: `compare tốt (good, of quality)`.
- Keep the meaning Wiktionary gives. You are correcting wording, not inventing meanings. If a
  Wiktionary gloss is garbled, rewrite it from what the gloss, its tags and its examples show.
  If you are not sure what it means, keep its wording close and say so in `notes`.
- "synonym of X (“…”)" and "alternative form of X" senses: write the meaning itself, and
  mention X only if the difference matters (`colloquial form of …`).

## Order

Put the meaning a learner is most likely to meet first, then the others in order of how often
they are used today. Wiktionary lists meanings in editing order, not by frequency: `hay` lists
"to know" (literary) before "good", "often" and "or", which are what everyone says.

## Merging and dropping

- Merge two senses only when they are the same meaning with the same part of speech, worded
  differently. Different meanings stay separate even when close.
- Pronoun and address senses that differ only in who is speaking to whom are one meaning:
  merge them and say who uses it in the gloss (`you (to an aunt, an older woman or a teacher)`).
  Keep `I` and `you` apart.
- The same thing named in different settings is one meaning: the chariot in Chinese chess and
  the rook in chess; a district-level unit in Japan, France and the US.
- Two senses with the same meaning but different parts of speech stay apart, unless one of
  the parts of speech is plainly wrong; then fix it and merge.
- Drop a sense only when it is not a meaning: a Sino-Vietnamese reading ("Sino-Vietnamese
  reading of 矮"), a bare cross-reference with nothing to say, or a parsing accident. Rare,
  archaic, regional and offensive meanings are meanings: keep them and tag them.
- A sense you cannot verify is not dropped either: keep Wiktionary's meaning in its words,
  tag it `rare`, write a short plain example, and say in `notes` that it is unverified.

## Tags

Use only these, and only when they help: a common meaning needs no tag.

- How current it is: `uncommon`, `rare`, `dated`, `archaic`, `historical`
- Register: `colloquial`, `informal`, `slang`, `Internet`, `formal`, `literary`, `polite`,
  `honorific`, `humble`, `endearing`, `childish`, `humorous`, `euphemistic`, `derogatory`,
  `offensive`, `vulgar`
- Region: `Northern`, `Central`, `Southern`
- Use: `figurative`, `idiomatic`, `in-compounds` (only used inside compounds)

Wiktionary's tags are a hint, not an answer. Its fragments ("usually", "especially", "also")
are never tags. When the register depends on the region ("formal outside the North"), tag
what holds for most speakers and say the rest in a short parenthesis in the gloss. Irony and
mock-formality go under `humorous`.

Mapping Wiktionary's other tags: `obsolete` → `archaic`; `impolite`, `familiar` →
`informal` (or `colloquial`), with "(rude)" in the gloss when it is rude; `dialectal` → the
region if you know it, else none and a word in the gloss; `poetic` → `literary`;
`morpheme` → `in-compounds`. Grammar and scope labels (`transitive`, `intransitive`,
`collective`, `Chinese`, `attributive`) are not tags: say it in the gloss if it matters.

Kinship terms used for a wider family (a senior cousin, an uncle by marriage) stay separate
from the core meaning, as they do in `anh`.

## Examples

Every sense gets at least one example; one good one is better than two average ones.

**Keeping a Wiktionary example.** Keep it when it is short, modern, natural, clearly shows
this sense, and its English is right. Copy `vi` exactly; you may fix or supply `en`. Do not
keep long literary quotations, verse, old texts, or anything a learner would find obscure,
unless the sense itself is literary or archaic and the quotation is short.

**Writing an example.**

- A natural sentence a native speaker would say or write today. Standard, neutral Vietnamese
  unless the sense is regional (then that region's speech) or has a register (then match it).
- Short: usually 5 to 12 words. Go a little longer when the meaning needs context to come
  through, up to about 15. Never longer than 20 (the checker refuses it).
- It must use the headword in this exact sense, written exactly as the headword (the checker
  looks for it). Choose a sentence where only this meaning makes sense.
- Use simpler words than the headword around it where you can, so a learner can follow.
- Everyday subjects: family, food, work, school, travel, weather, feelings, town life. Vary
  them across an entry. No real people, no politics, nothing violent or sexual unless the
  word is about that, and then plainly.
- Classifiers: with typical nouns (`hai con mèo`). Particles: in the kind of sentence they
  end or soften. Pronouns: in a sentence that shows who is speaking to whom.
- Proverbs and idioms: a sentence in which someone uses it, or the saying in a short context.
- Archaic and literary senses: a short sentence in the style where it is still met (a set
  phrase, a formal register), not a made-up old text. When no living use survives, write a
  short plain sentence in which the old meaning is clear, keep the tag, and say in `notes`
  that the example is constructed.
- A word that names a real person or office by definition may have an example about them:
  plain and factual.
- When a sense cannot be verified and its only Wiktionary example is long, you may keep that
  example rather than invent one; say so in `notes`.
- `en`: a natural English translation, not word for word. Translate the headword with the
  gloss's meaning so the reader can see the connection.

## Before you finish

Read each entry again as a learner would, sense by sense:

1. Does the first sense match what the word most often means today?
2. Is every gloss plain English that would make sense on a flashcard?
3. Does every example use the headword, in this sense and no other, in natural Vietnamese?
   Would a native speaker say it? If you hesitate, write a different one.
4. Does each English translation match its Vietnamese?
5. Is every Wiktionary position in exactly one `from` or `dropped`?

Then run the checker until it reports `ok`.
