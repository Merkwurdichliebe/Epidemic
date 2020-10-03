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


STATS_MAX = 10
CARDPOOL_MAX = 35
TOP_CARDS = 16


class App:
    def __init__(self, view, game):
        self.game = game
        self.view = view

        self._cardpool_index = 0

        self.cb_new_game_dialog()
        self.cb_select_cardpool(0)
        self.update_drawdeck()
        self.populate_draw()

    def populate_draw(self):
        deck = self.game.deck['draw']
        cards = deck.sorted()
        for card in cards:
            button = self.view.deck['draw'].add_card_button(card)
            button.clicked.connect(lambda b=button, d=deck: self.cb_draw_card(b, d))

    def cb_draw_card(self, button, from_deck):
        # Get the deck we're drawing to
        to_deck = self.get_destination()

        # Ignore drawing from a deck onto itself
        if not from_deck == to_deck and not from_deck == to_deck.parent:
            print(f'Drawing {button.card.name} from {from_deck.name} to {to_deck.name}')

            # Move the card and update the game state
            self.game.draw_card(from_deck, to_deck, button.card)

            # Remove the card from the source deck in GUI
            if from_deck.name == 'draw':
                if button.card not in from_deck.top():
                    self.remove_button_from_deck(button, from_deck)
            else:
                self.remove_button_from_deck(button, from_deck)

            # Add the card to the destination deck in GUI
            if to_deck.has_parent():  # Deck is part of the Draw Deck
                # Add the button only if it's not already displayed
                if button.card.name not in self.view.deck[to_deck.parent.name].cards:
                    self.add_button_to_deck(button, self.game.deck['draw'])
            else:
                self.add_button_to_deck(button, to_deck)
            self.update_cardpool()
            self.update_drawdeck()

    def add_button_to_deck(self, button, deck):
        button = self.view.deck[deck.name].add_card_button(button.card)
        button.clicked.connect(lambda b=button, d=deck: self.cb_draw_card(b, d))

    def remove_button_from_deck(self, button, deck):
        self.view.deck[deck.name].remove_card_button(button)

    def get_destination(self):
        if self.view.destination['exclude'].isChecked():
            return self.game.deck['exclude']
        if self.view.destination['discard'].isChecked():
            return self.game.deck['discard']
        if self.view.destination['draw_top'].isChecked():
            return self.game.deck['draw']
        if self.view.destination['draw_pool'].isChecked():
            if not self.game.deck['draw'].is_empty():
                return self.game.deck['draw'].cards[-1 - self.cardpool_index]
            else:
                return self.game.deck['draw']

    @property
    def cardpool_index(self):
        return self._cardpool_index

    @cardpool_index.setter
    def cardpool_index(self, index):
        self.view.drawdeck.button[self._cardpool_index].set_active(False)
        self._cardpool_index = index
        self.view.drawdeck.button[index].set_active(True)

    def update_cardpool(self):
        text = f'Deck position: {self.cardpool_index+1}\n\n'
        if not self.game.deck['draw'].is_empty():
            d = self.game.deck['draw'].cards[-1-self._cardpool_index]
            if len(set(d)) < CARDPOOL_MAX:
                for card in sorted(set(d.cards), key=lambda x: x.name):
                    text += f'{card.name} ({d.cards.count(card)})\n'
            else:
                text += f'{CARDPOOL_MAX}+ cards'
            text += f'\n[{d.name}]'
        self.view.cardpool.set_text(text)

    def update_drawdeck(self):
        for i, c in enumerate(reversed(self.game.deck['draw'].cards[-TOP_CARDS:])):
            text = f'{len(c)}' if len(c) > 1 else c.cards[0].name
            btn = self.view.drawdeck.button[i]
            btn.setText(text)
            btn.clicked.connect(lambda index=i: self.cb_select_cardpool(index))

    def cb_select_cardpool(self, index):
        self.cardpool_index = index
        self.update_cardpool()

    def cb_new_game_dialog(self):
        games = list(self.game.games.keys())
        dialog = DialogNewGame(games)
        if dialog.exec_():
            self.game.initialise(dialog.combo.currentText())
            # self.update_gui(*self.get_all_decks())









    def update_gui(self, *decks):
        for deck in decks:
            if deck.name == 'draw':
                self.view.show_drawdeck_old(self.game.deck['draw'])
                self.view.update_epidemic_combo()
                self.view.update_stats(self.game.stats)
            self.view.show_deck(self.game.deck[deck.name])





    def cb_epidemic(self):
        """Shuffle epidemic card based on the selected card in the combobox."""
        new_card_name = self.view.combo_epidemic.currentText()
        self.game.epidemic(new_card_name)
        self.view.cardpool_index = 0
        self.update_gui(self.game.deck['draw'])
        self.update_gui(self.game.deck['discard'])



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
    view = MainWindow()
    model = Game()
    App(view, model)
    view.show()
    application.exec_()


if __name__ == '__main__':
    main()
