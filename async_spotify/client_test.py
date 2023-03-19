import asyncio
import os

from dotenv import load_dotenv

from async_spotify.client import AsyncSpotifyClient

TRACK_URL = "https://open.spotify.com/track/2z39kvnOiBa0DBbtsCRNA0?si=2e124c6dad114b52"


async def main():
    load_dotenv()
    SPOTIFY_APP_CLIENT_ID = os.environ["SPOTIFY_APP_CLIENT_ID"]
    SPOTIFY_APP_CLIENT_SECRET = os.environ["SPOTIFY_APP_CLIENT_SECRET"]

    client = AsyncSpotifyClient(SPOTIFY_APP_CLIENT_ID, SPOTIFY_APP_CLIENT_SECRET)
    res = await client.get_track(url=TRACK_URL)  # type: ignore
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
