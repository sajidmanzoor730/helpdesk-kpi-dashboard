"""
Sliding window log: each key keeps a log of exact timestamps for its
recent calls. A call is allowed if fewer than `max_requests` timestamps
fall within the last `window_seconds`. This is the most *accurate*
algorithm (no boundary burst issues like fixed windows have) at the
cost of O(requests in window) memory per key instead of O(1).
"""

from __future__ import annotations

import threading
import time
from collections import deque
from typing import Callable

from .base import RateLimiter


class SlidingWindowLimiter(RateLimiter):
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
        self._logs: dict[str, deque[float]] = {}

    def _evict_expired(self, key: str, now: float) -> deque[float]:
        log = self._logs.setdefault(key, deque())
        cutoff = now - self.window_seconds
        while log and log[0] <= cutoff:
            log.popleft()
        return log

    def allow(self, key: str = "default") -> bool:
        with self._lock:
            now = self._time_func()
            log = self._evict_expired(key, now)
            if len(log) < self.max_requests:
                log.append(now)
                return True
            return False

    def retry_after(self, key: str = "default") -> float:
        """Seconds until the oldest logged call expires and a new
        call would be allowed. Returns 0.0 if a call would be allowed now."""
        with self._lock:
            now = self._time_func()
            log = self._evict_expired(key, now)
            if len(log) < self.max_requests:
                return 0.0
            return max(0.0, (log[0] + self.window_seconds) - now)

    def reset(self, key: str | None = None) -> None:
        with self._lock:
            if key is None:
                self._logs.clear()
            else:
                self._logs.pop(key, None)
