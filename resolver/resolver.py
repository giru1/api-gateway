import aiohttp
from aiohttp import ClientConnectorError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from settings.config import config


class MainResolver:
    def __init__(self, request: Request):
        self.request = request
        self.headers = dict(request.headers)
        self.path = request.url.path
        self.query_params = self.request.query_params if self.request.query_params else None
        self.service_path = self.path.strip('/').split('/')
        if not self.service_path:
            raise HTTPException(status_code=404, detail="Service path not found")
        self.redirect_service = config.redirects.get(self.service_path[0])
        if not self.redirect_service:
            raise HTTPException(status_code=404, detail="Redirect path not found")
        self.new_host_name = self.redirect_service.get('hostname')
        self.new_port = self.redirect_service.get('port')
        self.schema = self.request.url.scheme
        self.url = f"{self.schema}://{self.new_host_name}"
        if self.new_port:
            self.url += f":{self.new_port}"
        self.url += self.path
        self.method = self.request.method.lower()
        self.data = None

    async def load_data(self):
        body = await self.request.body()
        if body:
            self.data = body

    async def make_request(self) -> Response:
        async with aiohttp.ClientSession() as session:
            try:
                async with getattr(session, self.method)(self.url,
                                                         params=self.query_params,
                                                         data=await self.request.body(),
                                                         headers=self.headers) as response:
                    res: aiohttp.ClientResponse = response
                    content = await res.content.read()
                    print("@@@@@@@@@@@@@@@@@@@@@ response from service")
                    print(res.headers)
                    print("@@@@@@@@@@@@@@@@@@@@@ response from service")
            except ClientConnectorError:
                raise HTTPException(status_code=502)
        return Response(content=content, status_code=res.status,
                        media_type=res.headers.get('content-type'))
