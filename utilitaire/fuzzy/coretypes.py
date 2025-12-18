from dataclasses import dataclass
from typing import Any, Iterable

type QueryEntries = Iterable[tuple[str, list[Any | None]]]
type Haystacks = Iterable[tuple[str, list[str]]]


@dataclass
class SearchResult:
    """Search result with score."""

    haystack_id: str
    score: float

    def __lt__(self, other):
        """For heap comparisons (min-heap, so we negate)."""
        return self.score < other.score

    def __hash__(self):
        return hash(self.haystack_id)

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, SearchResult):
            return value.haystack_id == self.haystack_id

        return False
