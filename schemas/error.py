from pydantic import BaseModel


class HTTPExceptionSchema(BaseModel):
    detail: str | dict[str, str | int]


# 429
class TooManyRequests(HTTPExceptionSchema):
    class Config:
        schema_extra = {"example": {"error": "Rate limit exceeded: COUNT per SPAN minute"}}
