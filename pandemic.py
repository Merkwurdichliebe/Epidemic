#!/usr/bin/env python

"""
PANDEMIC TRACKER is designed to assist in evaluating card draw probabilities
in the board game Pandemic. It is my first attempt at a working project
using Tkinter for the GUI.
"""

__author__ = "Tal Zana"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "0.5"

# TODO undo

from pandemictk import MainWindow
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


class Card:
    """Basic class to represent a card with a city name and color.
    Cards are contained in Decks."""

    def __init__(self, city, color):
        self.city = city
        self.color = color


class Deck:
    """Basic class to define a deck of Card objects, which are held in a simple list.
    There are three main decks in the game:
    - Draw Deck
    - Discard Deck
    - Exile Deck"""

    def __init__(self, name):
        self.name = name
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

    def move(self, card, to_deck):
        self.remove(card)
        to_deck.add(card)

    def get_card_by_name(self, name):
        if isinstance(self, DrawDeck):
            list = self.cards[0].cards
        else:
            list = self.cards
        found_card = next((card for card in list if card.city == name), None)
        assert found_card is not None, f'Card with name "{name}" not found in Deck "{self.name}".'
        return found_card

    def clear(self):
        self.cards = []


class DrawDeck(Deck):
    """Subclass of Deck used for the Draw Deck only.
    The Draw Deck doesn't hold Card objects, but a list of Decks objects,
    which represent the potential cards for each draw."""

    def __init__(self, name):
        Deck.__init__(self, name)

    def add(self, item):
        # Add a card to the Draw Deck.If we're adding a single card to the Draw Deck
        # we need to make a Deck out of it, containing a single card.
        if isinstance(item, Deck):
            for i in item.cards:
                self.cards.append(item)
        else:
            new_deck = Deck(item.city)
            new_deck.add(item)
            self.cards.append(new_deck)

    def remove(self, item):
        # Override the Deck.remove method so that the card is removed
        # from the list at the top of the deck,
        # i.e. the last element in the list."""
        if isinstance(item, Deck):
            self.remove(item)
        else:
            self.cards[-1].remove(item)
            self.cards.pop()

    def remove_from_bottom(self, card):
        # Remove a card from the bottom of the draw deck,
        # i.e. from list position 0,
        # then remove the list item entirely because the card was drawn.
        self.cards[0].remove(card)
        self.cards.pop(0)


class Stats:
    def __init__(self, deck):
        self.deck = deck
        self.cards_total = 0
        self.in_discard = 0
        self.top_frequency = 0
        self.top_cards = None
        self.potential_cards_total = 0
        self.percentage = 0
        self.update()

    def update(self):
        self.cards_total = len(self.deck['discard'].cards) + len(self.deck['draw'].cards[0].cards)
        self.in_discard = len(self.deck['discard'].cards)

        # Calculate draw probabilities
        card_list = self.deck['draw'].cards[-1].cards
        self.potential_cards_total = len(card_list)

        # Use a Counter to sort the cards by the most common ones
        c = Counter(card_list).most_common()

        # Get the frequency of the most common card
        self.top_frequency = c[0][1]
        self.percentage = self.top_frequency / self.potential_cards_total

        # Build a list of all the cards that share that top frequency
        self.top_cards = [card[0] for card in c if card[1] == self.top_frequency]


class App:
    def __init__(self, decks):
        self.decks = decks

        # Build the deck dictionary

        self.deck = {}
        for deck in decks:
            self.deck[deck.name] = deck

        # Tuple to hold three values of the top Draw Deck card frequency

        self.top_frequency_cards = ()

        self.stats = Stats(self.deck)

        # We don't assign the class to a variable since we are not using it later,
        # we only instantiate the window.
        self.view = MainWindow(self, self.deck)
        self.updateview()

    def updateview(self):
        self.view.update_stats(self.stats)

    def cb_epidemic(self):
        # self.do_epidemic()
        pass

    def do_epidemic(self):
        # Select card from bottom of draw pile based on the dropdown list
        new_card = self.deck['draw'].get_card_by_name(self.view.get_epidemic_choice())
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

        # We reset the index to 0 so that the card pool textbox displays
        # the top item in the Draw Deck.
        # self.cardpool_index = 0

        # Update the GUI.
        # self.update_gui(self.deck['draw'])
        # self.update_gui(self.deck['discard'])
        # self.update_gui(self.deck['cardpool'])




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
