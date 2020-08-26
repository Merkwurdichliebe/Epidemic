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