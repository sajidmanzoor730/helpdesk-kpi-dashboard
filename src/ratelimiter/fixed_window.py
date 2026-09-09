"""
Fixed window counter: time is divided into fixed-size windows (e.g.
every 60s, aligned to the epoch). Each key gets a counter that resets
when the window rolls over. O(1) memory per key — the cheapest
algorithm here — but it has a known boundary flaw: a caller can send
`max_requests` right before a window ends and another `max_requests`
right after, getting 2x the intended rate in a short burst around the
boundary. Documented deliberately, since pretending this doesn't
happen would defeat the point of implementing three algorithms to
compare.
"""

from __future__ import annotations

import threading
import time
from typing import Callable

from .base import RateLimiter


class FixedWindowLimiter(RateLimiter):
    def __init__(
        self,
        max_requests: int,
        window_seconds: float,
        time_func: Callable[[], float] = time.monotonic,
    ):
        if max_requests <= 0:
            raise ValueError("max_requests must be positive")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be positive")

        super().__init__(time_func)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        # key -> (window_index, count_in_that_window)
        self._counters: dict[str, tuple[int, int]] = {}

    def _current_window(self, now: float) -> int:
        return int(now // self.window_seconds)

    def allow(self, key: str = "default") -> bool:
        with self._lock:
            now = self._time_func()
            window = self._current_window(now)
            stored_window, count = self._counters.get(key, (window, 0))

            if stored_window != window:
                count = 0
                stored_window = window

            if count < self.max_requests:
                self._counters[key] = (stored_window, count + 1)
                return True

            self._counters[key] = (stored_window, count)
            return False

    def reset(self, key: str | None = None) -> None:
        with self._lock:
            if key is None:
                self._counters.clear()
            else:
                self._counters.pop(key, None)
