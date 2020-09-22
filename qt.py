from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout,\
    QLabel, QPushButton, QGroupBox, QRadioButton, QComboBox, QDialog

from PySide2.QtCore import Qt, QSize

# TODO center dialog boxes

COLORS = {'blue': '#3333ff',
          'black': '#000000',
          'yellow': '#e68019',
          'red': '#cc0000',
          'green': '#009933',
          'gray': '#bfbfbf'}


class MainWindow(QWidget):
    def __init__(self, app):
        super().__init__()  # QWidget defaults
        self.app = app
        self.cardpool_index = 0

        self.drawdeck_btns = []
        self.vbox_app = QVBoxLayout()
        self.vbox_deck = {'drawdeck': QVBoxLayout(),
                          'draw': QVBoxLayout(),
                          'discard': QVBoxLayout(),
                          'exclude': QVBoxLayout()}

        self.destination_draw = QRadioButton('Draw')
        self.destination_discard = QRadioButton('Discard')
        self.destination_exclude = QRadioButton('Exclude')

        self.buttons_root = {'drawdeck': QWidget(),
                             'draw': QWidget(),
                             'discard': QWidget(),
                             'exclude': QWidget()}

        self.text_cardpool = QLabel()
        self.text_stats = QLabel()
        self.combo_epidemic = QComboBox()

        self.initialise_ui()

    def initialise_ui(self):
        # self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Epidemic')

        # Main Box
        title = QLabel('Epidemic')
        self.vbox_app.addWidget(title)

        hbox_main = QHBoxLayout()
        self.vbox_app.addLayout(hbox_main)

        # Cardpool Box
        vbox_cardpool = QVBoxLayout()
        label = QLabel('CARD POOL')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        vbox_cardpool.addWidget(label)
        vbox_cardpool.addWidget(self.text_cardpool)
        vbox_cardpool.addStretch()
        hbox_main.addLayout(vbox_cardpool)

        # Draw Deck Box
        label = QLabel('DRAW DECK')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        self.vbox_deck['drawdeck'].addWidget(label)
        self.vbox_deck['drawdeck'].setSpacing(5)
        hbox_main.addLayout(self.vbox_deck['drawdeck'])

        # Draw Card Box
        label = QLabel('DRAW CARD')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        self.vbox_deck['draw'].addWidget(label)
        self.vbox_deck['draw'].setSpacing(5)
        hbox_main.addLayout(self.vbox_deck['draw'])

        # Discard Box
        label = QLabel('DISCARD')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        self.vbox_deck['discard'].addWidget(label)
        self.vbox_deck['discard'].setSpacing(5)
        hbox_main.addLayout(self.vbox_deck['discard'])

        # exclude Box
        label = QLabel('EXCLUDE')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        self.vbox_deck['exclude'].addWidget(label)
        self.vbox_deck['exclude'].setSpacing(5)
        hbox_main.addLayout(self.vbox_deck['exclude'])

        # Options Box
        vbox_menu = QVBoxLayout()
        label = QLabel('OPTIONS')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        vbox_menu.addWidget(label)
        hbox_main.addLayout(vbox_menu)

        # New Game & Help
        vbox_game = QVBoxLayout()
        vbox_game.setSpacing(5)
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
        label.setMinimumWidth(150)
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
        vbox_epidemic.setSpacing(5)
        label = QLabel('Epidemic')
        label.setAlignment(Qt.AlignHCenter)
        vbox_epidemic.addWidget(label)
        vbox_epidemic.addWidget(self.combo_epidemic)
        btn = QPushButton('Shuffle Epidemic')
        btn.clicked.connect(self.app.cb_epidemic)
        vbox_epidemic.addWidget(btn)
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
        d = drawdeck.cards[-1 - self.cardpool_index]
        text = ''
        for card in sorted(set(d.cards), key=lambda x: x.name):
            text += f'{card.name} ({d.cards.count(card)})\n'
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
            btn.setFixedSize(QSize(150, 30))
            box.addWidget(btn)
            btn.clicked.connect(lambda ignore=True, index=i: self.app.cb_update_cardpool(index))  # 1
        box.addStretch()

    def show_deck(self, deck):
        box = self.get_new_deck_vbox(deck.name)
        for card in self.buttons_to_display(deck):
            btn = QPushButton(card.name, self)
            btn.setFixedSize(QSize(150, 30))
            color = COLORS['gray'] if deck.name == 'exclude' else COLORS[card.color]
            btn.setStyleSheet(f'color: {color}')
            box.addWidget(btn)
            btn.clicked.connect(lambda d=deck, c=card: self.app.cb_draw_card(d, c))
        box.addStretch()

    @staticmethod
    # TODO not working for drawdeck, fix later when app is working
    def buttons_to_display(deck):
        if deck.name == 'drawdeck':
            return reversed(deck.cards[-16:])
        else:
            return deck.sorted()

    def get_destination(self):
        if self.destination_draw.isChecked():
            return self.app.game.deck['draw']
        elif self.destination_discard.isChecked():
            return self.app.game.deck['discard']
        elif self.destination_exclude.isChecked():
            return self.app.game.deck['exclude']

    def get_new_deck_vbox(self, deck_name):
        self.buttons_root[deck_name].deleteLater()
        self.buttons_root[deck_name] = QWidget()
        p = self.buttons_root[deck_name]
        p.setFixedWidth(150)
        self.vbox_deck[deck_name].addWidget(p)
        button_vbox = QVBoxLayout()
        button_vbox.setSpacing(5)
        p.setLayout(button_vbox)
        return button_vbox

    def update_epidemic_combo(self):
        deck = self.app.game.deck['draw']
        # Update the epidemic dropdown list
        # based on the available cards in the Draw Deck.
        cards = sorted([c.name for c in list(set(deck.cards[0].cards))])

        self.combo_epidemic.clear()
        self.combo_epidemic.addItems(cards)
        self.combo_epidemic.repaint()
        # TODO don't clear this each time, add/remove items individiually

    def update_stats(self, stats):
        text = f'Total cards: {stats.total}\n'
        text += f'In discard pile: {stats.in_discard}\n'
        text += f'\nTop card frequency:\n'
        text += f'{stats.top_freq} '
        text += f'({stats.percentage:.2%})'
        text += '\n\n'
        for card in stats.top_cards:
            text += '- ' + card.name + '\n'

        self.text_stats.setText(text)
        self.text_stats.repaint()
        # TODO make stats a function


# 1: See SO article for reasons for "ignore" argument:
# https://stackoverflow.com/questions/18836291/lambda-function-returning-false

# 2: A hack which should be fixed with a better event handling
# https://stackoverflow.com/questions/4510712/qlabel-settext-not-displaying-text-immediately-before-running-other-method

class DialogNewGame(QDialog):
    def __init__(self, games):
        super().__init__()
        self.setWindowTitle('Start New Game')
        vbox_dialog = QVBoxLayout()
        label = QLabel('Select the game you wish to track:')
        vbox_dialog.addWidget(label)
        self.combo = QComboBox()
        self.combo.addItems(games)
        vbox_dialog.addWidget(self.combo)
        hbox_buttons = QHBoxLayout()
        b_cancel = QPushButton('Cancel')
        b_cancel.clicked.connect(self.cancel)
        hbox_buttons.addWidget(b_cancel)
        b_start = QPushButton('Start New Game')
        b_start.clicked.connect(self.start)
        b_start.setDefault(True)
        hbox_buttons.addWidget(b_start)
        vbox_dialog.addLayout(hbox_buttons)
        self.setLayout(vbox_dialog)

    def start(self):
        self.accept()
        return self.combo.currentText()

    def cancel(self):
        self.reject()


class DialogHelp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Open Help Page')
        vbox = QVBoxLayout()
        label = QLabel('Help is available on the application\'s GitHub page.')
        vbox.addWidget(label)
        hbox_buttons = QHBoxLayout()
        b_cancel = QPushButton('Close')
        b_cancel.clicked.connect(self.reject)
        hbox_buttons.addWidget(b_cancel)
        b_start = QPushButton('View in browser')
        b_start.clicked.connect(self.accept)
        b_start.setDefault(True)
        hbox_buttons.addWidget(b_start)
        vbox.addLayout(hbox_buttons)
        self.setLayout(vbox)

