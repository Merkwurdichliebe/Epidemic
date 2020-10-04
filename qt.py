from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,\
    QLabel, QPushButton, QGroupBox, QRadioButton, QComboBox, QScrollArea,\
    QButtonGroup, QDialog, QMainWindow
from PySide2.QtCore import Qt, QSize, Signal
from enum import Enum
import bisect

import logging
logging.basicConfig(level=logging.DEBUG)

# TODO center dialog boxes

WINDOW_MIN_HEIGHT = 700
SPACING = 5                 # Vertical spacing of buttons
SPACER = 20                 # Vertical spacer
WIDTH = 150                 # Width of buttons and layout columns
HEIGHT = 24                 # Height of buttons
WIDTH_WITH_SCROLL = 176


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


class EpidemicMenu(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(SPACING)
        self.addWidget(Heading('Epidemic'))
        self.combo_box = QComboBox()
        self.addWidget(self.combo_box)
        # self.btn_shuffle_epidemic.clicked.connect(self.app.cb_epidemic)
        self.button = QPushButton('Shuffle Epidemic')
        self.addWidget(self.button)


class PoolButton(QLabel):
    clicked = Signal()  # signal to be used in "connect" declared as a class variable

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(WIDTH, HEIGHT))
        self.setAlignment(Qt.AlignCenter)
        self.active = None
        self.set_active(False)
        self.connected = False

    def set_connected(self, connected):
        self.connected = connected

    def is_connected(self):
        return self.connected

    def set_active(self, active):
        self.active = active
        self.setStyleSheet(ButtonCSS.Active.value if active else ButtonCSS.Inactive.value)
        self.repaint()  # Fix Qt bug on macOS

    def mouseReleaseEvent(self, event):
        self.clicked.emit()  # emit this signal when receiving the mouseReleaseEvent

    def enterEvent(self, event):
        if self.isEnabled():
            self.setStyleSheet(ButtonCSS.MouseEnter.value)

    def leaveEvent(self, event):
        if self.isEnabled() and self.active:
            self.setStyleSheet(ButtonCSS.Active.value)
        else:
            self.setStyleSheet(ButtonCSS.Inactive.value)

    def set_text(self, text):
        self.setText(text)
        self.repaint()  # Fix Qt bug on macOS


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
        self._text.setTextFormat(Qt.RichText)
        self._text.setWordWrap(True)
        self._text.setFixedWidth(WIDTH)
        self.addWidget(self._text)
        self.addStretch()

    def set_text(self, text):
        self._text.setText(text)


class PoolSelector(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(Heading('POOL SELECTOR'))
        v_buttons = QVBoxLayout()
        v_buttons.setSpacing(SPACING)
        self.addLayout(v_buttons)
        self.button = []
        for i in range(16):
            btn = PoolButton()
            btn.set_active(False)
            self.button.append(btn)
            v_buttons.addWidget(btn)
        self.addStretch()


class Deck(QVBoxLayout):
    def __init__(self, heading, color=True):
        super().__init__()
        logging.debug(f'qt [Deck]: {heading}')
        self.addWidget(Heading(heading))
        self.use_color = color
        self.cards = []
        self.buttons = []
        self.heading = heading

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.addWidget(self.scroll_area)

        self.v_scroll = QVBoxLayout()
        self.v_scroll.setSpacing(SPACING)
        self.v_scroll.addStretch()

        self.scroll_widget = QWidget()
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
        logging.debug(f'qt [Deck] Clearing {self.heading}')
        for button in self.buttons:
            button.deleteLater()
        self.cards.clear()
        self.buttons.clear()


class DrawDeck(Deck):
    def __init__(self, heading):
        super().__init__(heading)

    def add_card_button(self, card):
        # Override base method, use bisect to insert
        # the card into the Draw Deck in sorted order
        if card.name not in self.cards:
            index = bisect.bisect_left(self.cards, card.name)
            return super().insert_button_at_index(card, index)
        else:
            print(f'[qt DrawCardDeck] {card.name} already in layout')
            return None


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


class Stats(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(Heading('Stats'))
        self.text = QLabel()
        self.addWidget(self.text)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.cardpool = Cardpool()
        self.pool_selector = PoolSelector()

        self.deck = {
            'draw': DrawDeck('DRAW CARD'),
            'discard': Deck('DISCARD PILE'),
            'exclude': Deck('EXCLUDED', color=False)
        }

        self.app_buttons = AppButtons()

        self.destination = {
            'draw': QRadioButton('Draw'),
            'discard': QRadioButton('Discard'),
            'exclude': QRadioButton('Exclude')
        }
        self.destinations = DestinationRadioBox(self.destination)
        self.epidemic_menu = EpidemicMenu()
        self.stats = Stats()

        self.setWindowTitle('Epidemic')

        # Global parent container
        v_app = QVBoxLayout()
        self.setLayout(v_app)

        # Main horizontal container
        h_main = QHBoxLayout()
        v_app.addLayout(h_main)

        h_main.addLayout(self.cardpool)
        h_main.addLayout(self.pool_selector)
        h_main.addLayout(self.deck['draw'])
        h_main.addLayout(self.deck['discard'])
        h_main.addLayout(self.deck['exclude'])

        v_sidebar = QVBoxLayout()
        v_sidebar.addWidget(Heading(' '))
        v_sidebar.addLayout(self.app_buttons)
        v_sidebar.addWidget(self.destinations)
        v_sidebar.addLayout(self.epidemic_menu)
        v_sidebar.addLayout(self.stats)
        v_sidebar.addStretch()

        h_main.addLayout(v_sidebar)
        h_main.addStretch()

    def initialise(self):
        logging.debug('qt [MainWindow] initialise')
        for k, v in self.deck.items():
            self.deck[k].clear()
