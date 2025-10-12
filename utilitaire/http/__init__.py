from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from httpx import AsyncClient
from pydantic import BaseModel


class HTTPClient:
    sessions: dict[str, AsyncClient]

    def __init__(self):
        self.sessions = {}

    @staticmethod
    def get_baseurl(url: str) -> str:
        parsed = urlparse(url, scheme="https")

        scheme = parsed.scheme
        netloc = parsed.netloc

        return f"{scheme}://{netloc}"

    @staticmethod
    def get_urlrest(url: str) -> str:
        return url[len(HTTPClient.get_baseurl(url)) :]

    async def get_session(self, url: str) -> AsyncClient:
        baseurl = self.get_baseurl(url)

        if baseurl not in self.sessions:
            self.sessions[baseurl] = AsyncClient(base_url=baseurl)

        return self.sessions[baseurl]

    async def request(
        self,
        method: str,
        url: str,
        *,
        url_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **request_kwargs,
    ):
        session = await self.get_session(url)
        urlrest = self.get_urlrest(url)

        return await session.request(
            method,
            urlrest,
            params=url_params,
            headers=headers,
            data=data,
            **request_kwargs,
        )

    def __getitem__(self, url: str) -> Domain:
        if "//" not in url:
            url = f"//{url}"

        return Domain(self, self.get_baseurl(url)) / self.get_urlrest(url)

    async def close(self):
        sessions = self.sessions
        self.sessions = {}

        for client in sessions.values():
            await client.aclose()

        sessions.clear()


class PathParams(BaseModel):
    path: list[str]
    query: dict[str, Any]
    headers: dict[str, Any]


class Domain:
    def __init__(
        self,
        client: HTTPClient,
        baseurl: str,
        params: PathParams | None = None,
    ):
        self.client = client
        self.baseurl = baseurl
        self.params: PathParams = params or PathParams(path=[], query={}, headers={})

    def copy(self) -> Domain:
        return Domain(
            self.client,
            self.baseurl,
            PathParams(
                path=self.params.path,
                query=self.params.query,
                headers=self.params.headers,
            ),
        )

    def __truediv__(self, other: str) -> Domain:
        return self.add_path(*filter(None, other.split("/")))

    def __getitem__(
        self,
        params: tuple[slice[str, Any], ...] | slice[str, Any],
    ) -> Domain:
        items: dict[str, Any] = {}

        if isinstance(params, slice):
            params = (params,)

        for item in params:
            items[item.start] = item.stop

        return self.add_query(**items)

    def add_path(self, *segments: str) -> Domain:
        return self.replace_path(*self.params.path, *segments)

    def replace_path(self, *segments: str) -> Domain:
        new = self.copy()
        new.params.path = [*segments]
        return new

    def add_query(self, **params: Any) -> Domain:
        new = self.copy()
        new.params.query = {**self.params.query, **params}
        return new

    def replace_query(self, **params: Any) -> Domain:
        new = self.copy()
        new.params.query = {**params}
        return new

    def add_headers(self, **headers: Any) -> Domain:
        new = self.copy()
        new.params.headers = {**self.params.headers, **headers}
        return new

    def replace_headers(self, **headers: Any) -> Domain:
        new = self.copy()
        new.params.headers = {**headers}
        return new

    @property
    def path(self):
        return "/".join(self.params.path)

    @property
    def full_url(self):
        return f"{self.baseurl}/{self.path}"

    def request(
        self,
        method: str,
        *,
        url_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **request_kwargs,
    ):
        query: dict[str, Any] = {**self.params.query, **(url_params or {})}
        headers = {**self.params.headers, **(headers or {})}

        return self.client.request(
            method,
            self.full_url,
            url_params=query,
            data=data,
            headers=headers,
            **request_kwargs,
        )

    async def request_json(
        self,
        method: str,
        *,
        url_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **request_kwargs,
    ) -> Any:
        response = await self.request(
            method,
            url_params=url_params,
            data=data,
            headers=headers,
            **request_kwargs,
        )
        return response.json()

    def get(
        self,
        *,
        url_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **request_kwargs,
    ):
        return self.request(
            "get",
            url_params=url_params,
            data=data,
            headers=headers,
            **request_kwargs,
        )

    def post(
        self,
        *,
        url_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **request_kwargs,
    ):
        return self.request(
            "post",
            url_params=url_params,
            data=data,
            headers=headers,
            **request_kwargs,
        )

    async def get_json(
        self,
        *,
        url_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **request_kwargs,
    ) -> Any:
        response = await self.get(
            url_params=url_params,
            data=data,
            headers=headers,
            **request_kwargs,
        )
        return response.json()

    async def post_json(
        self,
        *,
        url_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **request_kwargs,
    ) -> Any:
        response = await self.post(
            url_params=url_params,
            data=data,
            headers=headers,
            **request_kwargs,
        )
        return response.json()


default_http_client = HTTPClient()
