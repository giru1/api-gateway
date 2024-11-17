import json
import typing

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    base_protocol: str
    redirects: dict
    debug: bool
    server_workers: int
    host: str
    port: int
    log_level: str
    protect_endpoints: typing.List[str]
    open_endpoints: typing.List[str]

    def __init__(self) -> None:
        super().__init__(**self.loads_config())

    def loads_config(self) -> dict:
        with open('settings/config.json', 'r') as f:
            return json.load(f)


config = Config()
