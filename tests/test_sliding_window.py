import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ratelimiter import SlidingWindowLimiter
from helpers import FakeClock


class TestSlidingWindow(unittest.TestCase):
    def test_allows_up_to_max_requests(self):
        clock = FakeClock()
        limiter = SlidingWindowLimiter(max_requests=2, window_seconds=10, time_func=clock)
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("a"))
        self.assertFalse(limiter.allow("a"))

    def test_old_entries_expire_out_of_window(self):
        clock = FakeClock()
        limiter = SlidingWindowLimiter(max_requests=1, window_seconds=10, time_func=clock)
        self.assertTrue(limiter.allow("a"))
        clock.advance(9.9)
        self.assertFalse(limiter.allow("a"))  # still within window
        clock.advance(0.2)  # now past the 10s window
        self.assertTrue(limiter.allow("a"))

    def test_no_boundary_burst_unlike_fixed_window(self):
        """The exact bug fixed-window has: sliding window must not
        allow 2x max_requests in a short span straddling a boundary."""
        clock = FakeClock()
        limiter = SlidingWindowLimiter(max_requests=2, window_seconds=10, time_func=clock)
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("a"))
        clock.advance(9.99)  # just before window edge
        self.assertFalse(limiter.allow("a"))

    def test_retry_after_reports_zero_when_allowed(self):
        clock = FakeClock()
        limiter = SlidingWindowLimiter(max_requests=1, window_seconds=10, time_func=clock)
        self.assertEqual(limiter.retry_after("a"), 0.0)

    def test_retry_after_reports_remaining_wait(self):
        clock = FakeClock()
        limiter = SlidingWindowLimiter(max_requests=1, window_seconds=10, time_func=clock)
        limiter.allow("a")
        clock.advance(4.0)
        self.assertAlmostEqual(limiter.retry_after("a"), 6.0)

    def test_reset_clears_all_keys(self):
        clock = FakeClock()
        limiter = SlidingWindowLimiter(max_requests=1, window_seconds=10, time_func=clock)
        limiter.allow("a")
        limiter.allow("b")
        limiter.reset()
        self.assertTrue(limiter.allow("a"))
        self.assertTrue(limiter.allow("b"))


if __name__ == "__main__":
    unittest.main()
