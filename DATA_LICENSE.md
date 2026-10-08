# Data License

The vocabulary data in `engine/data/` (including `raw/` and `vocab.json`), and
puzzle files generated from it, are licensed under
**Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.

- License deed: https://creativecommons.org/licenses/by-sa/4.0/
- Legal code: https://creativecommons.org/licenses/by-sa/4.0/legalcode

The source code in this repository is licensed separately under the MIT
license (see `LICENSE`). The MIT license does not apply to the data.

## Sources

This data is adapted from the following works:

1. **JLPT vocabulary lists** by Jonathan Waller, licensed under Creative
   Commons BY (credit required).
   https://www.tanos.co.uk/jlpt/

2. **yomitan-jlpt-vocab** by Stephen Kraus (stephenmk), licensed under
   CC BY-SA 4.0. Files `original_data/n5.csv`, `n4.csv` and `n3.csv` were taken
   from commit `b062d4e38c4bdd0950ae1d4ec55f04b176182e03` (2025-08-26).
   https://github.com/stephenmk/yomitan-jlpt-vocab

3. **JMdict**, by the Electronic Dictionary Research and Development Group
   (EDRDG), licensed under CC BY-SA 4.0. The yomitan-jlpt-vocab lists include
   JMdict entry IDs and spelling choices derived from JMdict. This
   publication has included material from the JMdict (EDICT, etc.) dictionary
   files in accordance with the licence provisions of the EDRDG.
   https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project
   Licence: https://www.edrdg.org/edrdg/licence.html

## Changes made

The data was modified from the original files. From `n5.csv`, `n4.csv` and
`n3.csv` the columns `kana` (used as the puzzle answer) and
`waller_definition` (used as the clue) were extracted. Entries were filtered to
hiragana-only answers (entries with characters outside U+3041 to U+3096,
including katakana, were removed), text was NFC-normalized, duplicate answers
were removed, and clues were shortened. See `engine/scripts/clean_vocab.py`
for the exact rules.

## Attribution requirements for apps

Any app or site built from this data must credit the sources above and link to
the licenses, on a screen reachable from a menu (for example "About" or
"Sources"), not only on a start-up screen. Copyright in the underlying
dictionary material remains with its original holders; do not claim copyright
over it.
