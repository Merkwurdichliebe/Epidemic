from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel,\
    QPushButton, QComboBox, QDialog


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