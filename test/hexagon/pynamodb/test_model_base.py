import unittest

from hamcrest import assert_that, calling, equal_to, instance_of, is_not, not_, raises
from pynamodb.attributes import ListAttribute, NumberAttribute, UnicodeAttribute
from schema import Schema, SchemaError

from hexagon.pynamodb.model_base import ModelBase


class TestModelBase(unittest.TestCase):
    def test_simple_validation(self):
        class MyModel(ModelBase):
            foo = UnicodeAttribute(hash_key=True, range_key=False)
            dur = NumberAttribute(hash_key=False, range_key=True)

        assert_that(
            calling(MyModel).with_args(
                foo=10,
                dur=100,
            ),
            raises(SchemaError)
        )
        assert_that(
            MyModel(foo='1', dur=10),
            instance_of(MyModel)
        )

    def test_validation_with_custom_schema(self):
        class MyModel(ModelBase):
            foo = ListAttribute()

            def schema(self):
                return Schema({
                    'foo': Schema([str])
                })

        assert_that(
            calling(MyModel).with_args(
                foo=[1, 2, 3, 100]
            ),
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
