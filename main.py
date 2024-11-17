import os

import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from auth.auth_middelware import AuthASGIMiddleware
from resolver.resolver import MainResolver
from settings.config import config


async def resolver(request: Request) -> Response:
    return await MainResolver(request).make_request()

ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
routes = []
for path in config.open_endpoints:
    routes.append(
        Route(path, resolver,
              methods=ALLOWED_METHODS),
    )
for path in config.protect_endpoints:
    routes.append(
        Route(path, resolver,
              methods=ALLOWED_METHODS,
              middleware=[Middleware(AuthASGIMiddleware)]),
    )

app = Starlette(debug=config.debug, routes=routes)

origins = os.environ.get('ORIGINS', '').split(';')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=config.host,
                port=int(os.getenv('API_GATEWAY_PORT')),
                workers=config.server_workers,
                log_level=config.log_level)
