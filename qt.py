from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,\
    QLabel, QPushButton, QGroupBox, QRadioButton, QComboBox, QScrollArea,\
    QButtonGroup
from PySide2.QtCore import Qt, QSize, Signal
from enum import Enum

# TODO center dialog boxes
# TODO don't reset scroll after click

WINDOW_MINIMUM_HEIGHT = 700
SPACING = 5                 # Vertical spacing of buttons
SPACER = 20                 # Vertical spacer
WIDTH = 150                 # Width of buttons and layout columns
HEIGHT = 24                 # Height of buttons
WIDTH_WITH_SCROLL = 176
MAX_CARDS_IN_CARDPOOL = 35
MAX_CARDS_IN_STATS = 10

COLOR = {
    'blue': '#4073bf',
    'black': '#404040',
    'yellow': '#f5993d',
    'red': '#df4620',
    'green': '#009933',
    'gray': '#bfbfbf'
    }


class ButtonCSS(Enum):
    """Stylesheets for active and inactive cardpool buttons
    displayed in the Draw Deck column"""
    Active = 'background: #999999; color: black; font-weight: bold;'
    Inactive = 'background: #dddddd; color: black; font-weight: bold;'
    MouseEnter = 'background: black; color: white; font-weight: bold;'


class Heading(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setStyleSheet('font-weight: bold')
        self.setFixedWidth(WIDTH_WITH_SCROLL)
        self.setAlignment(Qt.AlignHCenter)


class DeckLayout(QVBoxLayout):
    def __init__(self, heading, widget):
        super().__init__()
        self.addWidget(Heading(heading))
        self.addWidget(widget)


class DeckScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(WIDTH_WITH_SCROLL)


class CardButton(QLabel):
    clicked = Signal()  # signal to be used in "connect" declared as a class variable

    def __init__(self, deck, card):
        super().__init__(card.name)
        self.deck = deck
        self.card = card
        self.color = COLOR['gray'] if deck.name == 'exclude' else COLOR[card.color]
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            f'background: {self.color};'
            f'color: white;'
            f'font-weight: bold;')
        self.setFixedSize(QSize(WIDTH, HEIGHT))

    def mouseReleaseEvent(self, event):
        self.clicked.emit()  # emit this signal when receiving the mouseReleaseEvent

    def enterEvent(self, event):
        self.setStyleSheet(ButtonCSS.MouseEnter.value)

    def leaveEvent(self, event):
        self.setStyleSheet(f'background: {self.color};'
                           f'color: white;'
                           f'font-weight: bold;')


class PoolButton(QLabel):
    clicked = Signal()  # signal to be used in "connect" declared as a class variable

    def __init__(self, text):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText(text)
        self.active = None
        self.set_active(False)

    def set_active(self, active):
        self.active = active
        self.setStyleSheet(ButtonCSS.Active.value if active else ButtonCSS.Inactive.value)

    def mouseReleaseEvent(self, event):
        self.set_active(True)
        self.clicked.emit()  # emit this signal when receiving the mouseReleaseEvent

    def enterEvent(self, event):
        self.setStyleSheet(ButtonCSS.MouseEnter.value)

    def leaveEvent(self, event):
        if self.active:
            self.setStyleSheet(ButtonCSS.Active.value)
        else:
            self.setStyleSheet(ButtonCSS.Inactive.value)


class DestinationRadioBox(QGroupBox):
    def __init__(self, destinations):
        super().__init__()
        label = Heading('Card Destination')
        label.setMinimumWidth(WIDTH)
        label.setAlignment(Qt.AlignHCenter)
        box = QVBoxLayout()
        box.addWidget(label)

        # We are subclassing QGroupBox for the *visual* container
        self.setMaximumWidth(WIDTH_WITH_SCROLL)

        # QButtonGroup is used for the *logical* grouping of buttons
        self.b_group = QButtonGroup()

        for button in destinations:
            self.b_group.addButton(button)
            box.addWidget(button)
        self.setLayout(box)

    def get_selection(self):
        return self.b_group.checkedButton()


class MainWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.setMinimumHeight(WINDOW_MINIMUM_HEIGHT)
        self.app = app
        self.cardpool_index = 0

        self.drawdeck = QVBoxLayout()
        self.scroll_deck = {
            'draw': DeckScrollArea(),
            'discard': DeckScrollArea(),
            'exclude': DeckScrollArea()
        }

        self.destination = {
            'draw_pool': QRadioButton('Draw (Pool)'),
            'draw_top': QRadioButton('Draw (Top)'),
            'discard': QRadioButton('Discard'),
            'exclude': QRadioButton('Exclude')
        }
        self.destination_box = DestinationRadioBox(self.destination.values())

        self.draw_deck_root = QWidget()
        self.text_cardpool = QLabel()
        self.text_cardpool.setMaximumWidth(WIDTH)

        self.text_stats = QLabel()
        self.combo_epidemic = QComboBox()
        self.combo_epidemic.setFixedWidth(WIDTH_WITH_SCROLL)
        self.btn_shuffle_epidemic = QPushButton('Shuffle Epidemic')
        self.btn_shuffle_epidemic.setFixedWidth(WIDTH_WITH_SCROLL)

        self.initialise_ui()

    def initialise_ui(self):
        self.setWindowTitle('Epidemic')

        # Global parent layout
        v_app = QVBoxLayout()
        h_main = QHBoxLayout()
        v_app.addLayout(h_main)

        # Cardpool Box
        # hbox_main.addLayout(DeckLayout('CARD POOL', self.text_cardpool)
        # This doesn't work because it needs addStretch

        v_cardpool = QVBoxLayout()
        label = Heading('CARD POOL')
        v_cardpool.addWidget(label)
        v_cardpool.addWidget(self.text_cardpool)
        v_cardpool.addStretch()
        h_main.addLayout(v_cardpool)

        # Draw Deck Box
        label = Heading('DRAW DECK')
        self.drawdeck.addWidget(label)
        h_main.addLayout(self.drawdeck)

        # Other Deck boxes
        h_main.addLayout(DeckLayout('DRAW CARD', self.scroll_deck['draw']))
        h_main.addLayout(DeckLayout('DISCARD PILE', self.scroll_deck['discard']))
        h_main.addLayout(DeckLayout('EXCLUDED', self.scroll_deck['exclude']))

        # Options Box
        v_menu = QVBoxLayout()
        label = Heading(' ')
        v_menu.addWidget(label)

        # New Game & Help
        v_game = QVBoxLayout()
        v_game.setSpacing(SPACING)
        b_new_game = QPushButton('New Game')
        b_new_game.setMaximumWidth(WIDTH_WITH_SCROLL)
        b_new_game.clicked.connect(self.app.cb_new_game)
        v_game.addWidget(b_new_game)
        b_help = QPushButton('Help')
        b_help.setMaximumWidth(WIDTH_WITH_SCROLL)
        b_help.clicked.connect(self.app.cb_dialog_help)
        v_game.addWidget(b_help)
        v_menu.addLayout(v_game)

        # Destination Radio Box
        v_menu.addWidget(self.destination_box)
        self.destination['exclude'].setChecked(True)
        v_menu.addSpacing(SPACER)

        # Epidemic dropdown
        v_epidemic = QVBoxLayout()
        v_epidemic.setSpacing(SPACING)
        label = Heading('Epidemic')
        v_epidemic.addWidget(label)
        v_epidemic.addWidget(self.combo_epidemic)
        self.btn_shuffle_epidemic.clicked.connect(self.app.cb_epidemic)
        v_epidemic.addWidget(self.btn_shuffle_epidemic)
        v_menu.addLayout(v_epidemic)
        v_menu.addSpacing(SPACER)

        # Stats
        label = Heading('Stats')
        v_menu.addWidget(label)
        v_menu.addWidget(self.text_stats)

        v_menu.addStretch()

        h_main.addLayout(v_menu)

        # Tell the Main Window to use the outer QVBoxLayout
        self.setLayout(v_app)

    def show_cardpool(self, drawdeck):
        text = ''
        if not drawdeck.is_empty():
            d = drawdeck.cards[-1 - self.cardpool_index]
            if len(set(d)) < MAX_CARDS_IN_CARDPOOL:
                for card in sorted(set(d.cards), key=lambda x: x.name):
                    text += f'{card.name} ({d.cards.count(card)})\n'
            else:
                text += f'{MAX_CARDS_IN_CARDPOOL}+ cards'
            text += f'\n[{d.name}]'
        self.text_cardpool.setText(text)
        self.text_cardpool.repaint()  # 2 TODO Fix repaint

    def show_drawdeck(self, deck):
        # Reset the cardpool index to point to the top of the Draw Deck
        # self.app.cb_update_cardpool(self.cardpool_index)
        self.show_cardpool(deck)

        # Redraw the parent widhet from scratch
        self.draw_deck_root.deleteLater()
        self.draw_deck_root = QWidget()
        self.draw_deck_root.setFixedWidth(WIDTH_WITH_SCROLL)

        self.drawdeck.addWidget(self.draw_deck_root)

        box = QVBoxLayout()
        box.setSpacing(SPACING)
        self.draw_deck_root.setLayout(box)

        for i, c in enumerate(reversed(deck.cards[-16:])):
            # If the top card is a single card we display its name,
            # otherwise we display the number of possible cards.
            if len(c) == 1:
                text = c.cards[0].name
            else:
                text = f'{len(c)}'

            btn = PoolButton(text)
            btn.setFixedSize(QSize(WIDTH, HEIGHT))
            btn.set_active(True if i == self.cardpool_index else False)
            box.addWidget(btn)
            btn.clicked.connect(lambda ignore=True, index=i: self.app.cb_update_cardpool(index))  # 1
        box.addStretch()

    def show_deck(self, deck):
        scroll_widget = QWidget()  # Redraw from scratch
        box = QVBoxLayout()
        box.setSpacing(SPACING)
        if not deck.is_empty():
            for card in self.buttons_to_display(deck):
                btn = CardButton(deck, card)
                box.addWidget(btn)
                btn.clicked.connect(lambda d=deck, c=card: self.app.cb_draw_card(d, c))
        box.addStretch()
        scroll_widget.setLayout(box)
        self.scroll_deck[deck.name].setWidget(scroll_widget)
        self.scroll_deck[deck.name].repaint()

    @staticmethod
    # TODO not working for drawdeck, fix later when app is working
    def buttons_to_display(deck):
        return reversed(deck.cards[-16:]) if deck.name == 'drawdeck' else deck.sorted()

    def get_destination(self):
        if self.destination_box.get_selection() == self.destination['draw_pool']:
            if not self.app.game.deck['draw'].is_empty():
                return self.app.game.deck['draw'].cards[-1 - self.cardpool_index]
            else:
                return self.app.game.deck['draw']
        elif self.destination_box.get_selection() == self.destination['draw_top']:
            return self.app.game.deck['draw']
        elif self.destination_box.get_selection() == self.destination['discard']:
            return self.app.game.deck['discard']
        elif self.destination_box.get_selection() == self.destination['exclude']:
            return self.app.game.deck['exclude']

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
                    text += f'\u2022 {card.name}\n'
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
