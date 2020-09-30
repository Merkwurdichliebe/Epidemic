from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,\
    QLabel, QPushButton, QGroupBox, QRadioButton, QComboBox, QScrollArea,\
    QButtonGroup, QDialog, QMainWindow
from PySide2.QtCore import Qt, QSize, Signal
from enum import Enum

# TODO center dialog boxes
# TODO don't reset scroll after click

WINDOW_MIN_HEIGHT = 700
SPACING = 5                 # Vertical spacing of buttons
SPACER = 20                 # Vertical spacer
WIDTH = 150                 # Width of buttons and layout columns
HEIGHT = 24                 # Height of buttons
WIDTH_WITH_SCROLL = 176

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
        self.setText(f'<h4>{text}</h4>')
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
        self.setFixedSize(QSize(WIDTH, HEIGHT))
        self.setAlignment(Qt.AlignCenter)
        self.setText(text)
        self.active = None
        self.set_active(False)

    def set_active(self, active):
        self.active = active
        self.setStyleSheet(ButtonCSS.Active.value if active else ButtonCSS.Inactive.value)

    def mouseReleaseEvent(self, event):
        # self.set_active(True)
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


class DrawDeck(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(Heading('DRAW DECK'))
        self.v_buttons = QVBoxLayout()
        self.v_buttons.setSpacing(SPACING)
        self.button = []
        self.addLayout(self.v_buttons)
        for i in range(16):
            btn = PoolButton('init')
            btn.setFixedSize(QSize(WIDTH, HEIGHT))
            btn.set_active(False)
            self.button.append(btn)
            self.v_buttons.addWidget(btn)
        self.addStretch()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._text_cardpool = QLabel()
        self._text_cardpool.setWordWrap(True)

        self.drawdeck = DrawDeck()

        # self.drawdeck = QVBoxLayout()
        # self.scroll_deck = {
        #     'draw': DeckScrollArea(),
        #     'discard': DeckScrollArea(),
        #     'exclude': DeckScrollArea()
        # }
        #
        # self.destination = {
        #     'draw_pool': QRadioButton('Draw (Pool)'),
        #     'draw_top': QRadioButton('Draw (Top)'),
        #     'discard': QRadioButton('Discard'),
        #     'exclude': QRadioButton('Exclude')
        # }
        # self.destination_box = DestinationRadioBox(self.destination.values())
        #
        # self.draw_deck_root = QWidget()
        # self.text_cardpool.setMaximumWidth(WIDTH)
        #
        # self.text_stats = QLabel()
        # self.combo_epidemic = QComboBox()
        # self.combo_epidemic.setFixedWidth(WIDTH_WITH_SCROLL)
        # self.btn_shuffle_epidemic = QPushButton('Shuffle Epidemic')
        # self.btn_shuffle_epidemic.setFixedWidth(WIDTH_WITH_SCROLL)

        self.setWindowTitle('Epidemic')

        # Global parent container
        v_app = QVBoxLayout()
        self.setLayout(v_app)

        # Main horizontal container
        self.h_main = QHBoxLayout()
        v_app.addLayout(self.h_main)

        self._create_cardpool()
        self.h_main.addLayout(self.drawdeck)
        # self._create_drawdeck()

    def _create_cardpool(self):
        v_cardpool = QVBoxLayout()
        v_cardpool.addWidget(Heading('CARD POOL'))
        v_cardpool.addWidget(self._text_cardpool)
        v_cardpool.addStretch()
        self.h_main.addLayout(v_cardpool)

    def _create_drawdeck(self):
        v_drawdeck = QVBoxLayout()
        v_drawdeck.addWidget(Heading('DRAW DECK'))
        v_drawdeck.addLayout(self.v_drawdeck_buttons)
        v_drawdeck.addStretch()
        self.h_main.addLayout(v_drawdeck)

    def set_cardpool_text(self, text):
        self._text_cardpool.setText(text)

    def insert_into(self, index, widget):
        self.v_drawdeck_buttons.insertWidget(index, widget)







    def show_drawdeck_old(self, deck):
        # Reset the cardpool index to point to the top of the Draw Deck
        # self.app.cb_update_cardpool(self.cardpool_index)
        self.show_cardpool(deck)

        # text = f'First {TOP_CARDS} card positions in the deck, top to bottom, ' \
        #        f''
        # text += f'with the number of possible cards at each position.'
        # label = QLabel(text)
        # label.setWordWrap(True)
        # self.drawdeck.addWidget(label)

        # Redraw the parent widhet from scratch
        self.draw_deck_root.deleteLater()
        self.draw_deck_root = QWidget()
        self.draw_deck_root.setFixedWidth(WIDTH_WITH_SCROLL)

        self.drawdeck.addWidget(self.draw_deck_root)

        box = QVBoxLayout()
        box.setSpacing(SPACING)
        self.draw_deck_root.setLayout(box)

        for i, c in enumerate(reversed(deck.cards[-TOP_CARDS:])):
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
        return reversed(deck.cards[-TOP_CARDS:]) if deck.name == 'drawdeck' else deck.sorted()

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
