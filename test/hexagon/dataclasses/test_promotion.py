from dataclasses import dataclass
from hamcrest import assert_that, equal_to
import hexagon.dataclasses.promotion as sut
import unittest


class TestDataclassesPromotion(unittest.TestCase):

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
