# draw card to zone de fin de partie pour villes abandonnées
# réorganiser 8 cartes

# draw 2, 3, 4 et 5 par épidémie
# gérer cartes HC
# undo
# affichage probabilités
# gérer erreur frappe
# refresh dropdown after epidemic

import tkinter as tk
from tkinter import ttk


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
    '''Class to define a card with city name and color.'''
    def __init__(self, city, color):
        self.city = city
        self.color = color

    # Used in an earlier console version, this makes 'print(card)'
    # return the colored name of the city instead of the card object.
    def __repr__(self):
        s = self.city
        return s


class Deck:
    '''Basic class to define a deck of Card objects,
    which are held in a simple list.'''
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

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

    def __repr__(self):
        text = f'DECK NAME: {self.name}\n'
        text += '--------------------\n'
        for card in self.cards:
            text += card.city + '\n'
        return text


class DrawDeck(Deck):
    '''Subclass of Deck used for the Draw Deck only,
    which holds a list of lists.'''
    def __init__(self, name):
        Deck.__init__(self, name)

    def add(self, cardpool):
        for i in range(len(cardpool)):
            self.cards.append(cardpool)

    def remove(self, card):
        self.cards[-1].remove(card)

    def __repr__(self):
        text = f'DRAW DECK NAME: {self.name}\n'
        text += '--------------------\n'
        for cardpool in self.cards:
            text += f'({len(cardpool)})'
        return text



# Initialize the start deck
starter_deck = Deck('starter').populate(available_cards)

draw_deck = DrawDeck('draw')
draw_deck.add(starter_deck.cards)

print(draw_deck)



# for i in range(4):
#     card = get_card_by_name(draw[-1], '[ Hommes creux ]')
#     if card is not None:
#         draw_card(card, draw[-1], discard)

"""
# Initialize Tkinter window
root = tk.Tk()
root.title('Pandemic Deck Tracker')
root.configure(padx=20, pady=10)

ttk.Style().configure('green.TButton', foreground='green', background='black')
ttk.Style().configure('blue.TButton', foreground='blue', background='black')
ttk.Style().configure('yellow.TButton', foreground='orange', background='red')
ttk.Style().configure('black.TButton', foreground='black', background='black')

# Frames

frame_pool = tk.Frame(root, padx=10)
frame_pool.grid(row=0, column=0, sticky='n')

frame_draw_deck = tk.Frame(root, padx=10)
frame_draw_deck.grid(row=0, column=1, sticky='n')

frame_draw_card = tk.Frame(root, padx=10)
frame_draw_card.grid(row=0, column=2, sticky='n')

frame_discard = tk.Frame(root, padx=10)
frame_discard.grid(row=0, column=3, sticky='n')

frame_exile = tk.Frame(root, padx=10)
frame_exile.grid(row=0, column=4, sticky='n')

frame_menu = tk.Frame(root, padx=10)
frame_menu.grid(row=0, column=5, sticky='n')

# Top 5 labels above the main interface

font_heading = ('Helvetica', 14, 'bold')

label_top_1 = tk.Label(frame_pool, pady=10, text='POSSIBLE CARDS', font=font_heading)
label_top_1.pack()

label_top_2 = tk.Label(frame_draw_deck, pady=10, text='DRAW DECK', font=font_heading)
label_top_2.pack()

label_top_3 = tk.Label(frame_draw_card, pady=10, text='DRAW CARD', font=font_heading)
label_top_3.pack()

label_top_4 = tk.Label(frame_discard, pady=10, text='DISCARD DECK', font=font_heading)
label_top_4.pack()

label_top_5 = tk.Label(frame_exile, pady=10, text='ABANDONED or EXILED', font=font_heading)
label_top_5.pack()

label_top_6 = tk.Label(frame_menu, pady=10, text='Card destination', font=font_heading)
label_top_6.pack()

# Two textboxes containing the dynamically built lists
# for the exile deck and the draw deck

textbox_draw_deck = tk.Text(frame_pool, width=20, height=50, font=("Helvetica", 14))
textbox_draw_deck.pack()

textbox_exile_deck = tk.Text(frame_exile, width=20, height=50, font=("Helvetica", 14))
textbox_exile_deck.pack()

# Radio buttons

radio_button_draw_destination = tk.StringVar()
radio_button_draw_destination.set('exile')

radio_button_draw_to_discard = tk.Radiobutton(
    frame_menu,
    text='Discard',
    variable=radio_button_draw_destination,
    value='discard',

    )
radio_button_draw_to_exile = tk.Radiobutton(
    frame_menu,
    text='Exile',
    variable=radio_button_draw_destination,
    value='exile'
    )
radio_button_draw_to_draw = tk.Radiobutton(
    frame_menu,
    text='Draw',
    variable=radio_button_draw_destination,
    value='draw'
    )

radio_button_draw_to_discard.pack(anchor='w')
radio_button_draw_to_exile.pack(anchor='w')
radio_button_draw_to_draw.pack(anchor='w')


# Dropdown menu for selecting city in epidemic

dropdown_epidemic = ttk.Combobox(frame_menu, width=15)
dropdown_epidemic.pack()

# Dictionaries to hold dynamically-built buttons
# Format is {Tk Button Object : Index}
# We need them because buttons can't be dynamically assigned parameters
# to send to the callback function, so we send the button itself instead

draw_options_buttons = {}
draw_card_buttons = {}
discard_card_buttons = {}


def get_card_by_name(cards, name):
    for card in cards:
        if card.city == name:
            return card
    return None


def draw_card(card, from_deck, to_deck):
    from_deck.remove(card)
    if to_deck == draw:
        item = [card]
    else:
        item = card
    to_deck.append(item)


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
    if radio_button_draw_destination.get() == 'exile':
        destination = exile
    elif radio_button_draw_destination.get() == 'discard':
        destination = discard

    draw_card(sorted(set(draw[-1]), key=lambda x: x.city)[button_index], draw[-1], destination)
    draw.pop()
    update_gui()
    list_draw_options(0)

def discard_card_button_cb(button):
    button_index = discard_card_buttons[button]
    if radio_button_draw_destination.get() == 'exile':
        destination = exile
    elif radio_button_draw_destination.get() == 'draw':
        destination = draw
    draw_card(sorted(discard, key=lambda x: x.city)[button_index], discard, destination)
    update_gui()

def update_gui():
    for k in draw_card_buttons.keys():
        k.destroy()

    for k in draw_options_buttons.keys():
        k.destroy()

    for k in discard_card_buttons.keys():
        k.destroy()

    # Discard

    for index, card in enumerate(sorted(discard, key=lambda x: x.city)):
        button = ttk.Button(
            frame_discard,
            style=card.color+'.TButton',
            width=15,
            text=card.city,
            command=quit
            )
        button.configure(command=lambda b=button: discard_card_button_cb(b))
        button.pack()
        discard_card_buttons[button] = index

    # Exile

    textbox_exile_deck.configure(state=tk.NORMAL)
    textbox_exile_deck.delete(1.0, tk.END)
    for card in sorted(exile, key=lambda x: x.city):
        textbox_exile_deck.insert(tk.END, card.city + '\n')
    textbox_exile_deck.configure(state=tk.DISABLED)

    # Draw options

    for index, card_list in enumerate(reversed(draw[-16:])):
        if len(card_list) == 1:
            button_text = card_list[0].city
        else:
            button_text = f'{len(card_list)}'
        button = ttk.Button(
            frame_draw_deck,
            width=15,
            text=button_text
            )
        button.configure(command=lambda b=button: draw_deck_button_cb(b))
        button.pack()
        draw_options_buttons[button] = index

    # Draw deck

    for index, card in enumerate(sorted(set(draw[-1]), key=lambda x: x.city)):
        button = ttk.Button(frame_draw_card, style=card.color+'.TButton', width=15, text=card.city)
        button.configure(command=lambda b=button: draw_card_button_cb(b))
        button.pack()
        draw_card_buttons[button] = index

    # Epidemic

    unique_cards = sorted([card.city for card in list(set(draw[0]))])
    dropdown_epidemic.configure(values=unique_cards)
    dropdown_epidemic.bind('<<ComboboxSelected>>', lambda e: print(dropdown_epidemic.get()))








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
exile = []






update_gui()

b_Quit = ttk.Button(frame_menu, text='Quit', width=15, command=quit)
b_Epidemic = ttk.Button(frame_menu, text='Epidemic', width=15, command=do_epidemic)

b_Epidemic.pack()
b_Quit.pack()

root.mainloop()
"""