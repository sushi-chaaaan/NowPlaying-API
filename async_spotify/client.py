import base64
import math
import re
import time
from typing import Any

import aiohttp
from pydantic import HttpUrl

from .cache import CacheFileHandler


class AsyncSpotifyClient:
    _regex_spotify_url = re.compile(
        r"^(http[s]?:\/\/)?open.spotify.com\/(?P<type>track|artist|album|playlist|show|episode|user)\/(?P<id>[0-9A-Za-z]+)(\?.*)?$"  # noqa: E501
    )
    cache_path: str = ".spotify.cache"

    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret

    async def __aenter__(self, client_id: str, client_secret: str) -> "AsyncSpotifyClient":
        self._client_id = client_id
        self._client_secret = client_secret
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def _generate_token(self):
        """Generate a new token and store it in the cache"""

        header = {
            "Authorization": "Basic {0}".format(
                base64.b64encode(f"{self._client_id}:{self._client_secret}".encode()).decode()
            )
        }
        data = {"grant_type": "client_credentials"}

        async with aiohttp.ClientSession() as session:
            async with session.post("https://accounts.spotify.com/api/token", headers=header, data=data) as response:
                data = await response.json()
                try:
                    token = data["access_token"]
                    type = data["token_type"]
                    expires_in = int(data["expires_in"])
                except KeyError:
                    raise Exception("Failed to generate token")
                else:
                    expires_at = math.floor(time.time()) + expires_in
                    cache: dict[str, str | int] = {
                        "token": token,
                        "token_type": type,
                        "expires_in": expires_in,
                        "expires_at": expires_at,
                    }
                    async with CacheFileHandler() as handler:
                        await handler.save_token_to_cache(cache)
        return

    async def _get_token(self) -> str:
        """Get a token from the cache or generate a new one if it doesn't exist"""

        async with CacheFileHandler() as handler:
            cached_token = await handler.get_cached_token()
        if cached_token:
            if cached_token["expires_at"] < math.floor(time.time()):
                await self._generate_token()
                return await self._get_token()
            else:
                return cached_token["token"]
        else:
            await self._generate_token()
            return await self._get_token()

    async def _request(self, endpoint: str, id: str, market: str | None = None) -> dict[str, Any]:
        BASE_API_URL = "https://api.spotify.com/v1"
        async with aiohttp.ClientSession() as session:
            params = {"locale": "ja_JP"}
            if market:
                params["market"] = market

            async with session.get(
                f"{BASE_API_URL}{endpoint}/{id}",
                headers={"Authorization": f"Bearer {await self._get_token()}"},
                params=params,
            ) as response:
                return await response.json()

    def _get_id(self, type: str, url: HttpUrl) -> str:
        match = self._regex_spotify_url.match(url)
        if match is not None:
            groups = match.groupdict()
            if groups["type"] != type:
                raise ValueError("Invalid URL")
            return groups["id"]

        raise ValueError("Invalid URL")

    async def get_track(self, url: HttpUrl) -> dict[str, Any]:
        id = self._get_id("track", url)
        return await self._request("/tracks", id)
