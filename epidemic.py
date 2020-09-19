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

from tkgui import MainWindow
from game import Game
import tkdialogs


class App:
    def __init__(self):
        # Instantiate the game-logic object (the Model in MVC)
        self.game = Game()

        # Instantiate the main window (the View in MVC)
        # We pass it the App object so that we can use callbacks
        # (Better way?)
        self.view = MainWindow(self)

        self.show_select_game_dialog()

    def updateview(self):
        self.view.update_cardpool(self.game.deck['draw'])
        self.view.update_exclude(self.game.deck['exclude'])
        self.view.update_drawdeck(self.game.deck['draw'])
        self.view.update_discard(self.game.deck['discard'])
        self.view.update_dropdown(self.game.deck['draw'])
        self.view.update_stats(self.game.stats)

    def show_select_game_dialog(self):
        # Display select new game dialog
        # (We reuse the callback function for the New Game button)
        self.cb_new_game()

    def cb_draw_card(self, from_deck, card):
        # Move a card from a deck to the destination deck
        # set by the radio buttons in MainWindow.
        to_deck = self.game.deck[self.view.get_destination()]
        self.game.draw(from_deck, to_deck, card)
        self.updateview()

    def cb_view_cardpool(self, index):
        # Callback from the buttons used to display the possible choices
        # in the Draw Deck. Outputs the possible cards in each potential draw.
        self.view.cardpool_index = index
        self.view.update_cardpool(self.game.deck['draw'])

    def cb_epidemic(self):
        """Callback from the Epidemic button.
        Runs the epidemic shuffle function based on the selected card."""
        new_card = self.view.get_epidemic()
        self.game.epidemic(new_card)
        self.updateview()

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
            self.game.init(dialog.game_choice.get())
            self.updateview()

    def cb_dialog_help(self):
        """Callback from the Help button.
        Displays a dialog with the option to view Help in browser."""
        dialog = tkdialogs.DialogHelp(self.view.root)
        self.view.root.wait_window(dialog.top)


def main():
    """Main program entry point."""
    app = App()
    app.view.root.mainloop()


if __name__ == '__main__':
    main()
