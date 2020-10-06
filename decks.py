#!/usr/bin/env python

"""
Classes used in the Epidemic application
for representing Card objects and Deck objects.

The DrawDeck object extends Deck and holds other Decks, not Cards.
Each of these Decks represents the possible draws at each position
in the DrawDeck. The top card is the last Card in the list.
"""

import logging
logger = logging.getLogger(__name__)


class Card:
    """Basic class to represent a card with a city name and color.
    Cards are referenced in Decks."""

    valid_colors = ['blue', 'yellow', 'black', 'green', 'red']

    def __init__(self, name, color):
        self.name = name
        assert color in Card.valid_colors, f'Invalid color: {color}'
        self.color = color


class Deck:
    """Defines a list Card objects.
    There are three decks in the game:
    - Discard Deck
    - Exile Deck
    - Draw Deck (special case, subclassed below)"""

    def __init__(self, name):
        self.name = name
        self.cards = []
        self.parent = None  # References parent Draw Deck if applicable

    def add(self, card, **kwargs):
        """Add a card to the Deck."""
        self.cards.append(card)

    def remove(self, card):
        """Remove a card from the Deck."""
        assert card in self.cards, f'{card.name} not in {self.name}'
        self.cards.remove(card)

    def move(self, card, to_deck, **kwargs):
        """Move a card from one Deck to another.
        **kwargs are used to denote position in the deck
        when a card is added to the Draw Deck."""
        self.remove(card)
        to_deck.add(card, **kwargs)

    def clear(self):
        self.cards.clear()

    def sorted(self):
        return sorted(self.cards, key=lambda x: x.name)

    def is_empty(self):
        return False if self.cards else True

    def has_parent(self):
        return True if self.parent else False

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)


class DrawDeck(Deck):
    """Subclass of Deck used for the Draw Deck only.
    The Draw Deck doesn't hold Card objects, but a list of Decks objects,
    which represent the potential cards for each draw."""

    def __init__(self, name):
        super().__init__(name)

    def add(self, item, **kwargs):
        # Override Deck.add.
        # If the added item is a Deck (i.e. after an epidemic),
        # add as many copies of it as the number of cards it contains.
        if isinstance(item, Deck):
            for i in item.cards:
                self.cards.append(item)
            item.parent = self
        # If the added item is a Card,
        # add it to the Deck at the required position
        # and insert an instance of the Deck at that position.
        else:
            pos = kwargs['position']
            assert pos != 'deck', f'Invalid Draw Deck destination'
            deck = None

            if self.is_empty() or pos == 'single':
                deck = Deck('Single card')
            elif pos == 'top':
                deck = self.top()
            elif pos == 'bottom':
                deck = self.bottom()

            deck.add(item)

            if pos == 'bottom':
                self.cards.insert(0, deck)
            else:
                self.cards.append(deck)

            assert deck is not None, f'Invalid Draw Deck state'
            deck.parent = self

    def remove(self, card):
        # Override Deck.remove:
        # Remove the card from the top of the deck
        # so that it's excluded from future possible draws,
        # then removes the Deck itself from the Draw Deck.
        self.top().remove(card)
        self.cards.pop()

    def get_card_from_bottom(self, name):
        list = self.bottom().cards
        found = next((card for card in list if card.name == name), None)
        assert found is not None,\
            f'Card with name "{name}" not found in Deck "{self.name}".'
        return found

    def remove_from_bottom(self, card):
        # Remove a card from the bottom of the draw deck,
        # i.e. from list position 0,
        # then remove the list item entirely because the card was drawn.
        self.bottom().remove(card)
        self.cards.pop(0)

    def sorted(self):
        # Override Deck.sorted to return
        # a sorted list of unique possible cards
        # at the top (last) position in the Deck.
        return sorted(set(self.cards[-1].cards), key=lambda x: x.name)

    def top(self):
        return self.cards[-1]

    def bottom(self):
        return self.cards[0]
