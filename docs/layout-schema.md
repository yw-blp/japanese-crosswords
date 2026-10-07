# Puzzle Layout Schema

The current schema version is the value of the `version` field below. Bump it
whenever the shape of the JSON changes.

## Conventions
- Coordinates are 0-indexed. `row` increases downward, `col` increases rightward
- (0, 0) is the top-left of the puzzle's bounding box
- One Unicode character = one cell. All strings are NFC-normalized
- A cell is *filled* if at least one word covers it; otherwise it is blank
- An `across` word occupies (row, col) … (row, col+length-1)
- A `down` word occupies (row, col) … (row+length-1, col)
- A *run* is a maximal sequence of 2+ horizontally (or vertically) adjacent
  filled cells
- Two words are *linked* if they share a cell
- `answer` contains only hiragana, including small kana (`ぁぃぅぇぉっゃゅょゎ`):
  U+3041 to U+3096. The long vowel mark `ー` (U+30FC) is not allowed.

## Top-level object
| Field     | Type    | Description                                  |
|-----------|---------|----------------------------------------------|
| version   | integer | Schema version                               |
| date      | string  | ISO date (YYYY-MM-DD) the puzzle is for      |
| seed      | integer | Seed used to generate it                     |
| width     | integer | Bounding box width in cells                  |
| height    | integer | Bounding box height in cells                 |
| words     | array   | Placed words (see below), sorted by id       |

## Word object
| Field     | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| id        | integer | Unique identifier for word within puzzle         |
| direction | string  | "across" or "down"                               |
| row, col  | integer | Position of the first cell                       |
| length    | integer | Number of cells (= characters in `answer`)       |
| answer    | string  | The hiragana word                                |
| clue      | string  | English meaning                                  |

## Identifiers
Each word has an `id`. Ids are positive integers, unique within the puzzle, 
so id alone identifies a word. Ids are opaque: consumers MUST NOT infer meaning 
from them or display them.

## Guarantees (the engine promises these)
- words are sorted by id in ascending order
- Every word has length >= 3, and length is the number of characters in `answer`
- Intersecting words have a shared character at the intersecting cell
- No two words have the same `answer`
- The puzzle is a single connected group: any two words are joined by a chain of linked words
- Every run is exactly one listed word, with the same start and
  length. No listed word is part of a longer run.
- Every cell belongs to at most one across word and at most one down word
- Every word lies within the bounding box
- The first and last rows and columns each contain at least one filled cell
- Every character in every `answer` is in the allowed set (see Conventions)

## Example

```json
{
  "version": 1,
  "date": "2026-10-07",
  "seed": 20261007,
  "width": 2,
  "height": 2,
  "words": [
    {"id": 1, "direction": "across", "row": 0, "col": 0, "length": 2, "answer": "みず", "clue": "water"},
    {"id": 2, "direction": "down",   "row": 0, "col": 0, "length": 2, "answer": "みせ", "clue": "store"}
  ]
}
```