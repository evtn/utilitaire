from typing import Any, Iterable, Sequence

from utilitaire.stringops import get_plain_chars


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


type QueryEntries = Iterable[tuple[str, list[Any | None]]]


def fuzzy_rank(
    query: str,
    entry_list: QueryEntries,
    *,
    max_k: int | None = None,
    do_sort: bool = False,
) -> Sequence[str]:
    query = get_plain_chars(query).lower()

    results: dict[str, float] = {}

    for key, entries in entry_list:
        if query:
            score = sum(
                fuzzy_score(query, get_plain_chars(str(entry)))
                for entry in entries
                if entry
            )
        else:
            score = 1

        if score:
            results[key] = score

        if not do_sort and max_k:
            if len(results) >= max_k:
                break

    if not do_sort:
        return list(results)

    base = sorted(
        results,
        key=lambda k: results[k],
        reverse=True,
    )

    if max_k:
        base = base[:max_k]

    return base


def fuzzy_rank_list(
    query: str,
    entries: Iterable[str],
    *,
    max_k: int | None = None,
    do_sort: bool = False,
) -> Sequence[str]:
    return fuzzy_rank(
        query,
        ((k, [k]) for k in entries),
        max_k=max_k,
        do_sort=do_sort,
    )
