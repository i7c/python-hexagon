from hamcrest import assert_that, calling, equal_to, instance_of, is_not, not_, raises
from hexagon.pynamodb.model_base import ModelBase
from pynamodb.attributes import ListAttribute, NumberAttribute, UnicodeAttribute
from schema import Schema, SchemaError
from unittest.mock import patch
import unittest


class TestModelBase(unittest.TestCase):
    def test_validation_fails_with_default_schema(self):

        class MyModel(ModelBase):
            foo = UnicodeAttribute(hash_key=True, range_key=False)
            dur = NumberAttribute(hash_key=False, range_key=True)

        problematic = MyModel(foo=100, dur=100)
        assert_that(
            calling(problematic.save),
            raises(SchemaError)
        )

    def test_validation_with_custom_schema(self):
        class MyModel(ModelBase):
            foo = ListAttribute()

            def schema(self):
                return Schema({
                    'foo': Schema([str])
                })

        model = MyModel(foo=[1, 2, 3, 100])

        assert_that(
            calling(model.save),
            raises(SchemaError)
        )

    def test_meta_class(self):
        class SomeModel(ModelBase):
            class Meta:
                table_name = "UNDEFINED"
            pass

        assert_that(SomeModel.Meta.table_name, equal_to("UNDEFINED"))

        SomeModel.Meta.table_name = "derp"
        assert_that(ModelBase.Meta.table_name, equal_to("UNDEFINED"))
