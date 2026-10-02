import unicodedata

from src.kana import tokenize


def test_one_character_per_cell():
    assert tokenize("きょう") == ["き", "ょ", "う"]
    assert len(tokenize("みず")) == 2


def test_nfc_form_is_single_codepoint():
    # が must be one character, not か + combining mark
    decomposed = unicodedata.normalize("NFD", "が")
    assert len(decomposed) == 2
    assert len(unicodedata.normalize("NFC", decomposed)) == 1