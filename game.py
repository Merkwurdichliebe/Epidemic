from decks import Card, Deck, DrawDeck
from collections import Counter
from copy import deepcopy
import utility
import yaml


class Stats:
    def __init__(self, deck):
        self.deck = deck
        self.total = 0
        self.in_discard = 0
        self.top_freq = 0
        self.top_cards = None
        self.percentage = 0
        # Cards total should only be updated on object creation
        self.total = len(self.deck['discard'].cards) + \
                     len(self.deck['draw'].cards[0].cards)
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


class Game:
    def __init__(self):
        self.games = self.read_decks_on_file()
        self.decks = None
        self.deck = None
        self.stats = None

    def init(self, game):
        """Prepare the initial state for the game. Initialise all decks.
        This is run once at the start of every game."""

        # Initialise the draw deck:
        # We use deepcopy to get a new copy of the deck
        # from the games variable, which stores all possible game types.
        drawdeck = DrawDeck('draw')
        drawdeck.add(deepcopy(self.games[game]))

        # Create a list with the Draw Deck and the 3 other empty decks
        self.decks = [drawdeck,
                      Deck('discard'),
                      Deck('exclude'),
                      Deck('cardpool')]

        # Build the decks dictionary so we can get a Deck object by its name
        self.deck = {deck.name: deck for deck in self.decks}

        # Get a Stats object for calculating draw probabilities
        self.stats = Stats(self.deck)

    def draw(self, from_deck, to_deck, card):
        # Move a card from a source deck to a destination deck.
        # Ignore drawing from a deck onto itself.
        if not from_deck == to_deck:
            from_deck.move(card, to_deck)
        self.stats.update()

    def epidemic(self, card):
        """Do the epidemic shuffle phase: draw a card from the bottom
        of the Draw Deck, discard it and shuffle the discard pile back
        onto the top of the Draw Deck."""
        new_card = self.deck['draw'].get_card_by_name(card)
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
        self.stats.update()

    @staticmethod
    def read_decks_on_file():
        # Initialize the initial deck from the card list in cards.yml
        game = {}
        file = utility.get_path('data/cards.yml')
        valid_colors = ['blue', 'yellow', 'black', 'green', 'red']

        # Read the cards.yml file
        try:
            with open(file, encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            print(f'Missing or damaged cards.yml configuration file\n({e})')

        # Check for valid card colors
        try:
            for game_item in data.keys():
                deck = Deck(game_item)
                for item in data[game_item]:
                    if item['color'] not in valid_colors:
                        raise ValueError(f"Invalid color: {item}")
                    card = Card(item['name'], item['color'])
                    for i in range(item['count']):
                        deck.add(card)
                game[game_item] = deck
        except ValueError:
            # Raise the error again to stop execution
            raise

        return game