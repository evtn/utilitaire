A set of various different utils I use that are too small to have their own library.

> Basically I'm tired of copy-pasting stuff and I'm tired of "hmm where is the latest version of that utility function"

This is intentionally not on PyPI and this is not a toolset (like e.g. lodash). It's a collection of stuff.
Some of it might migrate into separate packages sometime later.

To add with uv (replace with specific version):
```
uv add git+https://github.com/evtn/utilitaire --tag 0.1.0
```

**You should pin the release version because I can't promise *anything* about the API stability over the course of development (although I'll try to not break stuff around)**

# Modules

- caser — convert strings between different cases ([full docs here](https://github.com/evtn/utilitaire/tree/lord/utilitaire/caser))
- http — convenient httpx.AsyncClient wrapper and session manager ([full docs here](https://github.com/evtn/utilitaire/tree/lord/utilitaire/http))
- fuzzy — fast remove-only fuzzy search implementation (e.g. for command palettes) ([full docs here](https://github.com/evtn/utilitaire/tree/lord/utilitaire/fuzzy))

# Contributing

The module list might grow (and shrink) over time, but I don't want to accept external contributions for that.
On the other hand, fixes, bug reports and enhancements to existing modules are welcome.
