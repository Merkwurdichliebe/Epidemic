from PySide2.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout,\
    QLabel, QPushButton

from PySide2.QtCore import Qt, QSize


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()  # QWidget defaults
        # self.app = app
        self.cardpool_index = 0

        self.drawdeck_btns = []
        self.vbox_app = QVBoxLayout()
        self.vbox_deck = {'drawdeck': QVBoxLayout(),
                          'draw': QVBoxLayout(),
                          'discard': QVBoxLayout(),
                          'exile': QVBoxLayout()}

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
        hbox_main.addLayout(vbox_cardpool)
        label = QLabel('CARD POOL')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        vbox_cardpool.addWidget(label)
        vbox_cardpool.addStretch()

        # Draw Deck Box
        hbox_main.addLayout(self.vbox_deck['drawdeck'])
        label = QLabel('DRAW DECK')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        self.vbox_deck['drawdeck'].addWidget(label)
        self.vbox_deck['drawdeck'].setSpacing(5)
        self.vbox_deck['drawdeck'].addStretch()

        # Draw Card Box
        hbox_main.addLayout(self.vbox_deck['draw'])
        label = QLabel('DRAW CARD')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        self.vbox_deck['draw'].addWidget(label)
        self.vbox_deck['draw'].setSpacing(5)
        self.vbox_deck['draw'].addStretch()

        # Discard Box
        hbox_main.addLayout(self.vbox_deck['discard'])
        label = QLabel('DISCARD')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        self.vbox_deck['discard'].addWidget(label)
        self.vbox_deck['discard'].setSpacing(5)
        self.vbox_deck['discard'].addStretch()

        # Exile Box
        hbox_main.addLayout(self.vbox_deck['exile'])
        label = QLabel('EXILE')
        label.setMinimumWidth(150)
        label.setAlignment(Qt.AlignHCenter)
        self.vbox_deck['exile'].addWidget(label)
        self.vbox_deck['exile'].addStretch()

        self.setLayout(self.vbox_app)

    def show_drawdeck(self, deck):
        # Reset the cardpool index to point to the top of the Draw Deck
        self.cardpool_index = 0

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
            self.vbox_deck['drawdeck'].addWidget(btn)
            btn.clicked.connect(self.function)

        self.vbox_deck['drawdeck'].addStretch(1)

    def show_deck(self, deck):
        for i, card in self.buttons_to_display(deck):

            btn = QPushButton(card.name, self)
            btn.setFixedSize(QSize(150, 30))
            self.vbox_deck[deck.name].addWidget(btn)
            btn.clicked.connect(self.function)

    @staticmethod
    # TODO not working for drawdeck, fix later when app is working
    def buttons_to_display(deck):
        if deck.name == 'drawdeck':
            print('k')
            return enumerate(reversed(deck.cards[-16:]))
        else:
            return enumerate(deck.sorted())

    def function(self):
        pass
