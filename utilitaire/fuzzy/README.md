fast remove-only fuzzy search implementation (e.g. for command palettes)

Basic usage:

```python
from utilitaire import fuzzy_rank, fuzzy_rank_list

# use fuzzy_rank to rate arbitrary entries by one or more fields
entries = {
    "someid123": ["Fox Stevenson — Tryhard", "Sunk Cost Fallacy"],
    "someid456": ["AC/DC — Shot Down in Flames", "Highway To Hell"]
}

print(
    fuzzy_rank(
        "sdif",
        entries.items(),
        do_sort=True,
    )
) # [SearchResult(haystack_id='someid456', score=697.88)]

entries = [
    "Oh Wonder",
    "bottle of water",
    "AC/DC",
    "Grand Theft Auto IV",
    "Grand Theft Auto V",
    "Open Settings",
]

"""
fuzzy_rank_list(q, entries)

is a shorthand for

fuzzy_rank(q, ((k, [k]) for k in entries))
"""
# [SearchResult(haystack_id='Grand Theft Auto V', score=244.44), SearchResult(haystack_id='Grand Theft Auto IV', score=242.11)]
print(fuzzy_rank_list("gtav", entries, do_sort=True)) 
# [SearchResult(haystack_id='Grand Theft Auto IV', score=242.11), SearchResult(haystack_id='Grand Theft Auto V', score=244.44)]
print(fuzzy_rank_list("gtav", entries, do_sort=False)) 

```
