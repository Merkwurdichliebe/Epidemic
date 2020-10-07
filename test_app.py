import unittest
from unittest.case import TestCase

from epidemic import App
from game import Game
from qt import MainWindow
from PySide2.QtWidgets import QApplication, QWidget


class TestApp(TestCase):
    def setUp(self):
        self.game = Game()
        self.game.initialise('Small Debug Deck')
        qapp = QApplication()
        self.view = MainWindow()
        self.app = App(self.game, self.view)

    def tearDown(self):
        self.game = None
        self.view = None
        self.app = None

    def test_cardpool_index_clamping(self):
        self.app.cardpool_index = -1
        self.assertEqual(self.app.cardpool_index, 0)


if __name__ == '__main__':
    unittest.main()
