import os

if not __debug__:
    from dotenv import load_dotenv

    load_dotenv()

SPOTIFY_APP_CLIENT_ID = os.environ["SPOTIFY_APP_CLIENT_ID"]
SPOTIFY_APP_CLIENT_SECRET = os.environ["SPOTIFY_APP_CLIENT_SECRET"]
