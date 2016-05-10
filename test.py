import pytest

from pyutils import partition, partition_mapping, strict_zip, duplicates, bound


class TestPartition:
    def test_empty(self):
        assert partition(lambda i: None, []) == ([], [])

    def test_normal(self):
        a, b = partition(lambda i: i % 2 == 0, range(10))
        assert a == [0, 2, 4, 6, 8]
        assert b == [1, 3, 5, 7, 9]

    def test_partition_mapping(self):
        a, b = partition_mapping(lambda k, v: k == v, {1: 2, 3: 3, 4: 5})
        assert a == {3: 3}
        assert b == {1: 2, 4: 5}


class TestStrictZip:
    def test_empty(self):
        assert list(strict_zip()) == []

    def test_successful(self):
        iterables = (1, 2), ('a', 'b'), (True, False)
        assert list(strict_zip(*iterables)) == list(zip(*iterables))

    def test_bad_lengths(self):
        iterables = (1, 2), ('a', 'b', 'c')
        with pytest.raises(ValueError) as exc_info:
            strict_zip(*iterables)
        assert 'length' in str(exc_info.value)
        assert exc_info.value.lens == (2, 3)

    def test_does_not_consume_generators(self):
        assert list(strict_zip(x ** 2 for x in range(5))) == [
            (x,) for x in (0, 1, 4, 9, 16)]


class TestDuplicates:
    def test_empty(self):
        assert duplicates([]) == set()

    def test_normal(self):
        assert duplicates([1, 2, 3]) == set()

    def test_duplicates(self):
        assert duplicates([1, 1, 2, 2, 3]) == {1, 2}


class TestBound:
    def test_no_bounds(self):
        assert bound(42, None, None) == 42

    def test_min_bound_only(self):
        assert bound(41, 42, None) == 42
        assert bound(43, 42, None) == 43

    def test_max_bound_only(self):
        assert bound(41, None, 42) == 41
        assert bound(43, None, 42) == 42

    def test_bounded(self):
        assert bound(40, 41, 43) == 41
        assert bound(42, 41, 43) == 42
        assert bound(44, 41, 43) == 43
