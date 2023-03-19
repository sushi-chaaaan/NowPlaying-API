from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .limiter import limiter


class NowPlayingAPI(FastAPI):
    def __init__(self, title: str, version: str, *args, **kwargs) -> None:
        super().__init__(title=title, version=version, *args, **kwargs)
        self.setup_rate_limiter()
        self.setup_router()

    def setup_rate_limiter(self) -> None:
        self.limiter = limiter
        self.state.limiter = self.limiter
        self.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    def setup_router(self) -> None:
        # from routers.v1.chat import router as v1_chat_router
        # from routers.v1.command import router as v1_command_router
        # from routers.v1.metrics import router as v1_metrics_router
        # from routers.v1.whitelist import router as v1_whitelist_router

        # self.include_router(v1_chat_router, prefix="/v1", tags=["v1"])
        # self.include_router(v1_command_router, prefix="/v1", tags=["v1"])
        # self.include_router(v1_metrics_router, prefix="/v1", tags=["v1"])
        # self.include_router(v1_whitelist_router, prefix="/v1", tags=["v1"])
        return
