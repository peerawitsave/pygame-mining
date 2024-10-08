import random

class Bag:
    def __init__(self):
        self.bag = []

    def draw(self, o_bag):
        if not self.bag:
            self.bag = o_bag.copy()
            random.shuffle(self.bag)
        return self.bag.pop()


class ProgressiveProbability:
    def __init__(self, initial_success_rate=30, increment=5):
        self.initial_success_rate = initial_success_rate
        self.increment = increment
        self.success_rate = initial_success_rate

    def attempt(self):
        assert 0 <= self.success_rate <= 100, "Success rate must be between 0-100"
        
        p = random.uniform(0, 100)
        
        if p <= self.success_rate:
            return True
        else:
            return False

    def run_attempts(self, num_attempts=10):
        success_occurred = False

        for _ in range(num_attempts):
            success_occurred = self.attempt()
            
            if success_occurred:
                self.success_rate = self.initial_success_rate
                break
            else:
                self.success_rate += self.increment


class FixedRateProbability:
    def __init__(self, initial_success_rate, max_failures):
        assert 0 <= initial_success_rate <= 100, "Success rate must be between 0 and 100"
        self.initial_success_rate = initial_success_rate
        self.success_rate = initial_success_rate
        self.max_failures = max_failures
        self.failure_count = 0

    def attempt(self):
        if self.failure_count >= self.max_failures:
            self.success_rate = self.initial_success_rate
            self.failure_count = 0
            return True

        if random.uniform(0, 100) <= self.success_rate:
            self.success_rate = self.initial_success_rate
            self.failure_count = 0
            return True
        else:
            self.failure_count += 1
            return False

    def run_attempts(self, num_attempts):
        successes = 0
        for _ in range(num_attempts):
            if self.attempt():
                successes += 1
                break