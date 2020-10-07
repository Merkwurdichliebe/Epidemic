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
        self.qapp = QApplication()
        self.view = MainWindow()
        self.app = App(self.game, self.view)
        self.qapp.exec_()

    def tearDown(self):
        QApplication.quit()

    def test_cardpool_index_clamping(self):
        self.app.cardpool_index = -1
        self.assertEqual(self.app.cardpool_index, 0)
        self.app.cardpool_index = 100
        self.assertEqual(self.app.cardpool_index,
                         len(self.game.deck['draw'])-1)
        self.app.cardpool_index = 3
        self.assertEqual(self.app.cardpool_index, 3)
        with self.assertRaises(ValueError):
            self.app.cardpool_index = 'something else'

    def test_populate_draw(self):
        self.app.populate_draw()


if __name__ == '__main__':
    unittest.main()
