"""
Shared interface for all rate limiter implementations.

Every limiter answers one question: `allow(key)` — is this caller
allowed to proceed right now? Each algorithm tracks state per `key`
(e.g. per user ID, per IP, per API token) so one limiter instance can
serve many independent callers.

Design choices, and their tradeoffs:

- Time is injected via `time_func` (defaults to `time.monotonic`)
  instead of called directly. This is the whole reason the test suite
  can assert exact refill/expiry behavior without `time.sleep()` and
  flaky timing — tests pass a fake clock they control.
- Each limiter uses a single `threading.Lock` guarding its entire
  state dict, not one lock per key. That's simpler and definitely
  correct, but it means all keys serialize through one lock — under
  very high concurrency with many distinct keys, a per-key lock (or a
  sharded lock pool) would scale better. Documented here rather than
  silently assumed, since it's a real limitation, not a hidden one.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Callable


class RateLimitExceeded(Exception):
    """Raised by the @rate_limited decorator when a call is denied."""

    def __init__(self, key: str, retry_after: float | None = None):
        self.key = key
        self.retry_after = retry_after
        msg = f"Rate limit exceeded for key={key!r}"
        if retry_after is not None:
            msg += f" (retry after {retry_after:.2f}s)"
        super().__init__(msg)


class RateLimiter(ABC):
    """Common interface implemented by every algorithm in this package."""

    def __init__(self, time_func: Callable[[], float] = time.monotonic):
        self._time_func = time_func

    @abstractmethod
    def allow(self, key: str = "default") -> bool:
        """Return True if a call under `key` is allowed right now, and
        record the attempt as consumed if so."""
        raise NotImplementedError

    def reset(self, key: str | None = None) -> None:
        """Clear state for one key, or all keys if key is None.
        Subclasses override; default is a no-op for simplicity."""
        raise NotImplementedError
