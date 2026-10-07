# Crossword Engine

Daily randomized Hiragana crossword generator using JLPT word lists (N5 to N3).

## Setup
cd engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

## Decisions
- One Unicode character = one cell (きょう = 3 cells).
- All text normalized to NFC.