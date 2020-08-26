import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self, app):
        """Main application designed as class in order to allow easier communication
        between interface elements. cf. http://thinkingtkinter.sourceforge.net
        """

        # Main Tk window

        self.root = tk.Tk()
        self.root.title('Pandemic Deck Tracker')
        self.root.configure(padx=20, pady=10)
        self.root.resizable(False, False)

        self.app = app
        self.deck = self.app.deck

        # Replace default menu

        emptyMenu = tk.Menu(self.root)
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

        self.frm_header = tk.Frame(self.root)
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

        self.frm_main = tk.Frame(self.root)
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

        self.frm_bottom = tk.Frame(self.root, pady=20)
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

        btn_epidemic = ttk.Button(self.frm_menu, text='Shuffle as epidemic', width=15, command=self.app.cb_epidemic)
        btn_epidemic.pack()

        # Stats

        self.frm_stats = tk.Frame(self.frm_menu, pady=10)
        self.frm_stats.pack()

        self.lbl_stats = tk.Label(self.frm_stats, pady=10, text='Stats', font=FONT_H1)
        self.lbl_stats.pack()

        self.txt_stats = tk.Text(self.frm_stats, width=20, font=FONT_TEXT, wrap=tk.WORD)
        self.txt_stats.pack()

        # Center the app window on the screen

        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()
        positionRight = int(self.root.winfo_screenwidth() / 3 - windowWidth / 2)
        positionDown = int(self.root.winfo_screenheight() / 4 - windowHeight)
        self.root.geometry("+{}+{}".format(positionRight, positionDown))

        # Index of the cardpool to display when a Draw Deck item is clicked

        self.cardpool_index = 0


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

        if deck.name == 'draw':
            for button in self.draw_buttons:
                button.destroy()

            for button in self.cardpool_buttons:
                button.destroy()

            self.cardpool_index = 0
            self.update_textbox(self.txt_cardpool, self.deck['draw'].cards[-1 - self.cardpool_index])

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
                button.configure(command=lambda d=deck, c=card: self.app.cb_draw_card(d, c))
                button.pack()
                self.draw_buttons.append(button)

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
                button.configure(command=lambda d=deck, c=card: self.app.cb_draw_card(d, c))
                button.pack()
                self.discard_buttons.append(button)

    @staticmethod
    def update_textbox(textbox, deck):
        """Update a Tk textbox with the contents of the passed Deck object.
        This is used to refresh both the cardpool textbox and the Exile textbox."""
        # Method is static because it doesn't need the self keyword,
        # it only updates the contents of the Tk textbox which is passed to it.
        textbox.configure(state=tk.NORMAL)
        textbox.delete(1.0, tk.END)
        for card in sorted(deck.cards, key=lambda x: x.city):
            textbox.insert(tk.END, card.city + '\n')
        textbox.configure(state=tk.DISABLED)

    def update_dropdown(self):
        # Update the epidemic dropdown list based on the available cards in the Draw Deck.
        unique_cards = sorted([card.city for card in list(set(self.deck['draw'].cards[0].cards))])
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

    def update_stats(self, stats):
        text = f'\nTop card frequency:\n'
        text += f'{stats.top_frequency} '
        text += f'({stats.percentage:.2%})'
        text += '\n\n'
        for card in stats.top_cards:
            text += '- ' + card.city + '\n'

        self.txt_stats.configure(state=tk.NORMAL)
        self.txt_stats.delete(1.0, tk.END)
        self.txt_stats.insert(tk.END, f'Total cards: {stats.cards_total}\n')
        self.txt_stats.insert(tk.END, f'In discard pile: {stats.in_discard}\n')
        self.txt_stats.insert(tk.END, text)
        self.txt_stats.configure(state=tk.DISABLED)

    def get_destination_choice(self):
        return self.destination_choice.get()

    def get_epidemic_choice(self):
        return self.epidemic_choice.get()
