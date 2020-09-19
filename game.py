# Epidemic modules
from decks import Card, Deck, DrawDeck
from stats import Stats
import utility

# Other modules
from copy import deepcopy
import yaml


class Game:
    def __init__(self):
        self.games = self.read_decks_from_file()
        self.deck = None
        self.stats = None

    def initialise(self, game):
        """Prepare the initial state for the game. Initialise all decks.
        This is run once at the start of every game."""

        # Create a list with the Draw Deck and the 3 other empty decks
        game_decks = [self.initialise_draw_deck(game),
                      Deck('discard'),
                      Deck('exclude'),
                      Deck('cardpool')]

        # Build the decks dictionary so we can get a Deck object by its name
        self.deck = {deck.name: deck for deck in game_decks}

        # Get a Stats object for calculating draw probabilities
        self.stats = Stats(self.deck)

    def initialise_draw_deck(self, game):
        # Initialise the draw deck
        d = DrawDeck('draw')
        # We use deepcopy to get a new copy of the deck
        # from the games variable, which stores all possible game types.
        d.add(deepcopy(self.games[game]))
        return d

    def draw(self, from_deck, to_deck, card):
        # Move a card from a source deck to a destination deck.
        # Ignore drawing from a deck onto itself.
        if not from_deck == to_deck:
            from_deck.move(card, to_deck)

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
        new_cards = Deck('epidemic')
        for card in self.deck['discard'].cards.copy():
            new_cards.add(card)

        self.deck['draw'].add(new_cards)

        # Clear the discard pile
        self.deck['discard'].clear()

    def read_decks_from_file(self):
        # Initialize the initial deck from the card list in cards.yml
        game = {}
        file = utility.get_path('data/cards.yml')

        # Read the cards.yml file
        try:
            with open(file, encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            print(f'Missing or damaged cards.yml configuration file\n({e})')

        try:
            for game_title in data.keys():
                game[game_title] = self.create_deck(game_title, data)
        except ValueError:
            # Raise the error again to stop execution
            raise

        return game

    @staticmethod
    def create_deck(game_title, data):
        deck = Deck(game_title)
        for item in data[game_title]:
            if item['color'] not in Card.valid_colors:
                raise ValueError(f"Invalid color '{item['color']}' in "
                                 f"'{game_title} : {item['name']}'")
            else:
                card = Card(item['name'], item['color'])
                for i in range(item['count']):
                    deck.add(card)
        return deck
