#!/usr/bin/python3

# Main entrance

from globals import *

class Tools(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.button = QPushButton('Confirm', self)
        self.layout.addWidget(self.button)
        self.button.show()
        self.show()
