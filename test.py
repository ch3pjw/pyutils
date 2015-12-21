from unittest import TestCase

from pyutils import partition


class TestParition(TestCase):
    def test_empty(self):
        self.assertEqual(partition(lambda i: None, []), ([], []))

    def test_normal(self):
        self.assertEqual(
            partition(lambda i: i % 2 == 0, range(10)),
            ([0, 2, 4, 6, 8], [1, 3, 5, 7, 9]))
