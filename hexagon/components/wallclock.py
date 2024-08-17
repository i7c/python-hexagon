from typing import runtime_checkable, Protocol
import random
import time


@runtime_checkable
class WallclockProto(Protocol):
    def now(self, tnow: float = None) -> float:
        ...

    def nowi(self, tnowi: int = None) -> int:
        ...


class Wallclock(object):
    def now(self, tnow: float = None) -> float:
        return tnow or time.time()

    def nowi(self, tnowi: int = None) -> int:
        return tnowi or int(time.time())


class MockWallclock(object):
    def __init__(
            self,
            ticking: bool = True,
            tick_step: float = 1.00001001,
            jitter: float = 0.0,
    ) -> None:
        self.wctime: float = 1000000000.0
        self.ticking: bool = ticking
        self.tick_step: float = tick_step
        self.jitter: float = jitter

    def tick(self) -> None:
        if self.ticking:
            self.wctime += self.tick_step + random.uniform(0.0, self.jitter)

    def stop(self) -> float:
        self.tick()
        self.ticking = False
        return self.wctime

    def start(self) -> float:
        self.ticking = True
        self.tick()
        return self.wctime

    def now(self, tnow: float = None) -> float:
        self.tick()
        return tnow or self.wctime

    def nowi(self, tnow: int = None) -> int:
        self.tick()
        return int(tnow or self.wctime)

    def set(self, stime: float) -> float:
        if stime < self.wctime:
            raise ValueError("Cannot set mock wallclock backward. If you need to, use reset().")
        self.wctime = stime
        return self.wctime

    def reset(self, stime: float) -> float:
        self.wctime = stime
        return self.wctime
