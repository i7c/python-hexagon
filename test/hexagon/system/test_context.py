from aws_lambda_wsgi import response
from flask import Flask
from hamcrest import assert_that, equal_to, calling, raises
import hexagon.system.context as sut
import unittest


class ContextTest(unittest.TestCase):

    def test_successful_context_injection(self):
        app = Flask("testapp")

        class MyContext1(object):
            x = "10"

        @app.route("/")
        @sut.ctx
        def handler(ctx: MyContext1):
            return ctx.x

        with app.test_request_context():
            ctx = MyContext1()
            sut.register_context(app, ctx)

            resp = response(app, {
                'httpMethod': 'GET',
                'queryStringParameters': {},
                'path': '/',
                'headers': {'x-forwarded-proto': 'http'}
            }, None)
            assert_that(resp['statusCode'], equal_to(200))
            assert_that(resp['body'], equal_to("10"))

    def test_failed_context_injection_missing_param(self):
        app = Flask("testapp")

        @app.route("/")
        def handler():
            return "5"

        assert_that(calling(sut.ctx).with_args(handler),
                    raises(RuntimeError))

    def test_failed_context_injection_missing_register(self):
        app = Flask("testapp")

        class MyContext(object):
            x: int = 10

        @app.route("/")
        @sut.ctx
        def handler(ctx: MyContext):
            return ctx.x

        with app.test_request_context():
            resp = response(
                app,
                {
                    'httpMethod': 'GET',
                    'queryStringParameters': {},
                    'path': '/',
                    'headers': {'x-forwarded-proto': 'http'}
                },
                None
            )
            assert_that(resp['statusCode'], 500)
