from PySide2.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout,\
    QLabel, QPushButton, QButtonGroup, QGroupBox, QRadioButton

from PySide2.QtCore import Qt, QSize


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
        vbox_cardpool = QVBoxLayout();
        label = QLabel('CARD POOL')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        vbox_cardpool.addWidget(label)
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
        self.vbox_deck['discard'].setSpacing(5)
        hbox_main.addLayout(self.vbox_deck['exclude'])

        # Menu Box
        vbox_menu = QVBoxLayout()
        label = QLabel('OPTIONS')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        vbox_menu.addWidget(label)
        hbox_main.addLayout(vbox_menu)

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
        vbox_menu.addStretch()

        # Tell the Main Window to use the outer QVBoxLayout
        self.setLayout(self.vbox_app)

    def show_drawdeck(self, deck):
        # Reset the cardpool index to point to the top of the Draw Deck
        self.cardpool_index = 0

        self.buttons_root['drawdeck'].deleteLater()
        self.buttons_root['drawdeck'] = QWidget()
        p = self.buttons_root['drawdeck']
        self.vbox_deck['drawdeck'].addWidget(p)
        button_vbox = QVBoxLayout()
        button_vbox.setSpacing(5)
        p.setLayout(button_vbox)

        # Define new ones
        for i, c in enumerate(reversed(deck.cards[-16:])):
            # If the top card is a single card we display its name,
            # otherwise we display the number of possible cards.
            if len(c.cards) == 1:
                text = c.cards[0].name
            else:
                text = f'{len(c.cards)}'

            btn = QPushButton(text, self)
            btn.setFixedSize(QSize(150, 30))
            button_vbox.addWidget(btn)
            btn.clicked.connect(self.function)
        button_vbox.addStretch()

    def show_deck(self, deck):
        self.buttons_root[deck.name].deleteLater()
        self.buttons_root[deck.name] = QWidget()
        p = self.buttons_root[deck.name]
        p.setFixedWidth(150)
        self.vbox_deck[deck.name].addWidget(p)
        button_vbox = QVBoxLayout()
        button_vbox.setSpacing(5)

        p.setLayout(button_vbox)
        for i, card in self.buttons_to_display(deck):
            btn = QPushButton(card.name, self)
            btn.setFixedSize(QSize(150, 30))
            button_vbox.addWidget(btn)
            btn.clicked.connect(lambda d=deck, c=card: self.app.cb_draw_card(d, c))
        button_vbox.addStretch()

    @staticmethod
    # TODO not working for drawdeck, fix later when app is working
    def buttons_to_display(deck):
        if deck.name == 'drawdeck':
            print('k')
            return enumerate(reversed(deck.cards[-16:]))
        else:
            return enumerate(deck.sorted())

    def get_destination(self):
        if self.destination_draw.isChecked():
            return self.app.game.deck['draw']
        elif self.destination_discard.isChecked():
            return self.app.game.deck['discard']
        elif self.destination_exclude.isChecked():
            return self.app.game.deck['exclude']

    def clicked(self, b, d, c):
        print(b)
        print(f'{c} from {d} to {self.get_destination()}')

    def function(self):
        pass