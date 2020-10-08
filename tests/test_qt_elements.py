from unittest.case import TestCase
import unittest
import qt
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QRadioButton, QPushButton, QComboBox, QWidget


@classmethod
class setUpClass:
    qApp = QApplication()


class TestQtElements(TestCase):
    def setUp(self):
        self.main = QWidget()

    def test_creation_of_app_buttons(self):
        app_buttons = qt.AppButtons()
        self.main.setLayout(app_buttons)

        self.assertIsInstance(app_buttons.button_new_game, QPushButton)
        self.assertEqual(app_buttons.button_new_game.text(), 'New Game')
        self.assertIn(app_buttons.button_new_game, self.main.children())

        self.assertIsInstance(app_buttons.button_help, QPushButton)
        self.assertEqual(app_buttons.button_help.text(), 'Help')
        self.assertIn(app_buttons.button_help, self.main.children())

        self.assertEqual(app_buttons.spacing(), qt.SPACING)

    def test_creation_of_epidemic_menu(self):
        menu = qt.EpidemicMenu()
        self.main.setLayout(menu)

        self.assertIsInstance(menu.combo_box, QComboBox)
        self.assertIsInstance(menu.button, QPushButton)
        self.assertEqual(menu.button.text(), 'Shuffle Epidemic')

        self.assertIn(menu.combo_box, self.main.children())
        self.assertIn(menu.button, self.main.children())

        self.assertEqual(menu.spacing(), qt.SPACING)

    def test_creation_of_destinations_radio_box(self):
        destinations = {
            'dest1': QRadioButton('Destination 1'),
            'dest2': QRadioButton('Destination 2'),
            'dest3': QRadioButton('Destination 3')
        }
        radio_box = qt.DestinationRadioBox(destinations)
        self.assertEqual(len(radio_box.b_group.buttons()), 3)
        for item in destinations.values():
            self.assertIn(item, radio_box.children())

    def test_creation_of_stats_section(self):
        pass


if __name__ == '__main__':
    unittest.main()
