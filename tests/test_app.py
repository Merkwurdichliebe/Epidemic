import unittest
from unittest.case import TestCase
from unittest.mock import patch

import epidemic


# class TestApp(TestCase):
#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def test_cardpool_index_clamping(self):
#         index_min = 0
#         index_max = min(len(self.game.deck['draw']), 16)-1
#         self.app.cardpool_index = -1
#         self.assertEqual(self.app.cardpool_index, index_min)
#         self.app.cardpool_index = 100
#         self.assertEqual(self.app.cardpool_index, index_max)
#         self.app.cardpool_index = 3
#         self.assertEqual(self.app.cardpool_index, 3)
#         with self.assertRaises(ValueError):
#             self.app.cardpool_index = 'something else'


if __name__ == '__main__':
    unittest.main()
