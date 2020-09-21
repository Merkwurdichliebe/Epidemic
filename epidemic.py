#!/usr/bin/env python

"""
EPIDEMIC is designed to assist in evaluating card draw probabilities
in the board game Pandemic. It is my first attempt at a working project
using Tkinter for the GUI.

The Application uses the MVC pattern:
Model : Game (in game.py)
View : MainWindow (in tkgui.py)
Controller : App (in this file)
"""

__author__ = "Tal Zana"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "0.8"

# TODO undo
# TODO fr, en
# TODO parse YML import for empty file or wrong colors
# TODO better tk update method calls
# TODO disable textboxes on game launch
# TODO make game selection dialog receive focus on launch
# TODO For V2 : Make buttons into labels with hover color

from PySide2.QtWidgets import QApplication
from qt import MainWindow
from game import Game


class App:
    def __init__(self):
        # Instantiate the game-logic object (the Model in MVC)
        self.game = Game()

        # Instantiate the main window (the View in MVC)
        # We pass it the App object so that we can use callbacks
        # (Better way?)
        self.view = MainWindow(self)
        self.game.initialise('Legacy Season 2')
        self.update_gui(*self.get_all_decks())
        self.view.show()

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
            self.update_gui(from_deck, to_deck)

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

        # We pass the dialog box a list of the games dictionary's keys,
        # to be displayed in a dropdown menu.
        dialog = tkdialogs.DialogNewGame(self.view.root,
                                         list(self.game.games.keys()))
        self.view.root.wait_window(dialog.top)

        # If the box hasn't been canceled, start a new game.
        if dialog.game_choice is not None:
            self.game.initialise(dialog.game_choice.get())
            self.updateview()

    def cb_dialog_help(self):
        """Callback from the Help button.
        Displays a dialog with the option to view Help in browser."""
        dialog = tkdialogs.DialogHelp(self.view.root)
        self.view.root.wait_window(dialog.top)

    def get_all_decks(self):
        return list(self.game.deck.values())


def main():
    application = QApplication()
    app = App()
    application.exec_()


if __name__ == '__main__':
    main()
