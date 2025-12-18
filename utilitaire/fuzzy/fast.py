import heapq
from typing import Sequence

from .coretypes import Haystacks, SearchResult


def search_batch_topk(
    haystacks: Haystacks,
    needle: str,
    top_k: int = 10,
    case_sensitive: bool = False,
    do_sort: bool = False,
) -> Sequence[SearchResult]:
    """
    Ultra-fast fuzzy search returning top K results.

    Args:
        haystacks: List of strings to search
        needle: Search pattern
        top_k: Number of top results to return
        case_sensitive: Whether to match case

    Returns:
        List of top K SearchResult sorted by score (descending)
    """
    if not needle:
        return []

    if not case_sensitive:
        needle = needle.lower()

    needle_len = len(needle)
    if needle_len == 0:
        return []

    # Use min-heap to track top K results
    # We store (-score, result) so largest scores are extracted first
    heap: list[tuple[float, SearchResult]] = []
    min_score_in_heap = float("-inf")

    for haystack_id, hs_set in haystacks:
        score = 0.0

        for haystack in hs_set:
            if not haystack:
                continue

            # Normalize haystack if case-insensitive
            if not case_sensitive:
                haystack_lower = haystack.lower()
            else:
                haystack_lower = haystack

            hay_len = len(haystack_lower)

            # Quick reject: needle longer than haystack
            if needle_len > hay_len:
                continue

            indices = []
            hay_idx = 0
            consecutive_count = 0
            last_idx = -2  # for consecutive matches

            for char in needle:
                while hay_idx < hay_len:
                    if haystack_lower[hay_idx] == char:
                        indices.append(hay_idx)

                        if hay_idx == last_idx + 1:
                            consecutive_count += 1

                        last_idx = hay_idx

                        hay_idx += 1
                        break

                    hay_idx += 1

                else:  # unmatched char
                    break
            else:  # matched here
                span = indices[-1] - indices[0]

                span_score = 1000 * (1 - span / (hay_len - 1)) if hay_len > 1 else 1000

                position_bonus = 200 * (1 - indices[0] / hay_len)

                consecutive_bonus = (
                    (consecutive_count / (needle_len - 1)) * 300
                    if needle_len > 1
                    else 0
                )

                density = needle_len / (span + 1)
                density_bonus = min(density * 200, 200)

                score += span_score + position_bonus + consecutive_bonus + density_bonus

        if not score:
            continue

        if len(heap) < top_k:
            # free real estate (don't have top k yet)
            result = SearchResult(haystack_id, score)
            heapq.heappush(heap, (score, result))

        elif score > min_score_in_heap:
            # can replace some result
            result = SearchResult(haystack_id, score)
            heapq.heapreplace(heap, (score, result))

        if len(heap) == top_k:
            min_score_in_heap = heap[0][0]

    results = [result for _, result in heap]

    if do_sort:
        results.sort(key=lambda x: x.score, reverse=True)

    return results


def search_batch_all(
    haystacks: Haystacks,
    needle: str,
    case_sensitive: bool = False,
    min_score: float = 0.0,
    do_sort: bool = False,
) -> Sequence[SearchResult]:
    """
    Fast fuzzy search returning all matches above min_score.

    Args:
        haystacks: List of strings to search
        needle: Search pattern
        case_sensitive: Whether to match case
        min_score: Minimum score threshold (results below are filtered)

    Returns:
        List of SearchResult sorted by score (descending)
    """
    if not needle:
        return []

    if not case_sensitive:
        needle = needle.lower()

    needle_len = len(needle)
    first_char = needle[0]

    results = []

    for haystack_id, hs_set in haystacks:
        score = 0.0

        for haystack in hs_set:
            if not haystack:
                continue

            if not case_sensitive:
                haystack_lower = haystack.lower()
            else:
                haystack_lower = haystack

            hay_len = len(haystack_lower)

            if needle_len > hay_len or first_char not in haystack_lower:
                continue

            indices = []
            hay_idx = 0
            consecutive_count = 0
            last_idx = -2

            for char in needle:
                while hay_idx < hay_len:
                    if haystack_lower[hay_idx] == char:
                        indices.append(hay_idx)

                        if hay_idx == last_idx + 1:
                            consecutive_count += 1

                        last_idx = hay_idx
                        hay_idx += 1

                        break

                    hay_idx += 1
                else:
                    break
            else:
                span = indices[-1] - indices[0]

                span_score = 1000 * (1 - span / (hay_len - 1)) if hay_len > 1 else 1000
                position_bonus = 200 * (1 - indices[0] / hay_len)
                consecutive_bonus = (
                    (consecutive_count / (needle_len - 1)) * 300
                    if needle_len > 1
                    else 0
                )
                density = needle_len / (span + 1)
                density_bonus = min(density * 200, 200)

                score += span_score + position_bonus + consecutive_bonus + density_bonus

        if score and (score >= min_score):
            results.append(SearchResult(haystack_id, score))

    if do_sort:
        results.sort(key=lambda x: x.score, reverse=True)

    return results


def new_rank(
    query: str,
    haystacks: Haystacks,
    *,
    max_k: int | None = None,
    do_sort: bool = False,
) -> Sequence[SearchResult]:
    if max_k:
        return search_batch_topk(
            haystacks,
            query,
            top_k=max_k,
            do_sort=do_sort,
        )

    return search_batch_all(
        haystacks,
        query,
        do_sort=do_sort,
    )
