"""Kana rules shared by the whole engine.

Single source of truth for what counts as a valid answer.
See docs/layout-schema.md (Conventions and Guarantees).
"""

import unicodedata

# docs/layout-schema.md: hiragana U+3041..U+3096, including small kana.
HIRAGANA_FIRST = 0x3041
HIRAGANA_LAST = 0x3096
LONG_VOWEL_MARK = "ー"  # U+30FC, explicitly not allowed
MIN_LENGTH = 2


def normalize(text: str) -> str:
    """All text in the engine is NFC."""
    return unicodedata.normalize("NFC", text)


def tokenize(word: str) -> list[str]:
    """One Unicode character = one cell."""
    return list(word)


def is_answer_char(ch: str) -> bool:
    return len(ch) == 1 and HIRAGANA_FIRST <= ord(ch) <= HIRAGANA_LAST


def answer_problem(word: str) -> str | None:
    """Return the first reason `word` can't be an answer, or None if it can.

    Validates; never repairs. Callers normalize first.
    The long-vowel check is redundant with the range check, but it gives
    katakana loanwords with ー their own bucket in clean_vocab's report.
    """
    if not unicodedata.is_normalized("NFC", word):
        return "not_nfc"
    if LONG_VOWEL_MARK in word:
        return "long_vowel_mark"
    if not all(is_answer_char(ch) for ch in word):
        return "non_hiragana"
    if len(word) < MIN_LENGTH:
        return "too_short"
    return None


def is_valid_answer(word: str) -> bool:
    return answer_problem(word) is None