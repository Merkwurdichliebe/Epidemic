import unittest
from unittest.case import TestCase

from game import Log


class TestLog(TestCase):
    def setUp(self):
        self.log = Log()

    def tearDown(self):
        pass

    def test_adding_to_log(self):
        self.log.log('Something')
        self.log.log('Something else')
        self.assertEqual(len(self.log), 2)
        self.assertEqual(self.log[-1], 'Something else')

    def test_get_recent_entries(self, entries):
        pass


if __name__ == '__main__':
    unittest.main()
