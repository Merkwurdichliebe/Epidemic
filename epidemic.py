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


# Qt framework
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer

# Application modules
from game import Game
from qt import MainWindow
from qtdialogs import DialogHelp, DialogNewGame

# Other modules
from webbrowser import open as webopen
from enum import Enum

import logging
logging.basicConfig(
    level='DEBUG', format='%(levelname)s : %(filename)s : %(message)s')
# logging.disable()


class App:
    def __init__(self, game, view):
        logging.info('[App] init')
        self.game = game
        self.view = view
        self.game.log.view = self.view.log
        self._cardpool_index = 0

        self.bind_sidebar_buttons()
        QTimer.singleShot(0, self.cb_new_game_dialog)

    @ property
    def cardpool_index(self):
        return self._cardpool_index

    @ cardpool_index.setter
    def cardpool_index(self, index):
        if isinstance(index, int):
            self.view.pool_selector.button[self._cardpool_index].set_active(
                False)
            new_index = max(
                0, min(index, min(self.view.top_cards-1, len(self.game.deck['draw'])-1)))
            self.view.pool_selector.button[new_index].set_active(
                True)
            self._cardpool_index = new_index
            self.update_cardpool()
        else:
            raise ValueError('Integer expected for cardpool index')

    def bind_sidebar_buttons(self):
        logging.info('Binding sidebar buttons')
        new_game = self.view.app_buttons.button_new_game
        new_game.clicked.connect(self.cb_new_game_dialog)
        help = self.view.app_buttons.button_help
        help.clicked.connect(self.cb_help_dialog)
        epidemic = self.view.epidemic_menu.button
        epidemic.clicked.connect(self.cb_epidemic)

    def populate_draw(self):
        logging.info(f'Populating Draw Deck')
        self.view.deck['draw'].clear()
        deck = self.game.deck['draw']
        if not deck.is_empty():
            cards = deck.sorted()
            for card in cards:
                button = self.view.deck['draw'].add_card_button(card)
                button.clicked.connect(
                    lambda b=button, d=deck: self.cb_draw_card(b, d))

    @ staticmethod
    def is_last_card(deck):
        return True if deck.name == 'draw' and len(deck.top()) == 1 else False

    def cb_draw_card(self, button, from_deck):
        logging.info('Drawing Card')
        # Get the deck we're drawing to
        to_deck, position = self.get_destination()

        # Ignore drawing from a deck onto itself
        if not from_deck == to_deck and not from_deck == to_deck.parent:
            self.draw_card(button, from_deck, to_deck, position)

    def draw_card(self, button, from_deck, to_deck, position):
        logging.info(
            f'Drawing {button.card.name} ({from_deck.name} -> {to_deck.name})')

        card = button.card

        # Flag needed to populate draw if last button was removed
        is_last_card = self.is_last_card(from_deck)

        # Move the card and update the game state
        self.game.draw_card(from_deck, to_deck, card, position=position)

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
            self.populate_draw()
        else:
            self.add_button_to_deck(button, to_deck)

        # Clamp the active pool button to allowed range
        self.cardpool_index = self.cardpool_index

        self.update_gui()

    def add_button_to_deck(self, button, deck):
        logging.info(f'Adding button {button.card.name} to {deck.name}')
        button = self.view.deck[deck.name].add_card_button(button.card)
        if button is not None:
            button.clicked.connect(
                lambda b=button, d=deck: self.cb_draw_card(b, d))

    def remove_button_from_deck(self, button, deck):
        logging.info(f'Removing button {button.card.name} from {deck.name}')
        self.view.deck[deck.name].remove_card_button(button)

    def get_destination(self):
        """Return the Game Deck based on the selected radio button."""
        for item in self.view.destination:
            if self.view.destination[item].isChecked():
                deck, position = self.splitter(item, '_')
                logging.info(f'Destination: {deck} (Position: {position})')
                return (self.game.deck[deck], position)

    @ staticmethod
    def splitter(item, delimiter):
        if delimiter in item:
            return tuple(item.split(delimiter))
        else:
            return (item, 'None')

    def update_cardpool(self):
        logging.info(f'Updating cardpool')
        if self.game.deck['draw'].is_empty():
            self.view.cardpool.show_empty()
        else:
            deck = self.game.deck['draw'].cards[-1-self.cardpool_index]
            self.view.cardpool.show(deck.name, self.cardpool_index+1, deck)

    def update_pool_selector(self):
        logging.info(f'Updating pool selector')
        for i in range(self.view.top_cards):
            if i < len(self.game.deck['draw']):
                c = self.game.deck['draw'].cards[-1-i]
                text = f'{len(c)}' if len(c) > 1 else c.cards[0].name
                btn = self.view.pool_selector.button[i]
                btn.setEnabled(True)
                btn.set_text(text)
                if not btn.is_connected():
                    btn.clicked.connect(
                        lambda index=i: self.cb_select_cardpool(index))
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
        logging.info(f'Updating epidemic menu')
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
        logging.info('Updating stats')
        self.view.stats.show(self.game.stats)

    def cb_select_cardpool(self, index):
        logging.info(f'Selecting cardpool {index}')
        self.cardpool_index = index

    def cb_new_game_dialog(self):
        logging.info('Displaying new game dialog')
        games = list(self.game.games.keys())
        dialog = DialogNewGame(games)
        if dialog.exec_():
            self.game.initialise(dialog.combo.currentText())
            self.view.initialise()
            self.populate_draw()
            self.update_gui()
            self.cb_select_cardpool(0)
        else:
            logging.debug(f'Quitting')
            if not self.view.has_initialised:
                # QApplication.quit() doesn't quit immediately
                # Hide the main window and delay quitting slightly
                self.view.hide()
                QTimer.singleShot(100, QApplication.quit)

    def cb_epidemic(self):
        """Shuffle epidemic card based on the selected card in the combobox."""
        logging.info('Starting epidemic')
        new_card_name = self.view.epidemic_menu.combo_box.currentText()
        self.game.epidemic(new_card_name)
        self.view.deck['discard'].clear()
        self.populate_draw()
        self.update_gui()
        self.cb_select_cardpool(0)

    @ staticmethod
    def cb_help_dialog():
        logging.info('Displaying help dialog')
        """Callback from the Help button.
        Displays a dialog with the option to view Help in browser."""
        dialog = DialogHelp()
        if dialog.exec_():
            webopen('https://github.com/Merkwurdichliebe/Epidemic/wiki')

    def update_gui(self):
        logging.info(f'Updating GUI')
        self.update_pool_selector()
        self.update_epidemic_menu()
        self.update_stats()


def main():
    application = QApplication()
    view = MainWindow()
    model = Game()
    app = App(model, view)
    view.show()
    application.exec_()


if __name__ == '__main__':
    main()
