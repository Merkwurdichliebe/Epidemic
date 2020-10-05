from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel,\
    QPushButton, QComboBox, QDialog
from PySide2.QtCore import QSize
# import PySide2.QtCore.Qt.Sheet


class DialogNewGame(QDialog):
    def __init__(self, games):
        super().__init__()
        self.setWindowTitle('Start New Game')
        self.setFixedSize(QSize(250, 150))
        v_main = QVBoxLayout()
        v_main.addWidget(QLabel('Select the game you wish to track:'))

        self.combo = QComboBox()
        self.combo.addItems(games)
        self.combo.setCurrentIndex(3)
        v_main.addWidget(self.combo)

        h_buttons = QHBoxLayout()
        b_cancel = QPushButton('Cancel')
        b_cancel.clicked.connect(self.cancel)
        h_buttons.addWidget(b_cancel)

        b_start = QPushButton('Start New Game')
        b_start.clicked.connect(self.start)
        b_start.setDefault(True)
        h_buttons.addWidget(b_start)

        v_main.addLayout(h_buttons)
        self.setLayout(v_main)

    def start(self):
        self.accept()
        return self.combo.currentText()

    def cancel(self):
        self.reject()


class DialogHelp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Open Help Page')
        self.setFixedSize(QSize(350, 100))
        # self.setWindowFlag(PySide2.QtCore.Qt.Sheet)

        v_main = QVBoxLayout()
        v_main.addWidget(QLabel('Help is available on the application\'s GitHub page.'))

        h_buttons = QHBoxLayout()
        b_cancel = QPushButton('Close')
        b_cancel.clicked.connect(self.reject)
        h_buttons.addWidget(b_cancel)

        b_start = QPushButton('View in browser')
        b_start.clicked.connect(self.accept)
        b_start.setDefault(True)
        h_buttons.addWidget(b_start)

        v_main.addLayout(h_buttons)
        self.setLayout(v_main)