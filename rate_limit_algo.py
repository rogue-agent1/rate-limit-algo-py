#!/usr/bin/env python3
"""Rate limiting algorithms: token bucket, sliding window, leaky bucket, fixed window."""
import time, sys, collections

class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate; self.capacity = capacity
        self.tokens = capacity; self.last = time.time()
    def allow(self):
        now = time.time(); self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1: self.tokens -= 1; return True
        return False

class SlidingWindowLog:
    def __init__(self, limit, window_sec):
        self.limit = limit; self.window = window_sec; self.log = collections.deque()
    def allow(self):
        now = time.time()
        while self.log and self.log[0] <= now - self.window: self.log.popleft()
        if len(self.log) < self.limit: self.log.append(now); return True
        return False

class LeakyBucket:
    def __init__(self, rate, capacity):
        self.rate = rate; self.capacity = capacity; self.water = 0; self.last = time.time()
    def allow(self):
        now = time.time(); self.water = max(0, self.water - (now - self.last) * self.rate)
        self.last = now
        if self.water < self.capacity: self.water += 1; return True
        return False

if __name__ == "__main__":
    for name, limiter in [("TokenBucket", TokenBucket(5, 5)),
                           ("SlidingWindow", SlidingWindowLog(5, 1.0)),
                           ("LeakyBucket", LeakyBucket(5, 5))]:
        allowed = sum(1 for _ in range(10) if limiter.allow())
        print(f"{name}: {allowed}/10 allowed")
