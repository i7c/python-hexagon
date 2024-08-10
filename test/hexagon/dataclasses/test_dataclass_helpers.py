from dataclasses import dataclass
from hamcrest import assert_that, equal_to
from typing import Optional
import hexagon.dataclasses as sut
import unittest


class TestDataclassHelpers(unittest.TestCase):

    def test_simple_promotion(self):

        @dataclass()
        class Foo:
            x: str
            y: int


        @sut.promote
        def simple_func(x: Foo, *args, **kwargs):
            assert_that(type(x), equal_to(Foo))
            assert_that(args, equal_to(("foo", "bla")))
            assert_that(kwargs['barb'], equal_to(1010))

        simple_func(
            {'x': 'foo', 'y': 919},
            "foo",
            "bla",
            barb=1010,
        )
        simple_func(
            Foo(x=10, y="asdf"),
            "foo",
            "bla",
            barb=1010,
        )

    def test_as_dict(self):
        @dataclass
        class Bar:
            x: str
            y: Optional[int]

        assert_that(
            sut.as_dict(Bar(x="foo", y=10)),
            equal_to({'x': 'foo', 'y': 10})
        )

        assert_that(
            sut.as_dict(Bar(x="foo", y=None)),
            equal_to({'x': 'foo'})
        )
