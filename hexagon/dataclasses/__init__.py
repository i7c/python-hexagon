from functools import wraps
import dacite
import dataclasses
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
            if (dataclasses.is_dataclass(param.annotation)
                and not isinstance(argval, param.annotation)):
                promoted_args.append(
                    dacite.from_dict(param.annotation, argval)
                )
            else:
                promoted_args.append(argval)
        return func(*promoted_args, **kwargs)
    return wrapper


def as_dict(dc):
    """
    Takes a dataclass instance and transforms it into dicts,
    removing any keys with None values."
    """
    return dataclasses.asdict(
        dc,
        dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
    )


def as_obj(dc):
    """
    Takes a dataclass instance or list of dataclass instances and
    transforms them into dicts or list of dicts recursively.
    """
    if dataclasses.is_dataclass(dc):
        return as_dict(dc)
    elif isinstance(dc, list):
        return [as_obj(el) for el in dc]
    else:
        raise ValueError("Cannot transform to object {}".format(dc))
