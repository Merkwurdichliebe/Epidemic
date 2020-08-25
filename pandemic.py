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

from collections import Counter
import tkinter as tk
from tkinter import ttk


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


class App:
    def __init__(self, root, decks):
        """Main application designed as class in order to allow easier communication
        between interface elements. cf. http://thinkingtkinter.sourceforge.net
        """

        # Main Tk window

        self.root = root
        self.root.title('Pandemic Deck Tracker')
        self.root.configure(padx=20, pady=10)
        self.root.resizable(False, False)

        # Replace default menu

        emptyMenu = tk.Menu(root)
        self.root.config(menu=emptyMenu)

        # Define GUI variables and set defaults

        self.destination_choice = tk.StringVar()
        self.destination_choice.set('exile')

        self.epidemic_choice = tk.StringVar()

        # Keep track of added buttons so we can destroy and redraw them later

        self.cardpool_buttons = []
        self.draw_buttons = []
        self.discard_buttons = []

        # Styles

        FONT_H0 = ('Helvetica', 30, 'bold')
        FONT_H1 = ('Helvetica', 14, 'bold')
        FONT_TEXT = ('Helvetica', 14)

        # We use ttk buttons because macOS doesn't color Tk buttons properly

        ttk.Style().configure('green.TButton', foreground='green', background='black')
        ttk.Style().configure('blue.TButton', foreground='blue', background='black')
        ttk.Style().configure('yellow.TButton', foreground='orange', background='red')
        ttk.Style().configure('black.TButton', foreground='black', background='black')

        # Window header

        self.frm_header = tk.Frame(root)
        self.frm_header.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.frm_header_title = tk.Frame(self.frm_header)
        self.frm_header_title.pack(fill=tk.BOTH, expand=1)

        # Logo

        self.img_logo = tk.PhotoImage(file='pandemic-logo.png')
        self.lbl_logo = tk.Label(self.frm_header_title, image=self.img_logo)
        self.lbl_logo.pack(side=tk.LEFT)

        # Title

        self.label_title = tk.Label(self.frm_header_title, text='DECK TRACKER', padx=10, font=FONT_H0)
        self.label_title.pack(side=tk.LEFT)

        self.frm_header_line = tk.Frame(self.frm_header)
        self.frm_header_line.pack(fill=tk.X)

        self.canvas = tk.Canvas(self.frm_header_line, height=10)
        self.canvas.create_line(10, 10, 2000, 10)
        self.canvas.pack(fill=tk.X)

        # Main GUI frames

        self.frm_main = tk.Frame(root)
        self.frm_main.pack()

        self.frm_cardpool = tk.Frame(self.frm_main, padx=10)
        self.frm_cardpool.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_draw_deck = tk.Frame(self.frm_main, padx=10)
        self.frm_draw_deck.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_draw_card = tk.Frame(self.frm_main, padx=10)
        self.frm_draw_card.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_discard = tk.Frame(self.frm_main, padx=10)
        self.frm_discard.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_exile = tk.Frame(self.frm_main, padx=10)
        self.frm_exile.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_menu = tk.Frame(self.frm_main, padx=10)
        self.frm_menu.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_bottom = tk.Frame(root, pady=20)
        self.frm_bottom.pack(side=tk.LEFT)

        # Top labels above the main interface

        self.lbl1 = tk.Label(self.frm_cardpool, pady=10, text='POSSIBLE CARDS', width=20, font=FONT_H1)
        self.lbl1.pack()

        self.lbl2 = tk.Label(self.frm_draw_deck, pady=10, text='DRAW DECK', width=20, font=FONT_H1)
        self.lbl2.pack()

        self.lbl3 = tk.Label(self.frm_draw_card, pady=10, text='DRAW CARD', width=20, font=FONT_H1)
        self.lbl3.pack()

        self.lbl4 = tk.Label(self.frm_discard, pady=10, text='DISCARD DECK', width=20, font=FONT_H1)
        self.lbl4.pack()

        self.lbl5 = tk.Label(self.frm_exile, pady=10, text='ABANDONED or EXILED', width=20, font=FONT_H1)
        self.lbl5.pack()

        self.lbl6 = tk.Label(self.frm_menu, pady=10, text='Card destination', font=FONT_H1)
        self.lbl6.pack()

        # Bottom Text

        self.lbl7 = tk.Label(self.frm_bottom, pady=10, text='© 2020 Tal Zana', font=FONT_H1)
        self.lbl7.pack()

        # Two textboxes containing the dynamically built lists
        # for the exile deck and the cardpool deck

        self.txt_cardpool = tk.Text(self.frm_cardpool, name='txt_cardpool', width=20, height=50, font=FONT_TEXT)
        self.txt_cardpool.pack()

        self.txt_exile = tk.Text(self.frm_exile, name='txt_exile', width=20, height=50, font=FONT_TEXT)
        self.txt_exile.pack()

        # Radio buttons

        self.frm_radio = tk.Frame(self.frm_menu, pady=10)
        self.frm_radio.pack()

        radio_draw_to_discard = tk.Radiobutton(
            self.frm_radio,
            width=15,
            text='Discard',
            variable=self.destination_choice,
            value='discard',
            anchor=tk.W,
            padx=10

        )
        radio_draw_to_exile = tk.Radiobutton(
            self.frm_radio,
            width=15,
            text='Exile',
            variable=self.destination_choice,
            value='exile',
            anchor=tk.W,
            padx=10

        )
        radio_draw_to_draw = tk.Radiobutton(
            self.frm_radio,
            width=15,
            text='Draw',
            variable=self.destination_choice,
            value='draw',
            anchor=tk.W,
            padx=10
        )

        radio_draw_to_discard.pack(anchor=tk.W)
        radio_draw_to_exile.pack(anchor=tk.W)
        radio_draw_to_draw.pack(anchor=tk.W)

        # Dropdown menu for selecting city in epidemic

        self.frm_epidemic = tk.Frame(self.frm_menu)
        self.frm_epidemic.pack()

        self.lbl_epidemic = tk.Label(self.frm_menu, pady=20, text='Epidemic', font=FONT_H1)
        self.lbl_epidemic.pack()

        self.dropdown_epidemic_options = []
        self.dropdown_epidemic = tk.OptionMenu(self.frm_menu, self.epidemic_choice, self.dropdown_epidemic_options)
        self.dropdown_epidemic.config(width=15)
        self.dropdown_epidemic.pack()

        btn_epidemic = ttk.Button(self.frm_menu, text='Shuffle as epidemic', width=15, command=self.cb_epidemic)
        btn_epidemic.pack()

        # Stats

        self.frm_stats = tk.Frame(self.frm_menu, pady=10)
        self.frm_stats.pack()

        self.lbl_stats = tk.Label(self.frm_stats, pady=10, text='Stats', font=FONT_H1)
        self.lbl_stats.pack()

        self.txt_stats = tk.Text(self.frm_stats, width=20, font=FONT_TEXT, wrap=tk.WORD)
        self.txt_stats.pack()

        # btn_quit = ttk.Button(self.frm_menu, text='Quit', width=15, command=self.cb_quit)
        # btn_quit.pack()

        # Initialize a few general attributes

        # Build the deck dictionary

        self.deck = {}
        for deck in decks:
            self.deck[deck.name] = deck

        # Index of the cardpool to display when a Draw Deck item is clicked

        self.cardpool_index = 0

        # Fixed total of all the cards in the Draw Deck

        self.cards_total = len(self.deck['draw'].cards[0].cards)

        # Tuple to hold three values for displaying the top card frequency

        self.top_frequency_cards = ()

        # Update initial GUI

        self.update_gui(self.deck['exile'])
        self.update_gui(self.deck['cardpool'])
        self.update_gui(self.deck['draw'])
        self.update_gui(self.deck['discard'])

    def update_gui(self, deck):

        # We only update the GUI elements that need updating
        # based on the deck that is passed to the method.

        if deck.name == 'exile':
            self.update_textbox(self.txt_exile, self.deck['exile'])

        if deck.name == 'cardpool':
            self.update_textbox(self.txt_cardpool, self.deck['draw'].cards[-1 - self.cardpool_index])

        if deck.name == 'draw':
            for button in self.draw_buttons:
                button.destroy()

            for button in self.cardpool_buttons:
                button.destroy()

            for index, card_list in enumerate(reversed(deck.cards[-16:])):
                if len(card_list.cards) == 1:
                    button_text = card_list.cards[0].city
                    color = card_list.cards[0].color + '.TButton'
                else:
                    button_text = f'{len(card_list.cards)}'
                    color = 'black.TButton'
                button = ttk.Button(
                    self.frm_draw_deck,
                    style=color,
                    width=15,
                    text=button_text
                )
                button.configure(command=lambda x=index: self.cb_view_cardpool(x))
                button.pack()
                self.cardpool_buttons.append(button)

            for index, card in enumerate(sorted(set(deck.cards[-1].cards), key=lambda x: x.city)):
                button = ttk.Button(self.frm_draw_card, style=card.color + '.TButton', width=15, text=card.city)
                button.configure(command=lambda x=deck, y=card: self.cb_draw_card(x, y))
                button.pack()
                self.draw_buttons.append(button)

            self.update_dropdown(deck)
            self.calculate_probabilities()
            self.update_textbox_stats()

        if deck.name == 'discard':
            for button in self.discard_buttons:
                button.destroy()

            for index, card in enumerate(sorted(deck.cards, key=lambda x: x.city)):
                button = ttk.Button(
                    self.frm_discard,
                    style=card.color + '.TButton',
                    width=15,
                    text=card.city
                )
                button.configure(command=lambda x=deck, y=card: self.cb_draw_card(x, y))
                button.pack()
                self.discard_buttons.append(button)

    @staticmethod
    def update_textbox(textbox, deck):
        # Method is static because it doesn't need the self keyword,
        # it only updates the contents of the Tk textbox which is passed to it.
        textbox.configure(state=tk.NORMAL)
        textbox.delete(1.0, tk.END)
        for card in sorted(deck.cards, key=lambda x: x.city):
            textbox.insert(tk.END, card.city + '\n')
        textbox.configure(state=tk.DISABLED)

    def update_textbox_stats(self):
        self.txt_stats.configure(state=tk.NORMAL)
        self.txt_stats.delete(1.0, tk.END)
        self.txt_stats.insert(tk.END, f'Total cards: {self.cards_total}\n')
        self.txt_stats.insert(tk.END, f'In discard pile: {str(len(self.deck["discard"].cards))}\n')
        self.txt_stats.insert(tk.END, self.top_frequency_cards_to_text())
        self.txt_stats.configure(state=tk.DISABLED)

    def update_dropdown(self, deck):
        # Update the epidemic dropdown list based on the available cards in the Draw Deck.
        unique_cards = sorted([card.city for card in list(set(deck.cards[0].cards))])
        self.dropdown_epidemic_options = unique_cards
        m = self.dropdown_epidemic.children['menu']
        m.delete(0, tk.END)
        for card in unique_cards:
            # command value syntax is from
            # https://stackoverflow.com/questions/28412496/updating-optionmenu-from-list
            m.add_command(label=card, command=lambda value=card: self.epidemic_choice.set(value))
        self.epidemic_choice.set(unique_cards[0])

    def cb_view_cardpool(self, index):
        # Callback from the buttons used to display the possible choices in the Draw Deck.
        # Outputs the possible cards in each potential draw.
        self.cardpool_index = index
        self.update_gui(self.deck['cardpool'])

    def cb_draw_card(self, deck, card):
        # Move a card from a deck to the destination deck set by the radio buttons
        # Ignore drawing from a deck onto itself
        destination = self.deck[self.destination_choice.get()]
        if not deck == destination:
            deck.move(card, destination)
            self.cardpool_index = 0
            self.update_gui(self.deck['discard'])
            self.update_gui(self.deck['exile'])
            self.update_gui(self.deck['cardpool'])
            self.update_gui(self.deck['draw'])

    def calculate_probabilities(self):
        # Get the total number of cards
        card_list = self.deck['draw'].cards[-1].cards
        total_potential_cards = len(card_list)

        # Use a Counter to sort the cards by the most common ones
        c = Counter(card_list).most_common()

        # Get the frequency of the most common card
        top_frequency = c[0][1]

        # Build a list of all the cards that share that top frequency
        top_cards = [card[0] for card in c if card[1] == top_frequency]
        self.top_frequency_cards = (top_frequency, top_cards, total_potential_cards)

    def top_frequency_cards_to_text(self):
        text = f'\nTop card frequency:\n'
        text += str(self.top_frequency_cards[0]) + ' '
        text += f'({self.top_frequency_cards[0] / self.top_frequency_cards[2] :.2%})'
        text += '\n\n'
        for card in self.top_frequency_cards[1]:
            text += '- ' + card.city + '\n'
        return text

    def cb_epidemic(self):
        # Select card from bottom of draw pile based on the dropdown list
        new_card = self.deck['draw'].get_card_by_name(self.epidemic_choice.get())
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
        self.cardpool_index = 0

        # Update the GUI.
        self.update_gui(self.deck['draw'])
        self.update_gui(self.deck['discard'])
        self.update_gui(self.deck['cardpool'])


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
    root = tk.Tk()
    App(root, decks)
    root.mainloop()


if __name__ == '__main__':
    main()
