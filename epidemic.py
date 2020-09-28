#!/usr/bin/env python

"""
EPIDEMIC is designed to assist in evaluating card draw probabilities
in the board games Pandemic and Pandemic Legacy.

This is my first attempt at a working project
using the Qt framework and PySide2.

The code attempts to follow a simplified MVC pattern:
Model : Game (in game.py)
View : MainWindow (in qt.py)
Controller : App (in this file)
"""

__author__ = "Tal Zana"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "1.0"

# TODO undo
# TODO fr, en
# TODO parse YML import for empty file or wrong colors
# TODO disable textboxes on game launch
# TODO allow cancel on app start

from PySide2.QtWidgets import QApplication
from qt import MainWindow
from qtdialogs import DialogHelp, DialogNewGame
from game import Game
from webbrowser import open as webopen


class App:
    def __init__(self):
        # Instantiate the game-logic object (the Model in MVC)
        self.game = Game()

        # Instantiate the main window (the View in MVC)
        # We pass it the App object so that we can use callbacks
        self.view = MainWindow(self)
        self.view.show()
        self.show_select_game_dialog()

    def show_select_game_dialog(self):
        # Display select new game dialog
        # (We reuse the callback function for the New Game button)
        self.cb_new_game()

    def update_gui(self, *decks):
        for deck in decks:
            if deck.name == 'draw':
                self.view.show_drawdeck(self.game.deck['draw'])
                self.view.update_epidemic_combo()
                self.view.update_stats(self.game.stats)
            self.view.show_deck(self.game.deck[deck.name])

    def cb_draw_card(self, from_deck, card):
        to_deck = self.view.get_destination()
        if not from_deck == to_deck:
            self.game.draw_card(from_deck, to_deck, card)
            # self.update_gui(from_deck, to_deck)
            # TODO we update all the decks because now the 'draw' destination might actually be one of its decks
            # TODO Also draw into draw deck doesn't filter properly
            self.update_gui(*self.get_all_decks())

    def cb_update_cardpool(self, index):
        self.view.cardpool_index = index
        self.view.show_cardpool(self.game.deck['draw'])

    def cb_epidemic(self):
        """Callback from the Epidemic button.
        Runs the epidemic shuffle function based on the selected card."""
        new_card_name = self.view.combo_epidemic.currentText()
        self.game.epidemic(new_card_name)
        self.update_gui(self.game.deck['draw'])
        self.update_gui(self.game.deck['discard'])

    def cb_new_game(self):
        """Callback from the New Game button.
        Initialises the app for a new game."""
        games = list(self.game.games.keys())
        dialog = DialogNewGame(games)
        if dialog.exec_():
            self.game.initialise(dialog.combo.currentText())
        self.update_gui(*self.get_all_decks())

    @staticmethod
    def cb_dialog_help(self):
        """Callback from the Help button.
        Displays a dialog with the option to view Help in browser."""
        dialog = DialogHelp()
        if dialog.exec_():
            webopen('https://github.com/Merkwurdichliebe/Epidemic/wiki')

    def get_all_decks(self):
        return list(self.game.deck.values())


def main():
    application = QApplication()
    # TODO fix call order
    # window = MainWindow()
    # window.show()
    # pass app to window
    app = App()
    application.exec_()


if __name__ == '__main__':
    main()
