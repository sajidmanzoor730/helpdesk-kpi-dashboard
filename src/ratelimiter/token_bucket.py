"""
Token bucket: each key has a bucket that holds up to `capacity`
tokens and refills at `refill_rate` tokens/second. Each allowed call
consumes one token. This is the algorithm most production rate
limiters (AWS, Stripe, etc.) actually use, because it allows short
bursts up to `capacity` while enforcing a steady average rate.
"""

from __future__ import annotations

import threading
import time
from typing import Callable

from .base import RateLimiter


class TokenBucketLimiter(RateLimiter):
    def __init__(
        self,
        capacity: int,
        refill_rate: float,
        time_func: Callable[[], float] = time.monotonic,
    ):
        """
        capacity: max tokens (= max burst size) a bucket can hold.
        refill_rate: tokens added per second.
        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("refill_rate must be positive")

        super().__init__(time_func)
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._lock = threading.Lock()
        # key -> (tokens_remaining, last_refill_timestamp)
        self._buckets: dict[str, tuple[float, float]] = {}

    def _refill(self, key: str) -> float:
        """Returns current token count after applying elapsed refill.
        Must be called while holding self._lock."""
        now = self._time_func()
        tokens, last = self._buckets.get(key, (self.capacity, now))
        elapsed = max(0.0, now - last)
        tokens = min(self.capacity, tokens + elapsed * self.refill_rate)
        self._buckets[key] = (tokens, now)
        return tokens

    def allow(self, key: str = "default") -> bool:
        with self._lock:
            tokens = self._refill(key)
            if tokens >= 1:
                tokens -= 1
                _, last = self._buckets[key]
                self._buckets[key] = (tokens, last)
                return True
            return False

    def tokens_remaining(self, key: str = "default") -> float:
        """Read-only peek at current tokens, without consuming one."""
        with self._lock:
            return self._refill(key)

    def reset(self, key: str | None = None) -> None:
        with self._lock:
            if key is None:
                self._buckets.clear()
            else:
                self._buckets.pop(key, None)
