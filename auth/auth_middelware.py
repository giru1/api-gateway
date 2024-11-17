from urllib.parse import urlencode

from starlette.datastructures import URL
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Scope, Receive, Send

from auth.api_call_func import get_token_info
from auth.query_schema import AuthResponse
from settings.config import config


async def authenticate(request: Request, token: str) -> AuthResponse:
    result = await get_token_info(token)
    print(f"get_token_info {result}")
    res_model = AuthResponse().model_validate(result)
    print(f"res_model {res_model}")
    return res_model


class AuthASGIMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.headers = [(b"test1", b"1"), (b"test2", b"2")]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        scope["scheme"] = config.base_protocol
        request = Request(scope)
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise HTTPException(status_code=401)
        if 'Bearer' not in auth_header:
            raise HTTPException(status_code=401)
        token = auth_header.split(' ')[-1]
        if not token:
            raise HTTPException(status_code=401)
        additional_query_model = await authenticate(request, token)
        q_params = dict(request.query_params)
        if not additional_query_model.managerId:
            for key in AuthResponse().model_dump():
                if key in q_params:
                    q_params.pop(key, None)
        q_params.update(additional_query_model.model_dump(exclude_none=True))
        scope['query_string'] = urlencode(q_params).encode('utf-8')
        await self.app(scope, receive, send)


class RedirectsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        scope["scheme"] = config.base_protocol
        url = URL(scope=scope)
        print('before @@@@@@@@@@@@@@@@@@@')
        print(url.components)
        print('before @@@@@@@@@@@@@@@@@@@')
        service_path = url.path.strip('/').split('/')
        if not service_path:
            raise HTTPException(status_code=404)
        if not service_path:
            raise HTTPException(status_code=404)
        redirect_service = config.redirects.get(service_path[0])
        if not redirect_service:
            raise HTTPException(status_code=404)
        url = url.replace(hostname=redirect_service.get('hostname'),
                          port=redirect_service.get('port'))
        print('after @@@@@@@@@@@@@@@@@@@')
        print(url.components)
        print('after@@@@@@@@@@@@@@@@@@@')
        response = RedirectResponse(url, status_code=301)
        await response(scope, receive, send)
        return


class TestMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        scope["scheme"] = config.base_protocol
        print('galllow1')
        body_size = 0

        async def receive_logging_request_body_size():
            nonlocal body_size
            print('galllow')
            message = await receive()
            assert message["type"] == "http.request"

            body_size += len(message.get("body", b""))

            if not message.get("more_body", False):
                print(f"Size of request body was: {body_size} bytes")

            return message

        await self.app(scope, receive_logging_request_body_size, send)
