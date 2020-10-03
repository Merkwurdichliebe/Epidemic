from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,\
    QLabel, QPushButton, QGroupBox, QRadioButton, QComboBox, QScrollArea,\
    QButtonGroup, QDialog, QMainWindow
from PySide2.QtCore import Qt, QSize, Signal
from enum import Enum
import bisect

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
        # self.setFixedWidth(WIDTH_WITH_SCROLL)
        self.setAlignment(Qt.AlignHCenter)


class AppButtons(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(SPACING)
        self.button_new_game = QPushButton('New Game')
        self.addWidget(self.button_new_game)
        self.button_help = QPushButton('Help')
        self.addWidget(self.button_help)


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

        for button in destinations.values():
            self.b_group.addButton(button)
            box.addWidget(button)

        self.setLayout(box)

        destinations['exclude'].setChecked(True)


class Cardpool(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(Heading('CARD POOL'))
        self._text = QLabel()
        self._text.setWordWrap(True)
        self._text.setFixedWidth(WIDTH)
        self.addWidget(self._text)
        self.addStretch()

    def set_text(self, text):
        self._text.setText(text)


class DrawDeck(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(Heading('DRAW DECK'))
        v_buttons = QVBoxLayout()
        v_buttons.setSpacing(SPACING)
        self.addLayout(v_buttons)
        self.button = []
        for i in range(16):
            btn = PoolButton('init')
            btn.set_active(False)
            self.button.append(btn)
            v_buttons.addWidget(btn)
        self.addStretch()


class Deck(QVBoxLayout):
    def __init__(self, heading, color=True):
        super().__init__()
        self.addWidget(Heading(heading))
        self.use_color = color
        self.cards = []
        self.buttons = []
        self.heading = heading

        self.scroll_widget = QWidget()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.addWidget(self.scroll_area)

        self.v_scroll = QVBoxLayout()
        self.v_scroll.setSpacing(SPACING)
        self.v_scroll.addStretch()
        self.scroll_widget.setLayout(self.v_scroll)
        self.scroll_area.setFixedWidth(WIDTH_WITH_SCROLL)
        self.scroll_area.setWidget(self.scroll_widget)

    def add_card_button(self, card):
        return self.insert_button_at_index(card, 0)

    def insert_button_at_index(self, card, index):
        button = CardButton(card)
        self.v_scroll.insertWidget(index, button)
        color = COLOR[card.color] if self.use_color else COLOR['gray']
        button.set_color(color)
        self.cards.insert(index, card.name)
        self.buttons.append(button)
        return button

    def remove_card_button(self, button):
        self.cards.remove(button.card.name)
        self.buttons.remove(button)
        self.removeWidget(button)
        button.deleteLater()

    def clear(self):
        print(f'Clearing {self.heading}')
        for button in self.buttons:
            button.deleteLater()
        self.cards.clear()
        self.buttons.clear()


class DrawCardDeck(Deck):
    def __init__(self, heading):
        super().__init__(heading)

    def add_card_button(self, card):
        # Override base method, use bisect to insert
        # the card into the Draw Deck in sorted order
        if card.name not in self.cards:
            index = bisect.bisect_left(self.cards, card.name)
            return super().insert_button_at_index(card, index)
        else:
            print('not')


class CardButton(QLabel):
    clicked = Signal()  # signal to be used in "connect" declared as a class variable

    def __init__(self, card):
        super().__init__(card.name)
        self.card = card
        self.color = None
        self.stylesheet = None
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(QSize(WIDTH, HEIGHT))

    def set_color(self, color):
        self.color = color
        self.stylesheet = f'background: {self.color};' \
                          f'color: white;' \
                          f'font-weight: bold;'
        self.setStyleSheet(self.stylesheet)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()  # emit this signal when receiving the mouseReleaseEvent

    def enterEvent(self, event):
        self.setStyleSheet(ButtonCSS.MouseEnter.value)

    def leaveEvent(self, event):
        self.setStyleSheet(self.stylesheet)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.cardpool = Cardpool()
        self.drawdeck = DrawDeck()

        self.deck = {
            'draw': DrawCardDeck('DRAW CARD'),
            'discard': Deck('DISCARD PILE'),
            'exclude': Deck('EXCLUDED', color=False)
        }

        self.app_buttons = AppButtons()

        self.destination = {
            'draw_pool': QRadioButton('Draw (Pool)'),
            'draw_top': QRadioButton('Draw (Top)'),
            'discard': QRadioButton('Discard'),
            'exclude': QRadioButton('Exclude')
        }
        self.destinations = DestinationRadioBox(self.destination)

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
        h_main = QHBoxLayout()
        v_app.addLayout(h_main)

        h_main.addLayout(self.cardpool)
        h_main.addLayout(self.drawdeck)
        h_main.addLayout(self.deck['draw'])
        h_main.addLayout(self.deck['discard'])
        h_main.addLayout(self.deck['exclude'])

        v_options = QVBoxLayout()
        v_options.addWidget(Heading(' '))
        v_options.addLayout(self.app_buttons)
        v_options.addWidget(self.destinations)
        v_options.addStretch()

        h_main.addLayout(v_options)
        h_main.addStretch()

    def initialise(self):
        for k, v in self.deck.items():
            self.deck[k].clear()






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
        if self.destinations.get_selection() == self.destination['draw_pool']:
            if not self.app.game.deck['draw'].is_empty():
                return self.app.game.deck['draw'].cards[-1 - self.cardpool_index]
            else:
                return self.app.game.deck['draw']
        elif self.destinations.get_selection() == self.destination['draw_top']:
            return self.app.game.deck['draw']
        elif self.destinations.get_selection() == self.destination['discard']:
            return self.app.game.deck['discard']
        elif self.destinations.get_selection() == self.destination['exclude']:
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
