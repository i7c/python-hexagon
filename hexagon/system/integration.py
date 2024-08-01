from flask import Flask
from hexagon.system import App
from typing import Callable
import os


def aws_lambda_setup(init: Callable[[Flask], Flask], appname: str) -> None:
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        init(App(appname))
