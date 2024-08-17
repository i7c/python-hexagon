from flask import Flask, current_app
from functools import wraps
from typing import Any


def context_of(app: Flask):
    return app.extensions.get("hexagon.system.context")


def ctx(func):
    """
    Injects the hexagon context into a function. The annotated
    function must have a parameter called ctx, otherwise this
    annotation will throw.
    """

    args = func.__code__.co_varnames
    if 'ctx' not in args:
        raise RuntimeError(
            "Function {} annotated with @ctx, but no ctx param found.".format(
                func.__name__
            ))

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "hexagon.system.context" not in current_app.extensions:
            raise ValueError("No context found but injection requested. Did you forget to register it in app setup?")
        kwargs['ctx'] = context_of(current_app)
        return func(*args, **kwargs)

    return wrapper


def register_context(app: Flask, ctx: Any) -> None:
    """
    Registers the context for an app. This can be called exactly
    once for setting up the app. Any subsequent calls will throw.

    """
    if app.extensions.get("hexagon.system.context"):
        raise ValueError("System context is already registered, faulty setup")
    else:
        app.extensions["hexagon.system.context"] = ctx
