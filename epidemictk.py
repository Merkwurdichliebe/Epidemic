import tkinter as tk
from tkinter import ttk
from webbrowser import open as webopen
import utility


class MainWindow:
    def __init__(self, app):
        """Main application designed as class in order to allow easier communication
        between interface elements. cf. http://thinkingtkinter.sourceforge.net
        """

        # Main Tk window

        self.root = tk.Tk()
        self.root.title('Epidemic')
        self.root.configure(padx=20, pady=10)
        self.root.resizable(False, False)

        self.app = app
        self.deck = self.app.deck

        # Replace default menu

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Define GUI variables and set defaults<

        # Destination radio button
        self.destination_choice = tk.StringVar()
        self.destination_choice.set('exile')

        # Epidemic dropdown menu
        self.epidemic_choice = tk.StringVar()

        # Keep track of added buttons so we can destroy and redraw them later

        self.draw_deck_btns = []
        self.draw_card_btns = []
        self.discard_btns = []

        # Styles

        self.font = {'h1': ('Helvetica', 30, 'bold'),
                     'h2': ('Helvetica', 14, 'bold'),
                     'p': ('Helvetica', 14)}

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

        img = utility.get_path('img/pandemic-logo.png')
        self.img_logo = tk.PhotoImage(file=img)
        self.lbl_logo = tk.Label(self.frm_header_title, image=self.img_logo)
        self.lbl_logo.pack(side=tk.LEFT)

        btn_help = ttk.Button(self.frm_header_title, text='Help', width=15,
                              command=self.display_help)
        btn_help.pack(side=tk.RIGHT)

        # Title

        self.label_title = tk.Label(self.frm_header_title, text='DECK TRACKER', padx=10, font=self.font['h1'])
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
        # They never change so we declare and pack them in one go

        tk.Label(self.frm_cardpool, pady=10, text='POSSIBLE CARDS', width=20, font=self.font['h2']).pack()
        tk.Label(self.frm_draw_deck, pady=10, text='DRAW DECK', width=20, font=self.font['h2']).pack()
        tk.Label(self.frm_draw_card, pady=10, text='DRAW CARD', width=20, font=self.font['h2']).pack()
        tk.Label(self.frm_discard, pady=10, text='DISCARD DECK', width=20, font=self.font['h2']).pack()
        tk.Label(self.frm_exile, pady=10, text='ABANDONED or EXILED', width=20, font=self.font['h2']).pack()
        tk.Label(self.frm_menu, pady=10, text='Card destination', font=self.font['h2']).pack()

        # Bottom Text

        tk.Label(self.frm_bottom, pady=10, text='© 2020 Tal Zana', font=self.font['h2']).pack()

        # Two textboxes containing the dynamically built lists
        # for the exile deck and the cardpool deck

        self.txt_cardpool = tk.Text(self.frm_cardpool, name='txt_cardpool', width=20, height=50, font=self.font['p'])
        self.txt_cardpool.pack()

        self.txt_exile = tk.Text(self.frm_exile, name='txt_exile', width=20, height=50, font=self.font['p'])
        self.txt_exile.pack()

        # Radio buttons in their own frame

        self.frm_radio = tk.Frame(self.frm_menu, pady=10)
        self.frm_radio.pack()

        radio_discard = tk.Radiobutton(self.frm_radio, width=15, text='Discard',
                                       variable=self.destination_choice,
                                       value='discard', anchor=tk.W, padx=10)
        radio_exile = tk.Radiobutton(self.frm_radio, width=15, text='Exile',
                                     variable=self.destination_choice,
                                     value='exile', anchor=tk.W, padx=10)
        radio_draw = tk.Radiobutton(self.frm_radio, width=15, text='Draw',
                                    variable=self.destination_choice,
                                    value='draw', anchor=tk.W, padx=10)

        radio_discard.pack(anchor=tk.W)
        radio_exile.pack(anchor=tk.W)
        radio_draw.pack(anchor=tk.W)

        # Dropdown menu for selecting city in epidemic

        self.frm_epidemic = tk.Frame(self.frm_menu)
        self.frm_epidemic.pack()

        tk.Label(self.frm_menu, pady=20, text='Epidemic', font=self.font['h2']).pack()

        self.epidemic_options = []
        self.dropdown_epidemic = tk.OptionMenu(self.frm_menu, self.epidemic_choice,
                                               self.epidemic_options)
        self.dropdown_epidemic.config(width=15)
        self.dropdown_epidemic.pack()

        btn_epidemic = ttk.Button(self.frm_menu, text='Shuffle as epidemic', width=15,
                                  command=self.app.cb_epidemic)
        btn_epidemic.pack()

        # Stats

        self.frm_stats = tk.Frame(self.frm_menu, pady=10)
        self.frm_stats.pack()

        tk.Label(self.frm_stats, pady=10, text='Stats', font=self.font['h2']).pack()

        self.txt_stats = tk.Text(self.frm_stats, width=20, height=15, font=self.font['p'], wrap=tk.WORD)
        self.txt_stats.pack()

        # Center the app window on the screen

        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        pos_x = int(self.root.winfo_screenwidth() / 3 - width / 2)
        pos_y = int(self.root.winfo_screenheight() / 4 - height)
        self.root.geometry("+{}+{}".format(pos_x, pos_y))

        # Index of the cardpool to display when a Draw Deck item is clicked

        self.cardpool_index = 0

    def update_gui(self, deck):

        # We only update the GUI elements that need updating
        # based on the deck that is passed to the method.

        if deck.name == 'cardpool':
            self.update_textbox(self.txt_cardpool, self.deck['draw'].cards[-1 - self.cardpool_index])

        if deck.name == 'exile':
            self.update_textbox(self.txt_exile, self.deck['exile'])

        if deck.name == 'draw':

            # Reset the cardpool index to point to the top of the Draw Deck
            self.cardpool_index = 0

            # Refresh Draw Deck buttons:
            # Destroy old buttons if they exist
            if self.draw_deck_btns:
                for b in self.draw_deck_btns:
                    b.destroy()

            # Define new ones
            for i, c in enumerate(reversed(deck.cards[-16:])):
                # If the top card is a single card we display its name,
                # otherwise we display the number of possible cards.
                if len(c.cards) == 1:
                    text = c.cards[0].name
                    color = c.cards[0].color + '.TButton'
                else:
                    text = f'{len(c.cards)}'
                    color = 'black.TButton'
                btn = ttk.Button(
                    self.frm_draw_deck,
                    style=color,
                    width=15,
                    text=text
                )
                # The callback for the cardpool update is part of this class,
                # no need to ask App to do that.
                btn.configure(command=lambda x=i: self.cb_view_cardpool(x))
                btn.pack()
                self.draw_deck_btns.append(btn)

            # Refresh draw card buttons

            if self.draw_card_btns:
                for b in self.draw_card_btns:
                    b.destroy()

            for i, c in enumerate(sorted(set(deck.cards[-1].cards), key=lambda x: x.name)):
                btn = ttk.Button(self.frm_draw_card, style=c.color + '.TButton',
                                 width=15, text=c.name)
                btn.configure(command=lambda d=deck, e=c: self.app.cb_draw_card(d, e))
                btn.pack()
                self.draw_card_btns.append(btn)

        if deck.name == 'discard':
            if self.discard_btns:
                for btn in self.discard_btns:
                    btn.destroy()

            for i, c in enumerate(sorted(deck.cards, key=lambda x: x.name)):
                btn = ttk.Button(self.frm_discard, style=c.color + '.TButton',
                                 width=15, text=c.name)
                btn.configure(command=lambda d=deck, e=c: self.app.cb_draw_card(d, e))
                btn.pack()
                self.discard_btns.append(btn)

    @staticmethod
    def update_textbox(box, deck):
        """Update a Tk textbox with the contents of the passed Deck object.
        This is used to refresh both the cardpool textbox and the Exile textbox."""
        # Method is static because it doesn't need the self keyword,
        # it only updates the contents of the Tk textbox which is passed to it.
        box.configure(state=tk.NORMAL)
        box.delete(1.0, tk.END)
        for card in sorted(deck.cards, key=lambda x: x.name):
            box.insert(tk.END, card.name + '\n')
        box.configure(state=tk.DISABLED)

    def update_dropdown(self):
        # Update the epidemic dropdown list based on the available cards in the Draw Deck.
        cards = sorted([c.name for c in list(set(self.deck['draw'].cards[0].cards))])
        self.epidemic_options = cards

        # command value lambda syntax is from
        # https://stackoverflow.com/questions/28412496/updating-optionmenu-from-list
        m = self.dropdown_epidemic.children['menu']
        m.delete(0, tk.END)
        for c in cards:
            m.add_command(label=c, command=lambda v=c: self.epidemic_choice.set(v))
        self.epidemic_choice.set(cards[0])

    def cb_view_cardpool(self, index):
        # Callback from the buttons used to display the possible choices in the Draw Deck.
        # Outputs the possible cards in each potential draw.
        self.cardpool_index = index
        self.update_gui(self.deck['cardpool'])

    def update_stats(self, stats):
        text = f'\nTop card frequency:\n'
        text += f'{stats.top_freq} '
        text += f'({stats.percentage:.2%})'
        text += '\n\n'
        for card in stats.top_cards:
            text += '- ' + card.name + '\n'

        self.txt_stats.configure(state=tk.NORMAL)
        self.txt_stats.delete(1.0, tk.END)
        self.txt_stats.insert(tk.END, f'Total cards: {stats.total}\n')
        self.txt_stats.insert(tk.END, f'In discard pile: {stats.in_discard}\n')
        self.txt_stats.insert(tk.END, text)
        self.txt_stats.configure(state=tk.DISABLED)

    def get_destination(self):
        return self.destination_choice.get()

    def get_epidemic(self):
        return self.epidemic_choice.get()

    def display_help(self):
        def cb_open_web():
            webopen('https://github.com/Merkwurdichliebe/Epidemic/wiki')
            popup.destroy()

        popup = tk.Toplevel()
        popup.title('Epidemic Help')
        text = 'Help is available on the application\'s GitHub page.'
        lbl1 = tk.Label(popup, text=text, pady=10, padx=20)
        lbl1.pack()

        frm_btns = tk.Frame(popup, pady=10)
        frm_btns.pack()

        btn = tk.Button(frm_btns, text='View in browser', width=15, command=cb_open_web)
        btn.pack(side=tk.LEFT, padx=5)
        btn = tk.Button(frm_btns, text='Close', width=15, command=popup.destroy)
        btn.pack(side=tk.LEFT, padx=5)

        width = popup.winfo_reqwidth()
        height = popup.winfo_reqheight()
        pos_x = int(self.root.winfo_screenwidth() / 2 - width / 2)
        pos_y = int(self.root.winfo_screenheight() / 2 - height)
        popup.geometry("+{}+{}".format(pos_x, pos_y))

        popup.mainloop()
