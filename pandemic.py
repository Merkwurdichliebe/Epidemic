#!/usr/bin/env python

"""
PANDEMIC TRACKER is designed to assist in evaluating card draw probabilities
in the board game Pandemic. It is my first attempt at a working project
using Tkinter for the GUI.
"""

__author__ = "Tal Zana"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "0.7"

# TODO undo

from pandemictk import MainWindow
from pandemicdeck import Card, Deck, DrawDeck
from collections import Counter

# A list of all the cards available in the deck, including exiled ones
# but excluding permanently destroyed cards.
# The city name is followed by the number of copies of that card,
# and its family color.
# "Hollow Men" are green for no particular reason.

available_cards = [
    ('Jacksonville', 3, 'yellow'),
    ('Lagos', 3, 'yellow'),
    ('Le Caire', 3, 'black'),
    ('Londres', 3, 'blue'),
    ('New York', 3, 'blue'),
    ('Sao Paolo', 3, 'yellow'),
    ('Washington', 3, 'blue'),
    ('Bogota', 2, 'yellow'),
    ('Buenos Aires', 2, 'yellow'),
    ('Paris', 2, 'blue'),
    ('Francfort', 2, 'blue'),
    ('Atlanta', 1, 'blue'),
    ('Lima', 1, 'yellow'),
    ('Moscou', 1, 'black'),
    ('Los Angeles', 1, 'yellow'),
    ('San Francisco', 2, 'blue'),
    ('Denver', 2, 'blue'),
    ('Baghdad', 2, 'black'),
    ('Kinshasa', 1, 'yellow'),
    ('Khartoum', 1, 'yellow'),
    ('Johannesbourg', 2, 'blue'),
    ('Saint-Pétersbourg', 1, 'blue'),
    ('Santiago', 1, 'yellow'),
    ('Mexico', 1, 'yellow'),
    ('Tripoli', 3, 'black'),
    ('Chicago', 2, 'blue'),
    ('Hommes creux', 4, 'green')
]


class Stats:
    def __init__(self, deck):
        self.deck = deck
        self.total = 0
        self.in_discard = 0
        self.top_freq = 0
        self.top_cards = None
        self.percentage = 0
        self.update()

    def update(self):
        self.total = len(self.deck['discard'].cards) + len(self.deck['draw'].cards[0].cards)
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

    # Initialize the starter deck from the available cards list
    starter_deck = Deck('starter')
    for card in available_cards:
        c = Card(card[0], card[2])
        for i in range(card[1]):
            starter_deck.add(c)

    # Initialize the draw deck
    draw = DrawDeck('draw')
    draw.add(starter_deck)

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


def main():
    """Main program entry point."""
    decks = initialize()
    app = App(decks)
    app.view.root.mainloop()


if __name__ == '__main__':
    main()
