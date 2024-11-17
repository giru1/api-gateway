import typing

from pydantic import BaseModel


class AuthResponse(BaseModel):
    ownerId: typing.Optional[str] = None
    organizationId: typing.Optional[str] = None
    workerId: typing.Optional[str] = None
    clientId: typing.Optional[str] = None
    managerId: typing.Optional[str] = None
