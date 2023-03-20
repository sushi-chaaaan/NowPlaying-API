from fastapi import Request
from pydantic import HttpUrl

from app.api import NowPlayingAPI
from async_spotify.client import AsyncSpotifyClient
from const.credentials import SPOTIFY_APP_CLIENT_ID, SPOTIFY_APP_CLIENT_SECRET
from schemas import error as error_schema
from schemas import root as root_schema

app = NowPlayingAPI(title="NowPlayingAPI", version="1.0.0")


@app.get(
    "/",
    responses={
        200: {"model": root_schema.RootPostResponse},
        429: {"model": error_schema.TooManyRequests},
    },
)
async def root(request: Request, url: HttpUrl) -> root_schema.RootPostResponse:
    """
    root endpoint
    """
    post = root_schema.RootPost(url=url)

    client = AsyncSpotifyClient(client_id=SPOTIFY_APP_CLIENT_ID, client_secret=SPOTIFY_APP_CLIENT_SECRET)
    track_info = await client.get_track(post.url)

    track_name: str = track_info["name"]
    track_artists: list[str] = [artist["name"] for artist in track_info["artists"]]
    artists: str = ", ".join(track_artists)
    track_album_name: str = track_info["album"]["name"]

    now_playing_tweet = f"""#NowPlaying
{track_name}/ {artists} - {track_album_name}
{post.url}
"""
    return root_schema.RootPostResponse(
        url=post.url,
        message=now_playing_tweet,
    )


# @app.get("/sentry-debug")
# @limiter.limit("1/minute")
# async def trigger_error(request: Request):
#     """cause error and test Sentry alert"""
#     try:
#         division_by_zero = str(1 / 0)
#     except Exception as e:
#         from sentry_sdk import capture_exception

#         division_by_zero = str(e.__class__)
#         capture_exception(e)
#     return {"message": "{}: please check sentry".format(str(division_by_zero))}


def main() -> None:
    # import sentry_sdk
    import uvicorn

    # sentry_sdk.init(
    #     dsn=os.environ["SENTRY_DSN"],
    #     # Set traces_sample_rate to 1.0 to capture 100%
    #     # of transactions for performance monitoring.
    #     # We recommend adjusting this value in production
    #     # ----------------advice by Sentry------------------
    #     # but set to 1.0 because this API is tiny service
    #     traces_sample_rate=1.0,
    # )

    uvicorn.run("main:app", host="0.0.0.0", port=8088)


def main_dev() -> None:
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)


if __name__ == "__main__":
    main()
