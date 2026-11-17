"""Vocabulary loading and the letter index the generator searches with."""

import json
from dataclasses import dataclass
from pathlib import Path

from src.kana import invalid_reason

LEVELS = ("n5", "n4", "n3")


@dataclass(frozen=True, slots=True)
class Entry:
    answer: str
    clue: str
    level: str


def load_vocab(path: Path | str) -> list[Entry]:
    """Read and strictly validate vocab.json (a list of answer/clue/level)."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"{path} is empty; run `python -m scripts.clean_vocab`")
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a JSON array")

    entries: list[Entry] = []
    seen: set[str] = set()
    for i, item in enumerate(data):
        where = f"{path}[{i}]"
        if not isinstance(item, dict) or set(item) != {"answer", "clue", "level"}:
            raise ValueError(f"{where}: expected keys answer, clue, level")
        answer, clue, level = item["answer"], item["clue"], item["level"]
        if not all(isinstance(v, str) for v in (answer, clue, level)):
            raise ValueError(f"{where}: values must be strings")
        if reason := invalid_reason(answer) is not None:
            raise ValueError(f"{where}: bad answer {answer!r} ({reason})")
        if not clue.strip():
            raise ValueError(f"{where}: empty clue")
        if level not in LEVELS:
            raise ValueError(f"{where}: unknown level {level!r}")
        if answer in seen:
            raise ValueError(f"{where}: duplicate answer {answer!r}")
        seen.add(answer)
        entries.append(Entry(answer, clue, level))
    return entries


class VocabIndex:
    """Entries plus lookups the generator needs.

    `char_location[char]` lists every (entry_index, char_index) where `char` occurs, so
    "which words can cross this cell?" is one dictionary lookup. Everything is
    built in entry order, so iteration order is deterministic.
    """

    def __init__(self, entries: list[Entry]) -> None:
        self.entries: tuple[Entry, ...] = tuple(entries)
        char_location: dict[str, list[tuple[int, int]]] = {}
        for entry_index, entry in enumerate(self.entries):
            for char_index, char in enumerate(entry.answer):
                char_location.setdefault(char, []).append((entry_index, char_index))
        self.char_location = {char: tuple(locations) for char, locations in char_location.items()}
        # Two words with the same clue ("blue" for あお and あおい) would be
        # indistinguishable to the player, so the generator avoids pairing them.
        self.clue_keys: tuple[str, ...] = tuple(
            " ".join(entry.clue.casefold().split()) for entry in self.entries
        )

    def __len__(self) -> int:
        return len(self.entries)

    def entry_indices_with_length(self, low: int, high: int) -> list[int]:
        return [entry_index
                for entry_index, entry in enumerate(self.entries)
                if low <= len(entry.answer) <= high
        ]
