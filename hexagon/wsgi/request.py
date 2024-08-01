from flask import Flask
from typing import Any, Callable, List, Dict, Optional
import aws_lambda_wsgi
import json


class WsgiRequestBuilder(object):
    def __init__(self):
        # type: () -> None
        self.method: str = 'GET'
        self.path: str = '/'
        self.query_params: Dict[str, str] = {}
        self.headers: Dict[str, str] = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'x-forwarded-for': "1.2.3.4",
            'x-forwarded-proto': 'http',
        }

    def render(self):
        # type: () -> dict[str, Any]
        return {
            'httpMethod': self.method,
            'headers': {
            },
            'path': self.path,
            'queryStringParameters': self.query_params
        }

    def perform_request_against_app_or_handler(self, handler=None, app=None):
        # type: (Optional[Callable[[dict, Any], Any]], Optional[Flask]) -> Any
        if app:
            return aws_lambda_wsgi.response(app, self.render(), None)
        elif handler:
            return handler(self.render(), None)
        else:
            raise ValueError("You need to pass either an app or a handler")

    def make(self, handler=None, app=None):
        # type: (Optional[Callable[[dict, Any], Any]], Optional[Flask]) -> Any
        response = self.perform_request_against_app_or_handler(handler=handler, app=app)
        try:
            response['body'] = json.loads(response['body'])
        except Exception:
            pass
        return response

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
