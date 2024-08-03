from pynamodb.attributes import Attribute, BooleanAttribute, ListAttribute, NumberAttribute, UnicodeAttribute
from schema import Schema
from typing import Callable
import inspect


def schema_from_attr(a: Attribute) -> object:
    if isinstance(a, UnicodeAttribute):
        return str
    elif isinstance(a, NumberAttribute):
        return int
    elif isinstance(a, BooleanAttribute):
        return bool
    elif isinstance(a, ListAttribute):
        return [object]
    else:
        raise ValueError("pynamodb type not supported for schema")


def schema_from_model(m: Callable) -> Schema:
    candidates = inspect.getmembers_static(
        m,
        lambda m: isinstance(m, Attribute)
    )
    return Schema({
        n: schema_from_attr(attr) for n, attr in candidates
    })
