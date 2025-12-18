from typing import Any, Iterable, Sequence, TypeGuard, TypeIs

from utilitaire.stringops import get_plain_chars

from .coretypes import QueryEntries, SearchResult
from .fast import new_rank
from .old import old_rank


def fuzzy_rank(
    query: str,
    entry_list: QueryEntries,
    *,
    max_k: int | None = None,
    do_sort: bool = False,
    use_old: bool = False,
    strip_syms: bool = False,
) -> Sequence[SearchResult]:
    if strip_syms:
        query = get_plain_chars(query)

    query = query.lower()

    def filter_none[T](x: T | None) -> TypeGuard[T]:
        return x is not None

    def stringify(x: Any) -> str:
        base = str(x)

        if strip_syms:
            base = get_plain_chars(base)

        return base

    haystacks = [
        (
            key,
            list(
                map(
                    stringify,
                    filter(
                        filter_none,
                        entries,
                    ),
                )
            ),
        )
        for key, entries in entry_list
    ]

    if use_old:
        func = old_rank
    else:
        func = new_rank

    results = func(
        query,
        haystacks,
        max_k=max_k,
        do_sort=do_sort,
    )

    return results


def fuzzy_rank_list(
    query: str,
    entries: Iterable[str],
    *,
    max_k: int | None = None,
    do_sort: bool = False,
    use_old=True,
) -> Sequence[SearchResult]:
    return fuzzy_rank(
        query,
        ((k, [k]) for k in entries),
        max_k=max_k,
        do_sort=do_sort,
    )
