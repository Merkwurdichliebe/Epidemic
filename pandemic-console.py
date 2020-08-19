# draw card to zone de fin de partie pour villes abandonnées
# réorganiser 8 cartes
# draw 2, 3, 4 et 5 par épidémie
# gérer cartes hommes creux
# undo
# affichage probabilités
# gérer erreur frappe
# synthétiser liste couleurs


from colorama import Fore, Back, Style
from enum import Enum


class Color(Enum):
    YELLOW = Fore.BLACK + Back.YELLOW
    BLUE = Fore.WHITE + Back.LIGHTBLUE_EX
    BLACK = Fore.BLACK + Back.LIGHTWHITE_EX


KNOWN = {
    'Jacksonville': 3,
    'Lagos': 3,
    'Le Caire': 3,
    'Londres': 3,
    'New York': 3,
    'Sao Paolo': 3,
    'Tripoli': 3,
    'Washington': 3,
    'Bogota': 2,
    'Buenos Aires': 2,
    'Chicago': 2,
    'Paris': 2,
    'Francfort': 2,
    'Atlanta': 1,
    'Lima': 1,
    'Moscou': 1,
    'Los Angeles': 1,
    'San Francisco': 2,
    'Mexico': 1,
    'Denver': 2,
    'Baghdad': 2
}


CONTINENTS = {
    'Jacksonville': Color.YELLOW,
    'Lagos': Color.YELLOW,
    'Le Caire': Color.BLACK,
    'Londres': Color.BLUE,
    'New York': Color.BLUE,
    'Sao Paolo': Color.YELLOW,
    'Tripoli': Color.BLACK,
    'Washington': Color.BLUE,
    'Bogota': Color.YELLOW,
    'Buenos Aires': Color.YELLOW,
    'Chicago': Color.BLUE,
    'Paris': Color.BLUE,
    'Francfort': Color.BLUE,
    'Atlanta': Color.BLUE,
    'Lima': Color.YELLOW,
    'Moscou': Color.BLACK,
    'Los Angeles': Color.YELLOW,
    'San Francisco': Color.BLUE,
    'Mexico': Color.YELLOW,
    'Denver': Color.BLUE,
    'Baghdad': Color.BLACK
}

tab = '\t' * 5


class Card:
    def __init__(self, city):
        self.city = city

    def __repr__(self):
        # print(CONTINENTS[self.city])
        s = CONTINENTS[self.city].value + ' ' + self.city + ' ' + Style.RESET_ALL
        return s


def get_card_by_name(cards, name):
    for card in cards:
        if card.city == name:
            return cards.pop(cards.index(card))
    return None


def draw_card(card):
    discard.append(card)
    draw.pop()


def select_card(cards):

    # Create a list of unique cards
    # Sort it by the card's city name
    unique_cards = [card for card in list(set(cards))]
    unique_cards.sort(key=lambda x: x.city)

    # Print the city list to choose from
    print('\n')
    for card in unique_cards:
        print(f'\t{unique_cards.index(card)}\t{card}')

    # Get user selection
    sel = -1
    while sel < 0 or sel > len(unique_cards):
        sel = int(input('\n\tCARD TO DRAW: '))

    # Return the selected card
    name = unique_cards[sel].city
    return get_card_by_name(cards, name)


def print_decks():

    # Print discard pile
    print(f'\n{tab}DISCARD PILE ({len(discard)} cards)\n')

    for card in discard:
        print(f'{tab}{card}')

    # Print draw pile
    print(f'\n{tab}DRAW PILE ({len(draw)} cards)\n')

    # Count backward 16 cards from end (top) of draw pile
    for i in range(len(draw)-1, len(draw)-17, -1):
        if len(draw[i]) > 10:
            dr = f'{len(draw[i])} cards'
        else:
            dr = draw[i]

        print(f'{i}{tab}{dr}')
    print(f'{tab}--------')
    print(f'{tab}{len(draw)} CARDS')


def new_pool(cards):
    pools.append(cards)
    for i in range(len(cards)):
        draw.append(pools[len(pools) - 1])


def initialize_deck():
    deck = []
    for k, v in KNOWN.items():
        c = Card(k)
        for i in range(v):
            deck.append(c)
    return deck


def do_epidemic():
    # Select card from bottom of draw pile
    new_card = select_card(draw[0])
    draw.pop(0)

    # Add card to discard pile
    discard.append(new_card)

    # Create new card pool
    # We use copy in order to reset the discard pile
    # without affecting the newly pooled cards
    new_pool(discard.copy())

    # Clear the discard pile
    discard.clear()


def show_menu():
    options = {
        'd': 'Draw a card',
        'e': 'Epidemic',
        'l': 'List decks',
        'q': 'Quit'
    }
    print('\n\t\tMENU\n\t\t----')
    for k, v in options.items():
        print(f'\t\t{k} : {v}')
    selection = input('\n\t\t>')
    if selection == 'd':
        card = select_card(draw[-1])
        draw_card(card)
        print_decks()
    if selection == 'e':
        do_epidemic()
    if selection == 'l':
        print_decks()
    if selection == 'q':
        return True


discard = []
draw = []
pools = []


# Initialize the start deck

new_pool(initialize_deck())


# Main loop

stop = False
while not stop:
    stop = show_menu()