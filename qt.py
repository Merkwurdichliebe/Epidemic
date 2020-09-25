from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,\
    QLabel, QPushButton, QGroupBox, QRadioButton, QComboBox, QScrollArea
from PySide2.QtCore import Qt, QSize

# TODO center dialog boxes
# TODO Fixed window size

COLORS = {'blue': '#3333ff',
          'black': '#000000',
          'yellow': '#e68019',
          'red': '#cc0000',
          'green': '#009933',
          'gray': '#bfbfbf'}

SPACING = 5  # Vertical spacing of buttons
WIDTH = 150  # Width of buttons and layout columns
WIDTH_WITH_SCROLL = 165
MAX_CARDS_IN_CARDPOOL = 20
MAX_CARDS_IN_STATS = 10


class ColumnLabel(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setStyleSheet('font-weight: bold')
        self.setFixedWidth(WIDTH)
        self.setAlignment(Qt.AlignHCenter)


class DeckScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(False)
        self.setMaximumWidth(WIDTH_WITH_SCROLL)


class MainWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.cardpool_index = 0

        self.setFixedSize(1100, 700)

        self.vbox_app = QVBoxLayout()
        self.vbox_deck = {'drawdeck': QVBoxLayout(),
                          'draw': QVBoxLayout(),
                          'discard': QVBoxLayout(),
                          'exclude': QVBoxLayout()}

        self.scroll_deck = {'draw': DeckScrollArea(),
                            'discard': DeckScrollArea(),
                            'exclude': DeckScrollArea()}

        self.destination_draw = QRadioButton('Draw')
        self.destination_discard = QRadioButton('Discard')
        self.destination_exclude = QRadioButton('Exclude')

        self.buttons_root = {'drawdeck': QWidget(),
                             'draw': QWidget(),
                             'discard': QWidget(),
                             'exclude': QWidget()}

        self.text_cardpool = QLabel()
        self.text_cardpool.setMaximumWidth(WIDTH)

        self.text_stats = QLabel()
        self.combo_epidemic = QComboBox()
        self.btn_shuffle_epidemic = QPushButton('Shuffle Epidemic')

        self.initialise_ui()

    def initialise_ui(self):
        self.setWindowTitle('Epidemic')

        # Global parent layout
        hbox_main = QHBoxLayout()
        self.vbox_app.addLayout(hbox_main)

        # Cardpool Box
        vbox_cardpool = QVBoxLayout()
        label = ColumnLabel('CARD POOL')
        vbox_cardpool.addWidget(label)
        vbox_cardpool.addWidget(self.text_cardpool)
        vbox_cardpool.addStretch()
        hbox_main.addLayout(vbox_cardpool)

        # Draw Deck Box
        label = ColumnLabel('DRAW DECK')
        self.vbox_deck['drawdeck'].addWidget(label)
        self.vbox_deck['drawdeck'].setSpacing(SPACING)
        hbox_main.addLayout(self.vbox_deck['drawdeck'])

        # Draw Card Box
        label = ColumnLabel('DRAW CARD')
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.scroll_deck['draw'])
        # self.vbox_deck['draw'].setSpacing(SPACING)
        hbox_main.addLayout(layout)

        # Discard Box
        label = ColumnLabel('DISCARD PILE')
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.scroll_deck['discard'])
        # self.vbox_deck['draw'].setSpacing(SPACING)
        hbox_main.addLayout(layout)

        # exclude Box
        label = ColumnLabel('EXCLUDED')
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.scroll_deck['exclude'])
        # self.vbox_deck['draw'].setSpacing(SPACING)
        hbox_main.addLayout(layout)

        # Options Box
        vbox_menu = QVBoxLayout()
        label = ColumnLabel('OPTIONS')
        vbox_menu.addWidget(label)
        hbox_main.addLayout(vbox_menu)

        # New Game & Help
        vbox_game = QVBoxLayout()
        vbox_game.setSpacing(SPACING)
        b_new_game = QPushButton('New Game')
        b_new_game.clicked.connect(self.app.cb_new_game)
        vbox_game.addWidget(b_new_game)
        b_help = QPushButton('Help')
        b_help.clicked.connect(self.app.cb_dialog_help)
        vbox_game.addWidget(b_help)
        vbox_menu.addLayout(vbox_game)

        # Destination Radio Box
        vbox_destination = QVBoxLayout()
        label = QLabel('Card Destination')
        label.setMinimumWidth(WIDTH)
        label.setAlignment(Qt.AlignHCenter)
        vbox_destination.addWidget(label)
        group_box = QGroupBox()
        group_box.setWindowTitle('Destination')
        self.destination_exclude.setChecked(True)
        vbox_destination.addWidget(self.destination_draw)
        vbox_destination.addWidget(self.destination_discard)
        vbox_destination.addWidget(self.destination_exclude)
        group_box.setLayout(vbox_destination)
        vbox_menu.addWidget(group_box)

        # Epidemic dropdown
        vbox_epidemic = QVBoxLayout()
        vbox_epidemic.setSpacing(SPACING)
        label = QLabel('Epidemic')
        label.setAlignment(Qt.AlignHCenter)
        vbox_epidemic.addWidget(label)
        vbox_epidemic.addWidget(self.combo_epidemic)
        self.btn_shuffle_epidemic.clicked.connect(self.app.cb_epidemic)
        vbox_epidemic.addWidget(self.btn_shuffle_epidemic)
        vbox_menu.addLayout(vbox_epidemic)

        # Stats
        label = QLabel('Stats')
        label.setAlignment(Qt.AlignHCenter)
        vbox_menu.addWidget(label)
        vbox_menu.addWidget(self.text_stats)

        vbox_menu.addStretch()

        # Tell the Main Window to use the outer QVBoxLayout
        self.setLayout(self.vbox_app)

    def show_cardpool(self, drawdeck):
        text = ''
        if not drawdeck.is_empty():
            d = drawdeck.cards[-1 - self.cardpool_index]
            if len(d) < MAX_CARDS_IN_CARDPOOL:
                for card in sorted(set(d.cards), key=lambda x: x.name):
                    text += f'{card.name} ({d.cards.count(card)})\n'
            else:
                text += f'{MAX_CARDS_IN_CARDPOOL}+ cards'
            text += f'\n[{d.name}]'
        self.text_cardpool.setText(text)
        self.text_cardpool.repaint()  # 2 TODO Fix repaint

    def show_drawdeck(self, deck):
        # Reset the cardpool index to point to the top of the Draw Deck
        self.app.cb_update_cardpool(0)
        box = self.get_new_deck_vbox('drawdeck')

        # Define new ones
        for i, c in enumerate(reversed(deck.cards[-16:])):
            # If the top card is a single card we display its name,
            # otherwise we display the number of possible cards.
            if len(c) == 1:
                text = c.cards[0].name
            else:
                text = f'{len(c)}'

            btn = QPushButton(text, self)
            btn.setFixedSize(QSize(WIDTH, 30))
            box.addWidget(btn)
            btn.clicked.connect(lambda ignore=True, index=i: self.app.cb_update_cardpool(index))  # 1
        box.addStretch()

    def show_deck(self, deck):
        scroll_widget = QWidget()  # Redraw from scratch
        box = QVBoxLayout()
        box.setSpacing(SPACING)
        if not deck.is_empty():
            for card in self.buttons_to_display(deck):
                btn = QPushButton(card.name, self)
                btn.setFixedSize(QSize(WIDTH, 30))
                color = COLORS['gray'] if deck.name == 'exclude' else COLORS[card.color]
                btn.setStyleSheet(f'color: {color}')
                box.addWidget(btn)
                btn.clicked.connect(lambda d=deck, c=card: self.app.cb_draw_card(d, c))
        box.addStretch()
        scroll_widget.setLayout(box)
        self.scroll_deck[deck.name].setWidget(scroll_widget)

    @staticmethod
    # TODO not working for drawdeck, fix later when app is working
    def buttons_to_display(deck):
        return reversed(deck.cards[-16:]) if deck.name == 'drawdeck' else deck.sorted()

    def get_destination(self):
        if self.destination_draw.isChecked():
            return self.app.game.deck['draw']
        elif self.destination_discard.isChecked():
            return self.app.game.deck['discard']
        elif self.destination_exclude.isChecked():
            return self.app.game.deck['exclude']

    def get_new_deck_vbox(self, deck_name):
        # TODO Delete cause only used by draw deck show method
        self.buttons_root[deck_name].deleteLater()
        self.buttons_root[deck_name] = QWidget()
        p = self.buttons_root[deck_name]
        p.setFixedWidth(WIDTH)
        self.vbox_deck[deck_name].addWidget(p)
        button_vbox = QVBoxLayout()
        button_vbox.setSpacing(SPACING)
        p.setLayout(button_vbox)
        return button_vbox

    def update_epidemic_combo(self):
        """Update the epidemic dropdown list
        based on the available cards in the Draw Deck."""
        deck = self.app.game.deck['draw']
        if not deck.is_empty():
            items = sorted([c.name for c in list(set(deck.bottom().cards))])
            self.combo_epidemic.setDisabled(False)
            self.btn_shuffle_epidemic.setDisabled(False)
        else:
            items = ['(Draw Deck Empty)']
            self.combo_epidemic.setDisabled(True)
            self.btn_shuffle_epidemic.setDisabled(True)
            # TODO Maybe add "became empty" method

        self.combo_epidemic.clear()
        self.combo_epidemic.addItems(items)
        self.combo_epidemic.repaint()
        # TODO don't clear this each time, add/remove items individiually

    def update_stats(self, stats):
        text = f'Total cards: {stats.total}\n'
        text += f'In discard pile: {stats.in_discard}\n'
        if not stats.deck['draw'].is_empty():
            text += f'\nTop card frequency:\n'
            text += f'{stats.top_freq} '
            text += f'({stats.percentage:.2%})'
            text += '\n\n'
            if len(stats.top_cards) < MAX_CARDS_IN_STATS:
                for card in stats.top_cards:
                    text += '- ' + card.name + '\n'
            else:
                text += f'({MAX_CARDS_IN_STATS}+ cards)'
        else:
            text += '\n(Draw Deck is empty)'

        self.text_stats.setText(text)
        self.text_stats.repaint()
        # TODO make stats a function

# 1: See SO article for reasons for "ignore" argument:
# https://stackoverflow.com/questions/18836291/lambda-function-returning-false

# 2: A hack which should be fixed with a better event handling
# https://stackoverflow.com/questions/4510712/qlabel-settext-not-displaying-text-immediately-before-running-other-method
