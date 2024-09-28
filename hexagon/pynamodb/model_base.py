from hexagon.pynamodb.helpers import dict_from_model_instance, schema_from_model
from pynamodb.expressions.condition import Condition
from pynamodb.models import Model, _KeyType
from schema import Schema
from typing import Any, Dict, Optional


class ModelBase(Model):
    class Meta:
        table_name = "UNDEFINED"

    def __init__(
            self,
            hash_key: Optional[_KeyType] = None,
            range_key: Optional[_KeyType] = None,
            _user_instantiated: bool = True,
            **attributes: Any
    ) -> None:
        super().__init__(hash_key, range_key, _user_instantiated, **attributes)

    def save(self, condition: Optional[Condition] = None, *, add_version_condition: bool = True) -> Dict[str, Any]:
        self.validate_schema()
        return super().save(
            condition,
            add_version_condition=add_version_condition
        )

    def schema(self):
        # type: () -> Schema
        return schema_from_model(self)

    def validate_schema(self):
        # type: () -> None
        self.schema().validate(
            dict_from_model_instance(self)
        )
