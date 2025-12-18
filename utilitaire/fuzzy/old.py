from typing import Sequence

from .coretypes import Haystacks, SearchResult

score_tables: dict[str, int] = {}


def score_letter(letter: str) -> int:
    if letter in score_tables:
        return score_tables[letter]

    if letter.isspace():
        return 1

    if letter.isalnum():
        score_tables[letter] = 1 + letter.isupper()
    return 3


def fuzzy_score(needle: str, haystack: str) -> float:
    if len(needle) > len(haystack):
        return 0

    needle = needle.upper()
    norm_haystack = haystack.upper()

    score = 0
    hi = 0
    ni = 0

    while ni < len(needle):
        if hi >= len(norm_haystack):
            return 0

        if norm_haystack[hi] == needle[ni]:
            score += score_letter(haystack[hi])
            ni += 1

        hi += 1

    return len(needle) / len(haystack) * score


def old_rank(
    query: str,
    haystacks: Haystacks,
    *,
    max_k: int | None = None,
    do_sort: bool = False,
) -> Sequence[SearchResult]:
    results: set[SearchResult] = set()

    for key, entries in haystacks:
        if query:
            score = sum(fuzzy_score(query, entry) for entry in entries if entry)
        else:
            score = 1

        if score:
            results.add(SearchResult(key, score))

        if not do_sort and max_k:
            if len(results) >= max_k:
                break

    result_list = list(results)

    if do_sort:
        result_list.sort(
            key=lambda r: r.score,
            reverse=True,
        )

    if max_k:
        result_list = result_list[:max_k]

    return result_list
