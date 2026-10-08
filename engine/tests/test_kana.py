import unicodedata

from src.kana import normalize, tokenize


def test_one_character_per_cell():
    assert tokenize("きょう") == ["き", "ょ", "う"]
    assert len(tokenize("みず")) == 2


def test_normalize_composes_dakuten():
    # が must be one cell, not か + combining mark
    decomposed = unicodedata.normalize("NFD", "が")
    assert len(decomposed) == 2
    assert normalize(decomposed) == "が"
    assert len(tokenize(normalize(decomposed))) == 1