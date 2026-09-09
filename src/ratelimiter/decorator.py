"""Decorator that applies any RateLimiter to a function call."""

from __future__ import annotations

import functools
from typing import Callable, TypeVar

from .base import RateLimiter, RateLimitExceeded

F = TypeVar("F", bound=Callable)


def rate_limited(limiter: RateLimiter, key_func: Callable[..., str] | None = None):
    """
    Decorator factory. By default all calls share the "default" key;
    pass key_func to derive a per-caller key from the call's
    arguments, e.g. key_func=lambda user_id, *a, **kw: user_id.

    Raises RateLimitExceeded instead of silently dropping the call —
    callers decide how to handle that (retry, queue, 429 response).
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs) if key_func else "default"
            if not limiter.allow(key):
                retry_after = None
                if hasattr(limiter, "retry_after"):
                    retry_after = limiter.retry_after(key)
                raise RateLimitExceeded(key, retry_after)
            return func(*args, **kwargs)

        return wrapper

    return decorator
