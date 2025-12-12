class Interval:
    """Inclusive intervals"""

    def __init__(self, lo: int, hi: int):
        if not isinstance(lo, int):
            raise TypeError(f"lo must be int, not {type(lo)}")
        self.lo = lo
        if not isinstance(hi, int):
            raise TypeError(f"hi must be int, not {type(hi)}")
        if hi < lo:
            raise ValueError("hi must be greater than lo")
        self.hi = hi

    def __repr__(self):
        return f"Interval({self.lo}, {self.hi})"

    def __str__(self):
        return f"[{self.lo}, {self.hi}]"

    def __len__(self):
        return self.hi - self.lo + 1

    def __eq__(self, other):
        if not isinstance(other, Interval):
            return False
        return self.hi == other.hi and self.lo == other.lo

    def __gt__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("could not compare against object that is not an Interval")
        if self.lo > other.lo:
            return True
        return self.hi > other.hi

    def overlaps(self, other):
        if not isinstance(other, Interval):
            raise TypeError("could not compare against object that is not an Interval")
        if self.lo <= other.lo and self.hi >= other.lo:
            return True
        return self.lo <= other.hi and self.hi >= other.lo

    def is_adjacent(self, other):
        if not isinstance(other, Interval):
            raise TypeError("could not compare against object that is not an Interval")
        return self.hi + 1 == other.lo or other.hi + 1 == self.lo

    def dominates(self, other):
        if not isinstance(other, Interval):
            raise TypeError("could not compare against object that is not an Interval")
        return self.lo <= other.lo and self.hi >= other.hi

    def is_dominated(self, other):
        if not isinstance(other, Interval):
            raise TypeError("could not compare against object that is not an Interval")
        return other.dominates(self)

    def merge(self, other):
        if not isinstance(other, Interval):
            raise TypeError("could not compare against object that is not an Interval")

        if not self.overlaps(other) and not self.is_adjacent(other):
            raise ValueError("Can only merge overlapping or adjacent Intervals")
        return Interval(min(self.lo, other.lo), max(self.hi, other.hi))
