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

# TODO fr, en
# TODO allow cancel on app start
# TODO make cards file easily editable on Windows

# Qt framework
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer

# Application modules
from game import Game
from qt import MainWindow
from qtdialogs import DialogHelp, DialogNewGame

# Other modules
from webbrowser import open as webopen

import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

TOP_CARDS = 16  # Number of Pool Selector buttons to display


class App:
    def __init__(self, game, view):
        self.game = game
        self.view = view

        self._cardpool_index = 0

        self.bind_sidebar_buttons()
        self.cb_new_game_dialog()
        # QTimer.singleShot(0, self.cb_new_game_dialog)

    @property
    def cardpool_index(self):
        return min(self._cardpool_index, max(0, len(self.game.deck['draw'].cards) - 1))

    @cardpool_index.setter
    def cardpool_index(self, index):
        self.view.pool_selector.button[self._cardpool_index].set_active(False)
        self._cardpool_index = index
        self.view.pool_selector.button[index].set_active(True)
        self.update_cardpool()

    def bind_sidebar_buttons(self):
        new_game_button = self.view.app_buttons.button_new_game
        new_game_button.clicked.connect(self.cb_new_game_dialog)
        help_button = self.view.app_buttons.button_help
        help_button.clicked.connect(self.cb_help_dialog)
        epidemic = self.view.epidemic_menu.button
        epidemic.clicked.connect(self.cb_epidemic)

    def populate_draw(self):
        logger.debug(f'APP: populate_draw')
        self.view.deck['draw'].clear()
        deck = self.game.deck['draw']
        if not deck.is_empty():
            cards = deck.sorted()
            for card in cards:
                button = self.view.deck['draw'].add_card_button(card)
                button.clicked.connect(lambda b=button, d=deck: self.cb_draw_card(b, d))

    @staticmethod
    def is_last_card(deck):
        return True if deck.name == 'draw' and len(deck.top()) == 1 else False

    def cb_draw_card(self, button, from_deck):
        # Get the deck we're drawing to
        to_deck = self.get_destination()
        card = button.card

        # Ignore drawing from a deck onto itself
        if not from_deck == to_deck and not from_deck == to_deck.parent:
            logger.debug(f'Drawing {button.card.name} from {from_deck.name} to {to_deck.name}')

            # Flag needed to populate draw if last button was removed
            is_last_card = self.is_last_card(from_deck)

            # Move the card and update the game state
            pos = -1 if self.view.destination['draw_top'].isChecked() else 0
            self.game.draw_card(from_deck, to_deck, card, position=pos)

            # Remove the card from the source deck in GUI
            if from_deck.name == 'draw':
                if from_deck.is_empty() or card not in from_deck.top():
                    self.remove_button_from_deck(button, from_deck)
                if is_last_card:
                    self.populate_draw()
            else:
                self.remove_button_from_deck(button, from_deck)

            # Add the card to the GUI
            if to_deck == self.game.deck['draw']:
                if card in self.game.deck['draw'].top():
                    self.add_button_to_deck(button, to_deck)
            else:
                self.add_button_to_deck(button, to_deck)

            # Clamp the active pool button to allowed range
            self.cardpool_index = self.cardpool_index
            self.update_gui()

    def add_button_to_deck(self, button, deck):
        button = self.view.deck[deck.name].add_card_button(button.card)
        if button is not None:
            button.clicked.connect(lambda b=button, d=deck: self.cb_draw_card(b, d))

    def remove_button_from_deck(self, button, deck):
        self.view.deck[deck.name].remove_card_button(button)

    def get_destination(self):
        for item in self.view.destination:
            print(self.view.destination[item].isChecked())
        if self.view.destination['exclude'].isChecked():
            return self.game.deck['exclude']
        if self.view.destination['discard'].isChecked():
            return self.game.deck['discard']
        if self.view.destination['draw_bottom'].isChecked() or \
                self.view.destination['draw_top'].isChecked():
            return self.game.deck['draw']

    def update_cardpool(self):
        logger.debug(f'APP: cb_update_cardpool')
        if self.game.deck['draw'].is_empty():
            self.view.cardpool.show_empty()
        else:
            deck = self.game.deck['draw'].cards[-1-self.cardpool_index]
            self.view.cardpool.show(deck.name, self.cardpool_index+1, deck)

    def update_pool_selector(self):
        logger.debug(f'APP: update_drawdeck')
        for i in range(TOP_CARDS):
            if i < len(self.game.deck['draw']):
                c = self.game.deck['draw'].cards[-1-i]
                text = f'{len(c)}' if len(c) > 1 else c.cards[0].name
                btn = self.view.pool_selector.button[i]
                btn.setEnabled(True)
                btn.set_text(text)
                if not btn.is_connected():
                    btn.clicked.connect(lambda index=i: self.cb_select_cardpool(index))
                    btn.set_connected(True)
            else:
                text = ''
                btn = self.view.pool_selector.button[i]
                btn.set_text(text)
                btn.set_connected(False)
                btn.setEnabled(False)

    def update_epidemic_menu(self):
        """Update the epidemic dropdown list
        based on the available cards in the Draw Deck."""
        deck = self.game.deck['draw']
        if not deck.is_empty():
            items = sorted([c.name for c in list(set(deck.bottom().cards))])
            self.view.epidemic_menu.combo_box.setDisabled(False)
            self.view.epidemic_menu.button.setDisabled(False)
        else:
            items = ['(Draw Deck Empty)']
            self.view.epidemic_menu.combo_box.setDisabled(True)
            self.view.epidemic_menu.button.setDisabled(True)

        self.view.epidemic_menu.combo_box.clear()
        self.view.epidemic_menu.combo_box.addItems(items)

    def update_stats(self):
        self.view.stats.show(self.game.stats)

    def cb_select_cardpool(self, index):
        logger.debug('APP: cb_select_cardpool')
        self.cardpool_index = index

    def cb_new_game_dialog(self):
        logger.debug('APP: cb_new_game')
        games = list(self.game.games.keys())
        dialog = DialogNewGame(games)
        if dialog.exec_():
            self.game.initialise(dialog.combo.currentText())
            self.view.initialise()
            self.populate_draw()
            self.update_gui()
            self.cb_select_cardpool(0)
        else:
            if not self.view.isVisible():
                print('quitting')
                QApplication.quit()

    def cb_epidemic(self):
        """Shuffle epidemic card based on the selected card in the combobox."""
        logger.debug('APP: cb_epidemic')
        new_card_name = self.view.epidemic_menu.combo_box.currentText()
        self.game.epidemic(new_card_name)
        self.view.deck['discard'].clear()
        self.view.deck['draw'].clear()
        self.populate_draw()
        self.update_gui()
        self.cb_select_cardpool(0)

    @staticmethod
    def cb_help_dialog(self):
        logger.debug('APP: cb_help')
        """Callback from the Help button.
        Displays a dialog with the option to view Help in browser."""
        dialog = DialogHelp()
        if dialog.exec_():
            webopen('https://github.com/Merkwurdichliebe/Epidemic/wiki')

    def update_gui(self):
        self.update_pool_selector()
        self.update_epidemic_menu()
        self.update_stats()


def main():
    application = QApplication()
    view = MainWindow()
    model = Game()
    App(model, view)
    view.show()
    application.exec_()


if __name__ == '__main__':
    main()
