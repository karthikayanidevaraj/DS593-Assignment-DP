
from client import avg, count, count0, _pretty_print

# Every query consumes epsilon = 0.5
EPSILON = 0.5


class BudgetTracker:
    # Set the starting privacy budget.
    def __init__(self, budget):
        if budget < 0:
            raise ValueError("Budget cannot be negative")

        self.budget = budget

    # Check and update the privacy budget before each query.
    def check_and_update_budget(self):
        if self.budget < EPSILON:
            raise ValueError("Out of budget")

        self.budget -= EPSILON
        return True

    def avg(self, group_by, averaged_column):
        self.check_and_update_budget()
        return avg(group_by, averaged_column, True)

    def count(self, group_by):
        self.check_and_update_budget()
        return count(group_by, True)

    def count0(self, group_by):
        self.check_and_update_budget()
        return count0(group_by, True)


if __name__ == "__main__":
    # Starting budget = 2.0
    # Each query costs 0.5, so four queries are allowed.
    tracker = BudgetTracker(2.0)

    # These four queries should succeed.
    _pretty_print(*tracker.avg(["programming"], "age"))
    _pretty_print(*tracker.count(["age", "music"]))
    _pretty_print(*tracker.count0(["programming"]))
    _pretty_print(*tracker.count(["programming"]))

    # The fifth query should fail.
    _pretty_print(*tracker.avg(["sport"], "age"))
