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
    """Ensures all text in the engine is NFC."""
    return unicodedata.normalize("NFC", text)


def tokenize(word: str) -> list[str]:
    """Converts 'word' to a list of characters."""
    return list(word)


def is_valid_char(char: str) -> bool:
    """Checks if charcter is valid in the first place."""
    return len(char) == 1 and HIRAGANA_FIRST <= ord(char) <= HIRAGANA_LAST


def invalid_reason(word: str) -> str | None:
    """Return the first reason `word` can't be an answer, or None if it can.

    Validates; never repairs. Callers normalize first.
    The long-vowel check is redundant with the range check, but it gives
    katakana loanwords with 'ー' their own bucket in clean_vocab's report.
    """
    if not unicodedata.is_normalized("NFC", word):
        return "not_nfc"
    if LONG_VOWEL_MARK in word:
        return "long_vowel_mark"
    if not all(is_valid_char(char) for char in word):
        return "non_hiragana"
    if len(word) < MIN_LENGTH:
        return "too_short"
    return None


def is_valid_answer(word: str) -> bool:
    return invalid_reason(word) is None
