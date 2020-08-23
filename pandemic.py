#!/usr/bin/env python

"""
PANDEMIC TRACKER is designed to assist in evaluating card draw probabilities in the board game Pandemic.
It is my first attempt at a working project using Tkinter for the GUI.
"""

__author__ = "Tal Zana"
__copyright__ = "Copyright 2020"
__license__ = "GPL"
__version__ = "0.1"

# TODO réorganiser 8 cartes
# TODO draw 2, 3, 4 et 5 par épidémie
# TODO undo
# TODO affichage probabilités

import tkinter as tk
from tkinter import ttk
import logging

logging.basicConfig(level=logging.DEBUG)

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
    ('[ Hommes creux ]', 4, 'green')
]


class Card:
    """Class to define a card with city name and color."""

    def __init__(self, city, color):
        self.city = city
        self.color = color


class Deck:
    """Basic class to define a deck of Card objects,
    which are held in a simple list."""

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

    def populate(self, cards):
        for card in cards:
            c = Card(card[0], card[2])
            for i in range(card[1]):
                self.add(c)
        return self

    def get_card_by_name(self, name):
        for card in self.cards:
            if card.city == name:
                return card
        return None

    def clear(self):
        self.cards = []


class DrawDeck(Deck):
    """Subclass of Deck used for the Draw Deck only,
    which holds a list of decks, as potential cards for each draw."""

    def __init__(self, name):
        Deck.__init__(self, name)

    def add(self, item):
        if isinstance(item, Deck):
            for i in item.cards:
                self.cards.append(item)
        else:
            newpool = Deck(item.city)
            newpool.add(item)
            self.cards.append(newpool)

    # Override the Deck.remove method so that the card is removed
    # from the list at the top of the deck,
    # i.e. the last element in the list.
    def remove(self, item):
        if isinstance(item, Deck):
            logging.info(f'{item} is a Deck. Removing.')
            self.remove(item)
        else:
            logging.info(f'{item} is a Card. Removing.')
            self.cards[-1].remove(item)
            self.cards.pop()

    def move(self, card, to_deck):
        self.remove(card)
        to_deck.add(card)

    def remove_from_bottom(self, card):
        """
        Remove a card from the bottom of the draw deck,
        i.e. from list position 0,
        then remove the list item entirely because the card was drawn.
        """
        logging.info(f'REMOVE_FROM_BOTTOM : Removing card from bottom : {card}.')
        self.cards[0].remove(card)
        self.cards.pop(0)

    def get_card_by_name(self, name):
        for card in self.cards[0].cards:
            if card.city == name:
                return card
        return None

    def __repr__(self):
        text = f'DRAW DECK NAME: {self.name}\n'
        text += '--------------------\n'
        for deck in self.cards:
            text += f'({len(deck.cards)})'
        return text


class App:
    def __init__(self, root, decks):

        # Main window

        self.root = root
        self.root.title('Pandemic Deck Tracker')
        self.root.configure(padx=20, pady=10)
        self.root.resizable(False, False)

        # Build the deck dictionary

        self.deck = {}
        for deck in decks:
            self.deck[deck.name] = deck

        # GUI variables

        self.destination = tk.StringVar()
        self.destination.set('exile')

        # Index of the cardpool to display when a Draw Deck item is clicked

        self.cardpool_index = 0

        # Keep track of added buttons so we can destroy and redraw them later

        self.cardpool_buttons = []
        self.draw_buttons = []
        self.discard_buttons = []

        # Styles

        FONT_H0 = ('Helvetica', 28, 'bold')
        FONT_H1 = ('Helvetica', 14, 'bold')
        FONT_TEXT = ('Helvetica', 14)

        ttk.Style().configure('green.TButton', foreground='green', background='black')
        ttk.Style().configure('blue.TButton', foreground='blue', background='black')
        ttk.Style().configure('yellow.TButton', foreground='orange', background='red')
        ttk.Style().configure('black.TButton', foreground='black', background='black')

        # Window header

        self.frm_header = tk.Frame(root, bg='red')
        self.frm_header.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.frm_header_title = tk.Frame(self.frm_header)
        self.frm_header_title.pack(fill=tk.BOTH, expand=1)

        self.label_title = tk.Label(self.frm_header_title, text='PANDEMIC TRACKER', font=FONT_H0)
        self.label_title.pack(side=tk.LEFT)

        self.frm_header_line = tk.Frame(self.frm_header)
        self.frm_header_line.pack(fill=tk.X)

        self.canvas = tk.Canvas(self.frm_header_line, height=10)
        self.canvas.create_line(10, 10, 2000, 10)
        self.canvas.pack(fill=tk.X)

        # Main GUI frames

        self.frm_cardpool = tk.Frame(root, name='frm_cardpool', padx=10)
        self.frm_cardpool.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_draw_deck = tk.Frame(root, name='frm_draw_deck', padx=10)
        self.frm_draw_deck.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_draw_card = tk.Frame(root, name='frm_draw_card', padx=10)
        self.frm_draw_card.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_discard = tk.Frame(root, name='frm_discard', padx=10)
        self.frm_discard.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_exile = tk.Frame(root, name='frm_exile', padx=10)
        self.frm_exile.pack(side=tk.LEFT, anchor=tk.N)

        self.frm_menu = tk.Frame(root, name='frm_menu', padx=10)
        self.frm_menu.pack(side=tk.LEFT, anchor=tk.N)

        # Top labels above the main interface

        self.lbl1 = tk.Label(self.frm_cardpool, pady=10, text='POSSIBLE CARDS', font=FONT_H1)
        self.lbl1.pack()

        self.lbl2 = tk.Label(self.frm_draw_deck, pady=10, text='DRAW DECK', font=FONT_H1)
        self.lbl2.pack()

        self.lbl3 = tk.Label(self.frm_draw_card, pady=10, text='DRAW CARD', font=FONT_H1)
        self.lbl3.pack()

        self.lbl4 = tk.Label(self.frm_discard, pady=10, text='DISCARD DECK', font=FONT_H1)
        self.lbl4.pack()

        self.lbl5 = tk.Label(self.frm_exile, pady=10, text='ABANDONED or EXILED', font=FONT_H1)
        self.lbl5.pack()

        self.lbl6 = tk.Label(self.frm_menu, pady=10, text='Card destination', font=FONT_H1)
        self.lbl6.pack()

        # Two textboxes containing the dynamically built lists
        # for the exile deck and the cardpool deck

        # TODO Disable on start

        self.txt_cardpool = tk.Text(self.frm_cardpool, name='txt_cardpool', width=20, height=50, font=FONT_TEXT)
        self.txt_cardpool.pack()

        self.txt_exile = tk.Text(self.frm_exile, name='txt_exile', width=20, height=50, font=FONT_TEXT)
        self.txt_exile.pack()

        # Radio buttons

        radio_draw_to_discard = tk.Radiobutton(
            self.frm_menu,
            indicatoron=0,
            width=15,
            text='Discard',
            variable=self.destination,
            value='discard',

        )
        radio_draw_to_exile = tk.Radiobutton(
            self.frm_menu,
            indicatoron=0,
            width=15,
            text='Exile',
            variable=self.destination,
            value='exile'
        )
        radio_draw_to_draw = tk.Radiobutton(
            self.frm_menu,
            indicatoron=0,
            width=15,
            text='Draw',
            variable=self.destination,
            value='draw'
        )

        radio_draw_to_discard.pack(anchor=tk.W)
        radio_draw_to_exile.pack(anchor=tk.W)
        radio_draw_to_draw.pack(anchor=tk.W)

        # Dropdown menu for selecting city in epidemic

        self.dropdown_epidemic = ttk.Combobox(self.frm_menu, width=15)
        self.dropdown_epidemic.pack()

        # Buttons

        btn_epidemic = ttk.Button(self.frm_menu, text='Epidemic', width=15, command=self.cb_epidemic)
        btn_epidemic.pack()

        btn_quit = ttk.Button(self.frm_menu, text='Quit', width=15, command=self.cb_quit)
        btn_quit.pack()

        # Update initial GUI

        self.update_gui(self.deck['exile'])
        self.update_gui(self.deck['cardpool'])
        self.update_gui(self.deck['draw'])
        self.update_gui(self.deck['discard'])

    def update_gui(self, deck):

        logging.info(f'GUI upate : size of Deck "{deck.name}" is {len(deck.cards)}')

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
        textbox.configure(state=tk.NORMAL)
        textbox.delete(1.0, tk.END)
        for card in sorted(deck.cards, key=lambda x: x.city):
            textbox.insert(tk.END, card.city + '\n')
        textbox.configure(state=tk.DISABLED)

    def update_dropdown(self, deck):
        unique_cards = sorted([card.city for card in list(set(deck.cards[0].cards))])
        self.dropdown_epidemic.configure(values=unique_cards)
        self.dropdown_epidemic.current(0)
        self.dropdown_epidemic.bind('<<ComboboxSelected>>',
                                    lambda e: print(f'UPDATE_DROPDOWN : {self.dropdown_epidemic.get()}'))

    def cb_view_cardpool(self, index):
        logging.info(f'CB_VIEW_CARDPOOL : index = {index}')
        self.cardpool_index = index
        self.update_gui(self.deck['cardpool'])

    def cb_draw_card(self, deck, card):
        # Draw a card from a deck to the destination set by the radio buttons
        # Ignore drawing from a deck onto itself
        if not deck == self.deck[self.destination.get()]:
            deck.move(card, self.deck[self.destination.get()])
            self.cardpool_index = 0
            self.update_gui(self.deck['draw'])
            self.update_gui(self.deck['discard'])
            self.update_gui(self.deck['exile'])
            self.update_gui(self.deck['cardpool'])

    def cb_epidemic(self):

        # Select card from bottom of draw pile
        new_card = self.deck['draw'].get_card_by_name(self.dropdown_epidemic.get())
        self.deck['draw'].remove_from_bottom(new_card)

        # Add card to discard pile
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

        self.cardpool_index = 0
        self.update_gui(self.deck['draw'])
        self.update_gui(self.deck['discard'])
        self.update_gui(self.deck['cardpool'])

    def cb_quit(self):
        self.root.destroy()


def initialize():
    """Prepare the initial states for all the decks.
    This is run once at the start of the game."""
    logging.info('Initiazing.')

    # Initialize the starter deck from the available cards list
    starter_deck = Deck('starter').populate(available_cards)

    # Initialize the draw deck
    draw = DrawDeck('draw')
    draw.add(starter_deck)
    logging.info('Draw Deck done.')

    # Initialize the discard and exile decks
    discard = Deck('discard')
    exile = Deck('exile')
    cardpool = Deck('cardpool')
    logging.info('Other decks done.')

    # Draw the 4 "Hollow Men" cards from the draw deck
    # onto the discard pile
    for i in range(4):
        draw.move(draw.get_card_by_name('[ Hommes creux ]'), discard)
    logging.info('Hollow men drawn.')

    logging.info('Initialize done.')
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
