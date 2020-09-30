#!/usr/bin/env python

"""
Classes used in the Epidemic application
for representing Card objects and Deck objects.

The DrawDeck object extends Deck and actually holds Decks, not Cards.
Each of these Decks represents the possible draws at each position
in the DrawDeck. The top card is always the last Card in the list.
"""
# TODO replace if isinstance(self, DrawDeck): with property


class Card:
    """Basic class to represent a card with a city name and color.
    Cards are grouped in Decks."""

    valid_colors = ['blue', 'yellow', 'black', 'green', 'red']

    def __init__(self, name, color):
        self.name = name
        assert color in Card.valid_colors, f'Invalid color: {color}'
        self.color = color


class Deck:
    """Basic class to define a deck of Card objects,
    which are held in a simple list.
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
            list = self.bottom().cards
        else:
            list = self.cards
        found = next((card for card in list if card.name == name), None)
        assert found is not None,\
            f'Card with name "{name}" not found in Deck "{self.name}".'
        return found

    def clear(self):
        self.cards.clear()

    def sorted(self):
        return sorted(self.cards, key=lambda x: x.name)

    def is_empty(self):
        return False if self.cards else True

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)


class DrawDeck(Deck):
    """Subclass of Deck used for the Draw Deck only.
    The Draw Deck doesn't hold Card objects, but a list of Decks objects,
    which represent the potential cards for each draw."""

    def __init__(self, name):
        Deck.__init__(self, name)

    def add(self, item):
        # Override Deck.add. This method adds a card to the Draw Deck.
        # If we're adding a single card to the Draw Deck
        # we need to make a Deck out of it, containing a single card,
        # which is why we are checking the item's class.
        if isinstance(item, Deck):
            for i in item.cards:
                self.cards.append(item)
        else:
            deck = Deck(item.name)
            deck.add(item)
            self.cards.append(deck)

    def remove(self, card):
        # Override Deck.remove:
        # Remove the card from the top of the deck
        # so that it's excluded from future possible draws,
        # then removes the Deck itself from the Draw Deck.
        self.top().remove(card)
        self.cards.pop()

    def remove_from_bottom(self, card):
        # Remove a card from the bottom of the draw deck,
        # i.e. from list position 0,
        # then remove the list item entirely because the card was drawn.
        self.bottom().remove(card)
        self.cards.pop(0)

    def sorted(self):
        # We override Deck.sorted because we are only interested
        # in a sorted list of unique possible cards
        # from the Deck at the top (last) position
        return sorted(set(self.cards[-1].cards), key=lambda x: x.name)

    def top(self):
        return self.cards[-1]

    def bottom(self):
        return self.cards[0]

