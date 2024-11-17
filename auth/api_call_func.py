import aiohttp
from starlette.exceptions import HTTPException

from settings.config import config


async def get_token_info(token: str):
    async with aiohttp.ClientSession() as session:
        url = (f"{config.base_protocol}://{config.redirects['auth']['hostname']}:"
               f"{config.redirects['auth']['port']}/auth/getTokenInfo")
        params = {"token": token}
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            raise HTTPException(status_code=401)
