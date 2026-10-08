"""Pins src.kana's answer rules to docs/layout-schema.md.

The constants below are copied from the schema on purpose and must NOT be
imported from src: if the code and the doc disagree, this test should fail.
Changing the schema's allowed set means changing it here in the same commit.
"""

import unicodedata

import pytest

from src.kana import answer_problem, is_answer_char, is_valid_answer, normalize

SPEC_FIRST = 0x3041
SPEC_LAST = 0x3096
SPEC_SMALL_KANA = "ぁぃぅぇぉっゃゅょゎ"


def test_allowed_set_matches_schema_exactly():
    # Sweep the hiragana and katakana blocks plus their punctuation neighbours.
    mismatches = [
        f"U+{cp:04X}"
        for cp in range(0x3000, 0x3100)
        if is_answer_char(chr(cp)) != (SPEC_FIRST <= cp <= SPEC_LAST)
    ]
    assert not mismatches


@pytest.mark.parametrize("ch", list(SPEC_SMALL_KANA))
def test_small_kana_allowed(ch):
    assert is_answer_char(ch)


@pytest.mark.parametrize(
    "ch", ["ー", "\u3099", "\u309b", "ゝ", "ア", "水", "a", "〜", "・"]
)
def test_excluded_characters(ch):
    assert not is_answer_char(ch)


@pytest.mark.parametrize(
    ("word", "reason"),
    [
        ("きょう", None),
        ("みず", None),
        ("コーヒー", "long_vowel_mark"),
        ("テレビ", "non_hiragana"),
        ("あの〜", "non_hiragana"),
        ("め", "too_short"),
        ("", "too_short"),
        (unicodedata.normalize("NFD", "がっこう"), "not_nfc"),
    ],
)
def test_answer_problem(word, reason):
    assert answer_problem(word) == reason


def test_normalize_then_validate():
    decomposed = unicodedata.normalize("NFD", "がっこう")
    assert answer_problem(decomposed) == "not_nfc"
    assert is_valid_answer(normalize(decomposed))