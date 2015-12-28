from unittest import TestCase

from pyutils import partition, strict_zip, bound


class TestPartition(TestCase):
    def test_empty(self):
        self.assertEqual(partition(lambda i: None, []), ([], []))

    def test_normal(self):
        self.assertEqual(
            partition(lambda i: i % 2 == 0, range(10)),
            ([0, 2, 4, 6, 8], [1, 3, 5, 7, 9]))


class TestStrictZip(TestCase):
    def test_empty(self):
        self.assertEqual(list(strict_zip()), [])

    def test_successful(self):
        iterables = (1, 2), ('a', 'b'), (True, False)
        self.assertEqual(list(strict_zip(*iterables)), list(zip(*iterables)))

    def test_bad_lengths(self):
        iterables = (1, 2), ('a', 'b', 'c')
        with self.assertRaisesRegex(ValueError, 'length') as cm:
            strict_zip(*iterables)
        self.assertEqual(cm.exception.lens, (2, 3))

    def test_does_not_consume_generators(self):
        self.assertEqual(
            list(strict_zip(x ** 2 for x in range(5))),
            [(x,) for x in (0, 1, 4, 9, 16)])


class TestBound(TestCase):
    def test_no_bounds(self):
        self.assertEqual(bound(42, None, None), 42)

    def test_min_bound_only(self):
        self.assertEqual(bound(41, 42, None), 42)
        self.assertEqual(bound(43, 42, None), 43)

    def test_max_bound_only(self):
        self.assertEqual(bound(41, None, 42), 41)
        self.assertEqual(bound(43, None, 42), 42)

    def test_bounded(self):
        self.assertEqual(bound(40, 41, 43), 41)
        self.assertEqual(bound(42, 41, 43), 42)
        self.assertEqual(bound(44, 41, 43), 43)
