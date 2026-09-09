"""A controllable fake clock, so tests don't rely on real wall-clock
sleeps and can assert exact behavior at exact time boundaries."""


class FakeClock:
    def __init__(self, start: float = 0.0):
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds
