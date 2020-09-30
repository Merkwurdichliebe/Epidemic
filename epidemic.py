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


MAX_CARDS_IN_CARDPOOL = 35
TOP_CARDS = 16


class App:
    def __init__(self, view, game):
        self.game = game
        self.view = view

        self._cardpool_index = 0

        self.show_select_game_dialog()

        self.cb_select_cardpool(0)
        self.update_drawdeck()

    @property
    def cardpool_index(self):
        return self._cardpool_index

    @cardpool_index.setter
    def cardpool_index(self, index):
        self.view.drawdeck.button[self._cardpool_index].set_active(False)
        self._cardpool_index = index
        self.view.drawdeck.button[index].set_active(True)

    def update_cardpool(self):
        drawdeck = self.game.deck['draw']
        text = f'Deck position: {self.cardpool_index+1}\n\n'
        if not drawdeck.is_empty():
            d = drawdeck.cards[-1 - self.cardpool_index]
            if len(set(d)) < MAX_CARDS_IN_CARDPOOL:
                for card in sorted(set(d.cards), key=lambda x: x.name):
                    text += f'{card.name} ({d.cards.count(card)})\n'
            else:
                text += f'{MAX_CARDS_IN_CARDPOOL}+ cards'
            text += f'\n[{d.name}]'
        self.view.set_cardpool_text(text)

    def update_drawdeck(self):
        for i, c in enumerate(reversed(self.game.deck['draw'].cards[-TOP_CARDS:])):
            # If the top card is a single card we display its name,
            # otherwise we display the number of possible cards.
            if len(c) == 1:
                text = c.cards[0].name
            else:
                text = f'{len(c)}'

            # btn.set_active(True if i == self.cardpool_index else False)
            # btn.clicked.connect(lambda ignore=True, index=i: self.app.cb_update_cardpool(index))  # 1
            btn = self.view.drawdeck.button[i]
            btn.setText(text)
            btn.clicked.connect(lambda index=i: self.cb_select_cardpool(index))

    def cb_select_cardpool(self, index):
        self.cardpool_index = index
        self.update_cardpool()





    def show_select_game_dialog(self):
        # (We reuse the callback function for the New Game button)
        self.cb_new_game()

    def update_gui(self, *decks):
        for deck in decks:
            if deck.name == 'draw':
                self.view.show_drawdeck_old(self.game.deck['draw'])
                self.view.update_epidemic_combo()
                self.view.update_stats(self.game.stats)
            self.view.show_deck(self.game.deck[deck.name])

    def cb_draw_card(self, from_deck, card):
        to_deck = self.view.get_destination()
        if not from_deck == to_deck and not from_deck == to_deck.parent:
            self.game.draw_card(from_deck, to_deck, card)
            self.update_gui(*self.get_all_decks())



    def cb_epidemic(self):
        """Shuffle epidemic card based on the selected card in the combobox."""
        new_card_name = self.view.combo_epidemic.currentText()
        self.game.epidemic(new_card_name)
        self.view.cardpool_index = 0
        self.update_gui(self.game.deck['draw'])
        self.update_gui(self.game.deck['discard'])

    def cb_new_game(self):
        games = list(self.game.games.keys())
        dialog = DialogNewGame(games)
        if dialog.exec_():
            self.game.initialise(dialog.combo.currentText())
            # self.update_gui(*self.get_all_decks())

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
    window = MainWindow()
    model = Game()
    App(window, model)
    window.show()
    application.exec_()


if __name__ == '__main__':
    main()
