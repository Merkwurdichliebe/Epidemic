# draw card to zone de fin de partie pour villes abandonnées
# réorganiser 8 cartes
# draw 2, 3, 4 et 5 par épidémie
# gérer cartes HC
# undo
# affichage probabilités
# gérer erreur frappe
# select abandoned cities
# refresh dropdown after epidemic
# colors (remove colorama)

from colorama import Fore, Back, Style
from enum import Enum
import tkinter as tk
from tkinter import ttk


class Color(Enum):
    YELLOW = Fore.BLACK + Back.YELLOW
    BLUE = Fore.WHITE + Back.LIGHTBLUE_EX
    BLACK = Fore.BLACK + Back.LIGHTWHITE_EX
    GREEN = Fore.BLACK + Back.GREEN


CARDS = [
    ('Jacksonville', 3, Color.YELLOW),
    ('Lagos', 3, Color.YELLOW),
    ('Le Caire', 3, Color.BLACK),
    ('Londres', 3, Color.BLUE),
    ('New York', 3, Color.BLUE),
    ('Sao Paolo', 3, Color.YELLOW),
    ('Washington', 3, Color.BLUE),
    ('Bogota', 2, Color.YELLOW),
    ('Buenos Aires', 2, Color.YELLOW),
    ('Paris', 2, Color.BLUE),
    ('Francfort', 2, Color.BLUE),
    ('Atlanta', 1, Color.BLUE),
    ('Lima', 1, Color.YELLOW),
    ('Moscou', 1, Color.BLACK),
    ('Los Angeles', 1, Color.YELLOW),
    ('San Francisco', 2, Color.BLUE),
    ('Denver', 2, Color.BLUE),
    ('Baghdad', 2, Color.BLACK),
    ('Kinshasa', 1, Color.YELLOW),
    ('Khartoum', 1, Color.YELLOW),
    ('Johannesbourg', 2, Color.BLUE),
    ('Saint-Pétersbourg', 1, Color.BLUE'),
    ('Santiago', 1, Color.YELLOW),
    ('[ Hommes creux ]', 4, Color.GREEN)
]

# ('Mexico', 1, Color.YELLOW),
# ('Tripoli', 3, Color.BLACK),
# ('Chicago', 2, Color.BLUE),


class Card:
    '''Class to define a card with city name and color.'''
    def __init__(self, city, color):
        self.city = city
        self.color = color

    # Used in an earlier console version, this makes 'print(card)'
    # return the colored name of the city instead of the card object.
    def __repr__(self):
        s = self.color.value + ' ' + self.city + ' ' + Style.RESET_ALL
        return s


# Initialize Tkinter window

root = tk.Tk()
root.title('Pandemic Deck Tracker')
root.configure(padx=20, pady=10)

# Top 5 labels above the main interface

label_top_1 = tk.Label(root, pady=10, text='POSSIBLE CARDS')
label_top_1.grid(row=0, column=0, sticky=tk.N)

label_top_2 = tk.Label(root, pady=10, text='DRAW DECK')
label_top_2.grid(row=0, column=1, sticky=tk.N)

label_top_3 = tk.Label(root, pady=10, text='DRAW CARD')
label_top_3.grid(row=0, column=2, sticky=tk.N)

label_top_4 = tk.Label(root, pady=10, text='DISCARD DECK')
label_top_4.grid(row=0, column=3, sticky=tk.N)

# Two textboxes containing the dynamically built lists
# for the discard deck and the draw deck

textbox_discard_deck = tk.Text(root, width=20, height=50, font=("Helvetica", 14))
textbox_discard_deck.grid(row=1, column=3, rowspan=200, sticky=tk.N)

textbox_draw_deck = tk.Text(root, width=20, height=50, font=("Helvetica", 14))
textbox_draw_deck.grid(row=1, column=0, rowspan=200, sticky=tk.N)

# Dropdown menu for selecting city in epidemic

dropdown_epidemic = ttk.Combobox(root, width=15)

# Dictionaries to hold dynamically-built buttons
# Format is {Tk Button Object : Index}
# We need them because buttons can't be dynamically assigned parameters
# to send to the callback function, so we send the button itself instead

draw_options_buttons = {}
draw_card_buttons = {}


def get_card_by_name(cards, name):
    for card in cards:
        if card.city == name:
            return card
    return None


def draw_card(card):
    discard.append(card)
    draw[-1].remove(card)
    draw.pop()
    update_gui()


def draw_deck_button_cb(button):
	button_index = draw_options_buttons[button]
	list_draw_options(button_index)


def list_draw_options(index):
	textbox_draw_deck.configure(state=tk.NORMAL)
	textbox_draw_deck.delete(1.0, tk.END)
	for card in sorted(draw[-1-index], key=lambda x: x.city):
		textbox_draw_deck.insert(tk.END, card.city + '\n')
	textbox_draw_deck.configure(state=tk.DISABLED)


def draw_card_button_cb(button):
	button_index = draw_card_buttons[button]
	draw_card(sorted(set(draw[-1]), key=lambda x: x.city)[button_index])
	list_draw_options(0)


def update_gui():
	for k in draw_card_buttons.keys():
		k.destroy()

	for k in draw_options_buttons.keys():
		k.destroy()

	textbox_discard_deck.configure(state=tk.NORMAL)
	textbox_discard_deck.delete(1.0, tk.END)
	for card in sorted(discard, key=lambda x: x.city):
		textbox_discard_deck.insert(tk.END, card.city + '\n')
	textbox_discard_deck.configure(state=tk.DISABLED)

	for index, card_list in enumerate(reversed(draw[-16:])):
		button_text = f'{len(card_list)}'
		button = ttk.Button(root, width=15, text=button_text, command=quit)
		button.configure(command=lambda b=button: draw_deck_button_cb(b))
		button.grid(row=1 + index, column=1)
		draw_options_buttons[button] = index

	for index, card in enumerate(sorted(set(draw[-1]), key=lambda x: x.city)):
		button = ttk.Button(root, width=15, text=card.city, command=quit)
		button.configure(command=lambda b=button: draw_card_button_cb(b))
		button.grid(row=1 + index, column=2)
		draw_card_buttons[button] = index

	unique_cards = sorted([card.city for card in list(set(draw[0]))])

	dropdown_epidemic.configure(values=unique_cards)
	dropdown_epidemic.bind('<<ComboboxSelected>>', lambda e: print(dropdown_epidemic.get()))
	dropdown_epidemic.grid(column=4, row=1)


def new_pool(cards):
    pools.append(cards)
    for i in range(len(cards)):
        draw.append(pools[len(pools) - 1])


def initialize_deck():
    deck = []
    for card in CARDS:
        c = Card(card[0], card[2])
        for i in range(card[1]):
            deck.append(c)
    return deck


def do_epidemic():
	# Select card from bottom of draw pile
	
	new_card = get_card_by_name(draw[0], dropdown_epidemic.get())
	draw[0].remove(new_card)
	draw.pop(0)

	# Add card to discard pile
	discard.append(new_card)

	# Create new card pool
	# We use copy in order to reset the discard pile
	# without affecting the newly pooled cards
	new_pool(discard.copy())

	# Clear the discard pile
	discard.clear()

	update_gui()


discard = []
draw = []
pools = []


# Initialize the start deck
new_pool(initialize_deck())
for i in range(4):
    card = get_card_by_name(draw[-1], '[ Hommes creux ]')
    if card is not None:
    	draw_card(card)

update_gui()

b_Quit = ttk.Button(root, text='Quit', width=15, command=quit)
b_Epidemic = ttk.Button(root, text='Epidemic', width=15, command=do_epidemic)

b_Epidemic.grid(column=4, row=2)
b_Quit.grid(column=4, row=3)

root.mainloop()