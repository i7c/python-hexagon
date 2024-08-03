from flask import Flask
from hexagon.wsgi.response import WsgiResponse
from typing import Any, Callable, Dict, Optional
import aws_lambda_wsgi
import json


class WsgiRequestBuilder(object):
    def __init__(self):
        # type: () -> None
        self.body: Any = None
        self.method: str = 'GET'
        self.path: str = '/'
        self.query_params: Dict[str, str] = {}
        self.headers: Dict[str, str] = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'x-forwarded-for': "1.2.3.4",
            'x-forwarded-proto': 'http',
        }

        self.app: Optional[Flask] = None
        self.handler: Optional[Callable[[Dict[Any, Any], Any], Any]] = None

        self.parse_json_response: bool = True

    def render(self):
        # type: () -> dict[str, Any]
        request = {
            'httpMethod': self.method,
            'headers': self.headers,
            'path': self.path,
            'queryStringParameters': self.query_params
        }
        if self.body:
            request['body'] = self.body
        return request

    def perform_request_against_app_or_handler(self, handler=None, app=None):
        # type: (Optional[Callable[[dict, Any], Any]], Optional[Flask]) -> Any
        if app:
            return aws_lambda_wsgi.response(app, self.render(), None)
        elif handler:
            return handler(self.render(), None)
        else:
            raise ValueError("You need to pass either an app or a handler")

    def make(self):
        # type: () -> Any
        response = self.perform_request_against_app_or_handler(
            handler=self.handler,
            app=self.app
        )
        try:
            if self.parse_json_response:
                response['body'] = json.loads(response['body'])
        except Exception:
            pass
        return WsgiResponse(response)

    def with_path(self, p):
        # type: (str) -> WsgiRequestBuilder
        self.path = p
        return self

    def with_method(self, m):
        # type (str) -> WsgiRequestBuilder
        self.method = m
        return self

    def with_json_body(self, b):
        # type (Any) -> WsgiRequestBuilder
        self.headers['content-type'] = 'application/json'
        self.headers['accept'] = 'application/json'
        self.body = json.dumps(b)
        return self

    def with_query_param(self, k, v):
        # type (str, str) -> WsgiRequestBuilder
        self.query_params[k] = v
        return self

    def on_handler(self, h):
        # type (Callable[[Dict[Any, Any], Any], Any]) -> WsgiRequestBuilder
        self.handler = h
        return self

    def on_app(self, a):
        # type (Flask) -> WsgiRequestBuilder
        self.app = a
        return self

    def returning_json_response(self):
        # type: () -> WsgiRequestBuilder
        self.parse_json_response = True
        return self

    def returning_raw_response(self):
        # type: () -> WsgiRequestBuilder
        self.parse_json_response = False
        return self


def start() -> WsgiRequestBuilder:
    return WsgiRequestBuilder()
