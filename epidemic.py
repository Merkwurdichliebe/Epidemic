#!/usr/bin/env python

"""
EPIDEMIC is designed to assist in evaluating card draw probabilities
in the board game Pandemic. It is my first attempt at a working project
using Tkinter for the GUI.
"""

__author__ = "Tal Zana"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "0.7"

# TODO undo
# TODO fr, en
# TODO parse YML import for empty file or wrong colors

from epidemictk import MainWindow
from epidemicdeck import Card, Deck, DrawDeck
from collections import Counter
import yaml
import os
import platform
import utility


class Stats:
    def __init__(self, deck):
        self.deck = deck
        self.total = 0
        self.in_discard = 0
        self.top_freq = 0
        self.top_cards = None
        self.percentage = 0
        # Cards total should only be updated on object creation
        self.total = len(self.deck['discard'].cards) + len(self.deck['draw'].cards[0].cards)
        self.update()

    def update(self):
        self.in_discard = len(self.deck['discard'].cards)

        # Calculate draw probabilities
        card_list = self.deck['draw'].cards[-1].cards

        # Use a Counter to sort the cards by the most common ones
        c = Counter(card_list).most_common()

        # Get the frequency of the most common card
        self.top_freq = c[0][1]
        self.percentage = self.top_freq / len(card_list)

        # Build a list of all the cards that share that top frequency
        self.top_cards = [card[0] for card in c if card[1] == self.top_freq]


class App:
    def __init__(self, decks):
        # Build the decks dictionary so we can get a Deck object by its name
        self.deck = {deck.name: deck for deck in decks}

        # Get a Stats object for calculating draw probabilities
        self.stats = Stats(self.deck)

        # Instantiate the main window
        self.view = MainWindow(self)
        self.updateview()

    # TODO Fix this, be careful with cb_view_cardpool
    def updateview(self):
        self.stats.update()
        for deck in self.deck:
            self.view.update_gui(self.deck[deck])
        self.view.update_stats(self.stats)
        self.view.update_dropdown()

    def cb_draw_card(self, deck, card):
        # Move a card from a deck to the destination deck set by the radio buttons
        # Ignore drawing from a deck onto itself
        dest = self.deck[self.view.get_destination()]
        if not deck == dest:
            deck.move(card, dest)
            self.updateview()

    def cb_epidemic(self):
        # Select card from bottom of draw pile based on the dropdown list
        new_card = self.deck['draw'].get_card_by_name(self.view.get_epidemic())
        self.deck['draw'].remove_from_bottom(new_card)

        # Add the card to the discard pile
        self.deck['discard'].add(new_card)

        # Create new card pool
        # We use copy in order to reset the discard pile
        # without affecting the newly pooled cards
        new_pool = Deck('pool')
        for card in self.deck['discard'].cards.copy():
            new_pool.add(card)

        self.deck['draw'].add(new_pool)

        # Clear the discard pile
        self.deck['discard'].clear()

        self.updateview()


def initialize():
    """Prepare the initial states for all the decks.
    This is run once at the start of the game."""

    # Initialize the draw deck
    draw = DrawDeck('draw')
    draw.add(get_initial_deck())

    # Initialize the discard and exile decks
    discard = Deck('discard')
    exile = Deck('exile')
    cardpool = Deck('cardpool')

    # Draw the 4 "Hollow Men" cards from the draw deck
    # onto the discard pile
    for i in range(4):
        draw.move(draw.get_card_by_name('Hommes creux'), discard)

    # Return the prepared decks
    return [draw, discard, exile, cardpool]


def get_initial_deck():
    # Initialize the initial deck from the available cards list in cards.yml
    # file = os.path.realpath('data/cards.yml')
    # file = NSBundle.mainBundle().pathForResource_ofType_("data/cards", "yml")
    file = utility.get_path('data/cards.yml')
    init_deck = Deck('Starter Deck')
    valid_colors = ['blue', 'yellow', 'black', 'green']

    # Read the cards.yml file
    try:
        with open(file, encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        print(f'Missing or damaged cards.yml configuration file\n({e})')

    # Check for valid card colors
    try:
        for item in data:
            if item['color'] not in valid_colors:
                raise ValueError(f"Invalid color specified in cards.yml for card: {item}")
            card = Card(item['name'], item['color'])
            for i in range(item['count']):
                init_deck.add(card)
    except ValueError:
        # Raise the error again to stop execution after displaying the Exception
        raise

    return init_deck


def main():
    """Main program entry point."""
    try:
        decks = initialize()
        app = App(decks)
        app.view.root.mainloop()
    except Exception as e:
        with open("/tmp/epidebug.log", 'w') as f:
            f.write(f"Error {e}")
    else:
        with open("/tmp/epidebug.log", 'w') as f:
            f.write(f"No errors")


if __name__ == '__main__':
    main()

# Error 'ascii' codec can't decode byte 0xc3 in position 1202: ordinal not in range(128)%