from pynamodb.attributes import Attribute, BooleanAttribute, ListAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.models import Model
from schema import Schema
from typing import Any, Callable, Dict, List, Tuple
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


def attribute_members(m: Callable) -> List[Tuple[str, Attribute]]:
    return inspect.getmembers_static(
        m,
        lambda m: isinstance(m, Attribute)
    )


def schema_from_model(m: Callable) -> Schema:
    candidates = attribute_members(m)
    return Schema({
        n: schema_from_attr(attr) for n, attr in candidates
    })


def dict_from_model_instance(m: Model) -> Dict[str, Any]:
    attributes = attribute_members(m)
    return {
        arg: getattr(m, arg)
        for arg, _ in attributes
    }
