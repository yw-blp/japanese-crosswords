"""Mutable crossword grid that only accepts entry placements the schema allows.

Coordinates are (row, col) and may be negative while a puzzle is being built;
generator.py shifts everything so the bounding box starts at (0, 0).

An entry placement is legal when, together with the words already on the grid,
it keeps every guarantee in docs/layout-schema.md that depends on geometry:

- it crosses at least one existing word (so the puzzle stays connected), and
  every shared cell holds the same character;
- it never overlaps a word running in its own direction;
- the cells just before and after it are empty (no longer run);
- every cell it adds has empty neighbours on both sides (no new, unlisted
  run beside it);
- the answer is not already on the grid;
- the bounding box stays within the size limits.
"""

from dataclasses import dataclass
from typing import NamedTuple

from src.kana import MIN_LENGTH

ACROSS = "across"
DOWN = "down"
DELTA = {ACROSS: (0, 1), DOWN: (1, 0)}

Cell = tuple[int, int]


@dataclass(frozen=True, slots=True)
class PlacedEntry:
    entry_index: int  # index into VocabIndex.entries
    answer: str
    row: int
    col: int
    direction: str

    @property
    def length(self) -> int:
        return len(self.answer)

    def occupied_cells(self) -> list[Cell]:
        dr, dc = DELTA[self.direction]
        return [(self.row + i * dr, self.col + i * dc) for i in range(self.length)]


class GridPreview(NamedTuple):
    """What the grid would look like after a legal PlacedEntry."""
    crossings: int
    height: int
    width: int


class Grid:
    def __init__(self, max_height: int, max_width: int) -> None:
        self.max_height = max_height
        self.max_width = max_width
        self._cells: dict[Cell, str] = {}
        # cell -> index of the placed entry that covers it in that direction
        self._occupied_by: dict[str, dict[Cell, int]] = {ACROSS: {}, DOWN: {}}
        # occupied_by -> outer key: direction, inner key: cell, value: index in placed_entries
        self._placed_entries: list[PlacedEntry] = []
        self._answers: set[str] = set()
        # (min_row, min_col, max_row, max_col); None while empty
        self._bounds: tuple[int, int, int, int] | None = None
        self._bounds_history: list[tuple[int, int, int, int] | None] = []

    def __len__(self) -> int:
        return len(self._placed_entries)

    @property
    def placed_entries(self) -> list[PlacedEntry]:
        return list(self._placed_entries)

    @property
    def size(self) -> tuple[int, int]:
        """(height, width) of the bounding box; (0, 0) when empty."""
        if self._bounds is None:
            return (0, 0)
        low_r, low_c, high_r, high_c = self._bounds
        return (high_r - low_r + 1, high_c - low_c + 1)

    def char_at(self, cell: Cell) -> str | None:
        return self._cells.get(cell)

    def open_cells(self) -> list[Cell]:
        """Cells covered by exactly one word: the places a new word can cross."""
        across, down = self._occupied_by[ACROSS], self._occupied_by[DOWN]
        return sorted(cell for cell in self._cells if (cell in across) != (cell in down))

    def direction_at(self, cell: Cell) -> str | None:
        """Direction of the one word covering an open cell."""
        if cell in self._occupied_by[ACROSS] and cell not in self._occupied_by[DOWN]:
            return ACROSS
        if cell in self._occupied_by[DOWN] and cell not in self._occupied_by[ACROSS]:
            return DOWN
        return None

    def _expanded_bounds(self, row: int, col: int, last_r: int, last_c: int) -> tuple[int, int, int, int]:
        if self._bounds is None:
            return (row, col, last_r, last_c)
        lo_r, lo_c, hi_r, hi_c = self._bounds
        return (min(lo_r, row), min(lo_c, col), max(hi_r, last_r), max(hi_c, last_c))

    def preview_placement(self, answer: str, row: int, col: int, direction: str) -> GridPreview | None:
        """Return the resulting crossings and dimensions of grid if the word may be placed here, else None."""
        n = len(answer)
        if n < MIN_LENGTH or answer in self._answers:
            return None
        dr, dc = DELTA[direction]
        last_r, last_c = row + (n - 1) * dr, col + (n - 1) * dc

        lo_r, lo_c, hi_r, hi_c = self._expanded_bounds(row, col, last_r, last_c)
        height, width = hi_r - lo_r + 1, hi_c - lo_c + 1
        if height > self.max_height or width > self.max_width:
            return None

        cells = self._cells
        if (row - dr, col - dc) in cells or (last_r + dr, last_c + dc) in cells:
            return None

        pr, pc = dc, dr  # step perpendicular to word direction
        same_direction = self._occupied_by[direction]
        crossings = 0
        for i, current_char in enumerate(answer):
            r, c = row + i * dr, col + i * dc
            cell_content = cells.get((r, c))
            if cell_content is None:
                if (r + pr, c + pc) in cells or (r - pr, c - pc) in cells:
                    return None
            elif cell_content != current_char or (r, c) in same_direction:
                return None
            else:
                crossings += 1
        if cells and crossings == 0:
            return None
        return GridPreview(crossings, height, width)

    def place(
        self, entry_index: int, answer: str, row: int, col: int, direction: str
    ) -> PlacedEntry:
        if self.preview_placement(answer, row, col, direction) is None:
            raise ValueError(
                f"illegal placed_entry: {answer!r} {direction} at {row},{col}"
            )
        placed_entry = PlacedEntry(entry_index, answer, row, col, direction)
        cells = placed_entry.occupied_cells()
        self._bounds_history.append(self._bounds)
        self._bounds = self._expanded_bounds(row, col, *cells[-1])
        index = len(self._placed_entries)
        for cell, char in zip(cells, answer, strict=True):
            self._cells[cell] = char
            self._occupied_by[direction][cell] = index
        self._placed_entries.append(placed_entry)
        self._answers.add(answer)
        return placed_entry

    def undo(self) -> PlacedEntry:
        """Remove the most recent placed_entry (for backtracking)."""
        placed_entry = self._placed_entries.pop()
        for cell in placed_entry.occupied_cells():
            del self._occupied_by[placed_entry.direction][cell]
            if cell not in self._occupied_by[ACROSS] and cell not in self._occupied_by[DOWN]:
                del self._cells[cell]
        self._answers.discard(placed_entry.answer)
        self._bounds = self._bounds_history.pop()
        return placed_entry