from flask import Flask
import aws_lambda_wsgi

_app: Flask = None


def App(app_name: str):
    """
    Creates and returns a global singleton for the flask app. This
    should be used for productive executions, do not use it in
    testing. Call this only once during setup, use app() for accessing
    it.

    """
    global _app
    _app = Flask(app_name)
    return _app


def app_exec(event, context):
    global _app
    if not _app:
        raise RuntimeError("App singleton has not been created. Forgot to call App()?")
    return aws_lambda_wsgi.response(_app, event, context)
