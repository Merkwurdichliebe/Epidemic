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

    def draw(self, card, to_deck):
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

    def __repr__(self):
        text = f'\n\nDECK NAME: {self.name}\n'
        text += '--------------------\n'
        for card in self.cards:
            text += card.city + '\n'
        text += '\n\n'
        return text


class DrawDeck(Deck):
    '''Subclass of Deck used for the Draw Deck only,
    which holds a list of decks, as potential cards for each draw.'''
    def __init__(self, name):
        Deck.__init__(self, name)


    def add(self, cardpool):
        for i in range(len(cardpool)):
            self.cards.append(cardpool)


    # Override the Deck.remove method so that the card is removed
    # from the list at the top of the deck,
    # i.e. the last element in the list.
    def remove(self, card):
        self.cards[-1].remove(card)


    # Remove a card from the bottom of the draw deck,
    # i.e. from list position 0,
    # then remove the list entirely because the card was drawn.
    def remove_from_bottom(self, card):
        self.cards[0].remove(card)
        self.cards.pop[0]


    def get_card_by_name(self, name):
        for card in self.cards[-1]:
            if card.city == name:
                return card
        return None


    def __repr__(self):
        text = f'DRAW DECK NAME: {self.name}\n'
        text += '--------------------\n'
        for cardpool in self.cards:
            text += f'({len(cardpool)})'
        return text


def gui_build():
    # Initialize Tkinter window
    root = tk.Tk()
    root.title('Pandemic Deck Tracker')
    root.configure(padx=20, pady=10)

    ttk.Style().configure('green.TButton', foreground='green', background='black')
    ttk.Style().configure('blue.TButton', foreground='blue', background='black')
    ttk.Style().configure('yellow.TButton', foreground='orange', background='red')
    ttk.Style().configure('black.TButton', foreground='black', background='black')

    # Frames

    frame_cardpool = tk.Frame(root, name='frame_cardpool', padx=10)
    frame_cardpool.pack(side=tk.LEFT, anchor=tk.N)

    frame_draw_deck = tk.Frame(root, name='frame_draw_deck', padx=10)
    frame_draw_deck.pack(side=tk.LEFT, anchor=tk.N)

    frame_draw_card = tk.Frame(root, name='frame_draw_card', padx=10)
    frame_draw_card.pack(side=tk.LEFT, anchor=tk.N)

    frame_discard = tk.Frame(root, name='frame_discard', padx=10)
    frame_discard.pack(side=tk.LEFT, anchor=tk.N)

    frame_exile = tk.Frame(root, name='frame_exile', padx=10)
    frame_exile.pack(side=tk.LEFT, anchor=tk.N)

    frame_menu = tk.Frame(root, name='frame_menu', padx=10)
    frame_menu.pack(side=tk.LEFT, anchor=tk.N)

    # Top 5 labels above the main interface

    font_heading = ('Helvetica', 14, 'bold')

    label_top_1 = tk.Label(frame_cardpool, pady=10, text='POSSIBLE CARDS', font=font_heading)
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
    # for the exile deck and the cardpool deck

    textbox_cardpool = tk.Text(frame_cardpool, name='textbox_cardpool', width=20, height=50, font=("Helvetica", 14))
    textbox_cardpool.pack()

    textbox_exile = tk.Text(frame_exile, name='textbox_exile', width=20, height=50, font=("Helvetica", 14))
    textbox_exile.pack()

    # Radio buttons

    radio_button_draw_destination = tk.StringVar()
    radio_button_draw_destination.set('exile')

    radio_button_draw_to_discard = tk.Radiobutton(
        frame_menu,
        indicatoron = 0,
        width=15,
        text='Discard',
        variable=radio_button_draw_destination,
        value='discard',

        )
    radio_button_draw_to_exile = tk.Radiobutton(
        frame_menu,
        indicatoron = 0,
        width=15,
        text='Exile',
        variable=radio_button_draw_destination,
        value='exile'
        )
    radio_button_draw_to_draw = tk.Radiobutton(
        frame_menu,
        indicatoron = 0,
        width=15,
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

    return root


# Dictionaries to hold dynamically-built buttons
# Format is {Tk Button Object : Index}
# We need them because buttons can't be dynamically assigned parameters
# to send to the callback function, so we send the button itself instead

draw_options_buttons = {}
draw_card_buttons = {}
discard_card_buttons = {}


def draw_deck_button_cb(button):
    window = button.winfo_toplevel()
    button_index = draw_options_buttons[button]
    update_gui(window, deck)


def draw_card_button_cb(button):
    pass
    # button_index = draw_card_buttons[button]
    # if radio_button_draw_destination.get() == 'exile':
    #     destination = table['exile']
    # elif radio_button_draw_destination.get() == 'discard':
    #     destination = table['discard']

    # destination = table['discard']
    # deck = table['draw']
    # deck.draw(sorted(set(draw.cards[-1]), key=lambda x: x.city)[button_index], destination)
    # # draw.cards.pop()
    # update_gui()

def discard_card_button_cb(button):
    button_index = discard_card_buttons[button]
    if radio_button_draw_destination.get() == 'exile':
        destination = exile
    elif radio_button_draw_destination.get() == 'draw':
        destination = draw
    draw_card(sorted(discard, key=lambda x: x.city)[button_index], discard, destination)
    update_gui()

def button_cb(button):
    pass

def update_gui(window, deck):

    def update_textbox(textbox, list):

        textbox.configure(state=tk.NORMAL)
        textbox.delete(1.0, tk.END)
        for card in sorted(list, key=lambda x: x.city):
            textbox.insert(tk.END, card.city + '\n')
        textbox.configure(state=tk.DISABLED)

    # dest = window.nametowidget('frame_discard')
    # destination = radio_button_draw_destination.get()
    
    # Update discard deck
    if deck.name == 'discard':

        frame = window.nametowidget('frame_discard')

        for k in discard_card_buttons.keys():
            k.destroy()

        for index, card in enumerate(sorted(deck.cards, key=lambda x: x.city)):
            button = ttk.Button(
                frame,
                style=card.color+'.TButton',
                width=15,
                text=card.city
                )
            button.configure(command=lambda b=button: discard_card_button_cb(b))
            button.pack()
            discard_card_buttons[button] = index


    # Update exile deck
    if deck.name == 'exile':
        textbox = window.nametowidget('frame_exile').nametowidget('textbox_exile')
        update_textbox(textbox, deck.cards)


    # Update draw deck
    if deck.name == 'draw':

        frame = window.nametowidget('frame_draw_deck')

        for k in draw_card_buttons.keys():
            k.destroy()

        for k in draw_options_buttons.keys():
            k.destroy()
        for index, card_list in enumerate(reversed(deck.cards[-16:])):
            if len(card_list) == 1:
                button_text = card_list[0].city
            else:
                button_text = f'{len(card_list)}'
            button = ttk.Button(
                frame,
                width=15,
                text=button_text
                )
            button.configure(command=lambda b=button: draw_deck_button_cb(b))
            button.pack()
            draw_options_buttons[button] = index

        # Update draw card button list

        frame = window.nametowidget('frame_draw_card')

        for index, card in enumerate(sorted(set(deck.cards[-1]), key=lambda x: x.city)):
            button = ttk.Button(frame, style=card.color+'.TButton', width=15, text=card.city)
            button.configure(command=lambda x=card: draw_card_button_cb(x))
            button.pack()
            draw_card_buttons[button] = index

        # Update cardpool

        textbox = window.nametowidget('frame_cardpool').nametowidget('textbox_cardpool')
        update_textbox(textbox, deck.cards[-1-index])

    # Epidemic

    # unique_cards = sorted([card.city for card in list(set(deck.cards[0]))])
    # dropdown_epidemic.configure(values=unique_cards)
    # dropdown_epidemic.bind('<<ComboboxSelected>>', lambda e: print(dropdown_epidemic.get()))


def do_epidemic():
    # Select card from bottom of draw pile
    
    new_card = get_card_by_name(draw.cards[0], dropdown_epidemic.get())
    draw.cards[0].remove(new_card)
    draw.cards.pop(0)

    # Add card to discard pile
    discard.append(new_card)

    # Create new card pool
    # We use copy in order to reset the discard pile
    # without affecting the newly pooled cards
    new_pool(discard.copy())

    # Clear the discard pile
    discard.clear()

    update_gui()


def initialize():
    '''Prepare the initial states for all the decks.
    This is run once at the start of the game.'''

    # Initialize the starter deck from the available cards list
    starter_deck = Deck('starter').populate(available_cards)

    # Initialize the draw deck
    draw = DrawDeck('draw')
    draw.add(starter_deck.cards)

    # Initialize the discard and exile decks
    discard = Deck('discard')
    exile = Deck('exile')

    # Draw the 4 "Hollow Men" cards from the draw deck
    # onto the discard pile
    for i in range(4):
        draw.draw(draw.get_card_by_name('[ Hommes creux ]'), discard)

    # Return the prepared decks
    return draw, discard, exile


def main():
    '''Main program entry point.'''

    # Initialize the decks and update the GUI with each one of them
    decks = initialize()

    window = gui_build()

    for deck in decks:
        update_gui(window, deck)

    # Run the GUI main loop
    window.mainloop()


if __name__ == '__main__':
    main()


# b_Quit = ttk.Button(frame_menu, text='Quit', width=15, command=quit)
# b_Epidemic = ttk.Button(frame_menu, text='Epidemic', width=15, command=do_epidemic)

# b_Epidemic.pack()
# b_Quit.pack()









