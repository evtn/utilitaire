A small httpx wrapper automanaging the sessions and adding some sugar

Basic usage:

```python
from utilitaire import HTTPClient

http_client = HTTPClient() # or `from utilitaire import default_http_client`

wiktionary = http_client["https://en.wiktionary.org"]

async def get_word(word: str):
    response = await (wiktionary / "wiki" / word).get() # httpx.Response
    ...
```

When you do a getitem (`[...]`) on HTTPClient, you get a Domain object holding that URL and a HTTPClient reference.
With Domain object you can:

- do `domain / "..."` or `domain.add_path(*segments: str)` to get a Domain with more path segments (or call )
- do `domain[key: value, key2: value]`or `domain.add_query(**params: Any)` to get a Domain with predefined query params
- do `domain.add_headers(**headers: Any)` to get a Domain with predefined headers

After you constructed the Domain you need, you can use `domain.request`:

```python
async def request(
    method: str,
    *,
    url_params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    json: Any | None = None,
) -> httpx.Response:
  ...
```

..or `domain.request_json` (calls request and then returns a json data of the response)

There are also `get`, `get_json`, `post` and `post_json` that fill in the `method` parameter.

If you want to be responsible, call `http_client.close()` when you've finished
