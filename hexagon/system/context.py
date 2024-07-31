from flask import current_app
from functools import wraps
from typing import Any


def ctx(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "hexagon.system.context" not in current_app.extensions:
            raise ValueError("No context found but injection requested. Did you forget to register it in app setup?")

        args = func.__code__.co_varnames
        if 'ctx' in args:
            nargs = list(args)
            nargs[args.index('ctx')] = current_app.extensions.get("hexagon.system.context")
            nargs_tuple = tuple(nargs)
            return func(*nargs_tuple, **kwargs)
        else:
            raise RuntimeError(
                "Function {} annotated with @ctx, but no ctx param found.".format(
                    func.__name__
                ))
    return wrapper


def register(ctx: Any) -> None:
    if current_app.extensions.get("hexagon.system.context"):
        raise ValueError("System context is already registered, faulty setup")
    else:
        current_app.extensions["hexagon.system.context"] = ctx
