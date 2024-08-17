import unittest
import hexagon.components.wallclock as sut
from hamcrest import assert_that, equal_to, greater_than, calling, raises


class TestWallclock(unittest.TestCase):
    def test_now_returns_a_float(self):
        wc = sut.Wallclock()

        assert_that(wc.now(), greater_than(1723904153))
        assert_that(type(wc.now()), equal_to(float))

    def test_now_returns_passed_param_if_not_none(self):
        wc = sut.Wallclock()

        assert_that(wc.now(1000), equal_to(1000))

    def test_nowi_returns_int(self):
        wc = sut.Wallclock()

        assert_that(wc.nowi(), greater_than(1723904153))
        assert_that(type(wc.nowi()), equal_to(int))


class TestMockWallclock(object):
    def test_ticks(self):
        wc = sut.MockWallclock()

        first = wc.now()
        second = wc.now()

        assert_that(second, greater_than(first))

    def test_wallclock_can_be_stopped_and_started(self):
        wc = sut.MockWallclock()

        wc.stop()

        first = wc.now()
        second = wc.now()

        assert_that(second, equal_to(first))

        third = wc.start()
        fourth = wc.now()

        assert_that(third, greater_than(second))
        assert_that(fourth, greater_than(third))

    def test_wallclock_jitters(self):
        wc = sut.MockWallclock(jitter=0.01, tick_step=1.0)

        first = wc.now()
        wc.now()
        wc.now()
        wc.now()
        wc.now()
        wc.now()
        later = wc.now()

        assert_that(later, greater_than(first + 6))
        

    def test_wallclock_can_be_reset_backwards_but_not_set_backwards(self):
        wc = sut.MockWallclock()

        first = wc.now()

        assert_that(
            calling(wc.set).with_args(first - 10),
            raises(ValueError)
        )

        wc.reset(first - 10)
        second = wc.now()
        assert_that(first, greater_than(second))
        
