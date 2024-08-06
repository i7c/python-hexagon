from hamcrest import assert_that, calling, equal_to, raises
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute, ListAttribute
from pynamodb.models import Model
import hexagon.pynamodb.helpers as sut
import schema as s
import unittest



class TestPynamodbHelpers(unittest.TestCase):

    def test_transform_model_to_schema(self):
        class TestModel(Model):
            class Meta:
                table_name = "foobla"
            foo = UnicodeAttribute(hash_key=True, null=False)
            bar = NumberAttribute(range_key=True, null=False)
            baz = BooleanAttribute(null=True)
            dur = ListAttribute(null=True)

        sch = sut.schema_from_model(TestModel)

        assert_that(
            sch.validate({
                'foo': 'floasdf',
                'bar': 981,
                'baz': False,
                'dur': [{'asdf': 'lol'}]}),
            equal_to({
                'foo': 'floasdf',
                'bar': 981,
                'baz': False,
                'dur': [{'asdf': 'lol'}]})
        )

        assert_that(
            calling(sch.validate).with_args({
                'foo': 'floasdf',
                'bar': 981,
                'baz': False,
                'dur': {'asdf': 'lol'}}),
            raises(s.SchemaError)
        )

    def test_automatic_validation(self):
        class TestModel(Model):
            class Meta:
                table_name = "foobla"
            foo = UnicodeAttribute(hash_key=True, null=False)
            bar = NumberAttribute(range_key=True, null=False)
            baz = BooleanAttribute(null=True)
            dur = ListAttribute(null=True)

        instance = TestModel(
            foo='bla',
            bar=100,
            baz=True,
            dur=[1, 2, 1000]
        )
        d = sut.dict_from_model_instance(instance)

        assert_that(
            d,
            equal_to({
                'foo': 'bla',
                'bar': 100,
                'baz': True,
                'dur': [1, 2, 1000]
            })
        )
