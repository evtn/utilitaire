fast remove-only fuzzy search implementation (e.g. for command palettes)


Basic usage:

```python
from utilitaire import fuzzy_score, fuzzy_rank, fuzzy_rank_list

entries = [
    "Oh Wonder",
    "bottle of water",
    "AC/DC",
    "Grand Theft Auto IV",
    "Grand Theft Auto V",
    "Open Settings",
]

# use fuzzy_score to get a score of matching
print(
    fuzzy_score("ow", entries[0]), # 1.33...
    fuzzy_score("ow", entries[1]), # 0.8
    fuzzy_score("ow", entries[2]), # 0
)

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
        max_k=1,
    )
) # ["someid456"]

"""
fuzzy_rank_list(q, entries)

is a shorthand for

fuzzy_rank(q, ((k, [k]) for k in entries))
"""
print(fuzzy_rank_list("gtav", entries, do_sort=True)) # ['Grand Theft Auto V', 'Grand Theft Auto IV']
print(fuzzy_rank_list("gtav", entries, do_sort=False)) # ['Grand Theft Auto IV', 'Grand Theft Auto V']

```
