import errno
import json
import logging

import aiofiles

logger = logging.getLogger(__name__)


class CacheFileHandler:
    """
    Handles reading and writing cached Spotify authorization tokens
    as json files on disk.
    """

    def __init__(self, cache_path: str = ".cache", encoder_cls: str | None = None) -> None:
        self.cache_path = cache_path
        self.encoder_cls = encoder_cls

    async def __aenter__(self) -> "CacheFileHandler":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def get_cached_token(self):
        token_info = None

        try:
            async with aiofiles.open(self.cache_path) as f:
                token_info_string = await f.read()
                token_info = json.loads(token_info_string)
        except IOError as error:
            if error.errno == errno.ENOENT:
                logger.debug("cache does not exist at: %s", self.cache_path)
            else:
                logger.warning("Couldn't read cache at: %s", self.cache_path)

        return token_info

    async def save_token_to_cache(self, token_info):
        try:
            async with aiofiles.open(self.cache_path, "w") as f:
                await f.write(json.dumps(token_info, cls=self.encoder_cls))  # type: ignore
        except IOError:
            logger.warning("Couldn't write token to cache at: %s", self.cache_path)
