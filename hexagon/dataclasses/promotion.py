from dacite import from_dict
from dataclasses import is_dataclass
from functools import wraps
import inspect


def promote(func):
    """
    Looks for attributes that are dataclasses and wraps the
    function in code that automatically promotes any dicts to
    dataclasses.
    """
    sig = inspect.signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        promoted_args = []
        for (_name, param), argval in zip(sig.parameters.items(), args):
            if is_dataclass(param.annotation) and not isinstance(argval, param.annotation):
                promoted_args.append(from_dict(param.annotation, argval))
            else:
                promoted_args.append(argval)
        return func(*promoted_args, **kwargs)


    return wrapper
