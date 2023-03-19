from pydantic import BaseModel, HttpUrl


class RootBase(BaseModel):
    pass


class RootPost(RootBase):
    url: HttpUrl

    class Config:
        schema_extra = {"example": {"url": "https://open.spotify.com/track/6u1FJReSSuQ2mEc4aRkIuV?si=30e251a21b804ab5"}}


class RootPostResponse(RootPost):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "SOME_COOL_NOW_PLAYING_MESSAGE",
                "url": "https://open.spotify.com/track/6u1FJReSSuQ2mEc4aRkIuV?si=30e251a21b804ab5",
            }
        }
