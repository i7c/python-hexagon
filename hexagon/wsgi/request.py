from flask import Flask
from typing import Any, Callable, List, Dict, Optional
import aws_lambda_wsgi


class WsgiRequestBuilder(object):
    def __init__(self):
        # type: () -> None
        self.method: str = 'GET'
        self.path: str = '/'
        self.protocol: str = 'http'
        self.proxies: List[str] = ['1.2.3.4']
        self.query_params: Dict[str, str] = {}

    def render(self):
        # type: () -> dict[str, Any]
        return {
            'httpMethod': self.method,
            'headers': {
                'x-forwarded-for': ", ".join(self.proxies),
                'x-forwarded-proto': self.protocol,
            },
            'path': self.path,
            'queryStringParameters': self.query_params
        }

    def make(self, handler=None, app=None):
        # type: (Optional[Callable[[dict, Any], Any]], Optional[Flask]) -> Any
        if app:
            return aws_lambda_wsgi.response(app, self.render(), None)
        elif handler:
            return handler(self.render(), None)
        else:
            raise ValueError("You need to pass either an app or a handler")

    def with_path(self, p):
        # type: (str) -> WsgiRequestBuilder
        self.path = p
        return self

    def with_method(self, m):
        # type (str) -> WsgiRequestBuilder
        self.method = m
        return self

    def with_query_param(self, k, v):
        # type (str, str) -> WsgiRequestBuilder
        self.query_params[k] = v
        return self


def start() -> WsgiRequestBuilder:
    return WsgiRequestBuilder()
