# Crossword Engine

Daily randomized Hiragana crossword generator using Genki vocabulary.

## Setup
cd engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

## Decisions
- One Unicode character = one cell (きょう = 3 cells).
- All text normalized to NFC.