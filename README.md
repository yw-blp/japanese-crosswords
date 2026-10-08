# Crossword Engine

Daily randomized Hiragana crossword generator using JLPT N5-N3 vocabulary.

## Setup
```
cd engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Decisions
- One Unicode character = one cell (きょう = 3 cells).
- All text normalized to NFC.
- Vocabulary comes from the JLPT N5, N4 and N3 lists. The answer is the hiragana
  reading and the clue is the English definition.

## Data
Raw lists live in `engine/data/raw/` (`n5.csv`, `n4.csv`, `n3.csv`), taken from
[yomitan-jlpt-vocab](https://github.com/stephenmk/yomitan-jlpt-vocab) at commit
`b062d4e38c4bdd0950ae1d4ec55f04b176182e03`. The cleaned list used by the engine
is `engine/data/vocab.json`, produced by `engine/scripts/clean_vocab.py`.

## Licenses
- **Code:** MIT (see [LICENSE.txt](LICENSE.txt)).
- **Vocabulary data** in `engine/data/` and puzzles generated from it:
  CC BY-SA 4.0 (see [DATA_LICENSE.md](DATA_LICENSE.md)). The MIT license does
  not cover this data.

## Credits
- JLPT vocabulary lists by [Jonathan Waller](https://www.tanos.co.uk/jlpt/),
  licensed under Creative Commons Attribution (CC BY). His
  [sharing page](https://www.tanos.co.uk/jlpt/sharing/) states the license as
  Creative Commons "BY" without a version number
  ([archived copy](https://web.archive.org/web/20260927074436/https://www.tanos.co.uk/jlpt/sharing/)).
  See the [CC BY deed](https://creativecommons.org/licenses/by/4.0/).
- [yomitan-jlpt-vocab](https://github.com/stephenmk/yomitan-jlpt-vocab) by
  Stephen Kraus (CC BY-SA 4.0).
- [JMdict](https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project),
  © Electronic Dictionary Research and Development Group (CC BY-SA 4.0).
  See the [EDRDG licence](https://www.edrdg.org/edrdg/licence.html).
