import pytest
from interval import Interval


def test_init_valid():
    i = Interval(1, 3)
    assert i.lo == 1
    assert i.hi == 3


@pytest.mark.parametrize("lo", [1.5, "a", None])
def test_init_lo_type_error(lo):
    with pytest.raises(TypeError):
        Interval(lo, 5)


@pytest.mark.parametrize("hi", [2.2, "x", None])
def test_init_hi_type_error(hi):
    with pytest.raises(TypeError):
        Interval(1, hi)


def test_init_hi_less_than_lo():
    with pytest.raises(ValueError):
        Interval(5, 3)


def test_len_single_point():
    assert len(Interval(2, 2)) == 1


def test_len_positive_range():
    assert len(Interval(0, 4)) == 5


def test_len_negative_range():
    assert len(Interval(-5, -1)) == 5


def test_eq_same_bounds():
    assert Interval(1, 4) == Interval(1, 4)


def test_eq_different_bounds():
    assert Interval(1, 4) != Interval(1, 5)
    assert Interval(1, 4) != Interval(0, 4)


def test_eq_non_interval():
    assert not (Interval(1, 4) == (1, 4))
    assert not (Interval(1, 4) == None)


def test_gt_by_lo():
    assert Interval(5, 6) > Interval(3, 10)


def test_gt_by_hi_when_lo_equal():
    assert Interval(3, 8) > Interval(3, 5)
    assert Interval(3, 5) < Interval(3, 8)


def test_gt_non_interval():
    with pytest.raises(TypeError):
        _ = Interval(1, 2) > 5


def test_overlaps_normal():
    a = Interval(1, 5)
    b = Interval(4, 8)
    assert a.overlaps(b)
    assert b.overlaps(a)


def test_overlaps_containment():
    a = Interval(1, 10)
    b = Interval(3, 4)
    assert a.overlaps(b)
    assert b.overlaps(a)


def test_overlaps_touching():
    a = Interval(1, 3)
    b = Interval(3, 7)
    assert a.overlaps(b)
    assert b.overlaps(a)


def test_overlaps_disjoint():
    a = Interval(1, 3)
    b = Interval(4, 6)
    assert not a.overlaps(b)
    assert not b.overlaps(a)


def test_overlaps_non_interval():
    with pytest.raises(TypeError):
        Interval(1, 2).overlaps("x")


def test_dominates_true():
    assert Interval(1, 10).dominates(Interval(3, 5))


def test_dominates_false():
    assert not Interval(3, 5).dominates(Interval(1, 10))
    assert not Interval(3, 5).dominates(Interval(4, 6))


def test_dominates_equal_intervals():
    assert Interval(1, 5).dominates(Interval(1, 5))


def test_is_dominated_true():
    assert Interval(3, 5).is_dominated(Interval(1, 10))


def test_is_dominated_false():
    assert not Interval(1, 10).is_dominated(Interval(3, 5))


def test_dominates_type_error():
    with pytest.raises(TypeError):
        Interval(1, 2).dominates(7)


def test_is_dominated_type_error():
    with pytest.raises(TypeError):
        Interval(1, 2).is_dominated("x")


def test_merge_overlapping():
    a = Interval(1, 5)
    b = Interval(4, 8)
    m = a.merge(b)
    assert isinstance(m, Interval)
    assert m.lo == 1
    assert m.hi == 8


def test_merge_touching():
    a = Interval(1, 3)
    b = Interval(3, 7)
    m = a.merge(b)
    assert (m.lo, m.hi) == (1, 7)


def test_merge_contained():
    a = Interval(1, 10)
    b = Interval(3, 5)
    m = a.merge(b)
    assert (m.lo, m.hi) == (1, 10)


def test_merge_disjoint_raises():
    a = Interval(1, 3)
    b = Interval(5, 7)
    with pytest.raises(ValueError):
        a.merge(b)


def test_merge_type_error():
    with pytest.raises(TypeError):
        Interval(1, 3).merge("x")


def test_merge_independence():
    a = Interval(1, 4)
    b = Interval(2, 3)
    m = a.merge(b)
    assert m == Interval(1, 4)
    a.lo = 100
    assert m != a
