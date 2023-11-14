# footer widget

import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QLabel,
)
from PyQt5.QtCore import Qt, QTimer

class FooterWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(40)
        self.setStyleSheet("background-color: rgb(50, 50, 50);padding: 0px; margin: 0px;")
        # version label
        self.versionLabel = QLabel()
        self.versionLabel.setText("Version 9999999999999")
        self.versionLabel.setStyleSheet("color: white; font-size: 12px;")
        self.versionLabel.setAlignment(Qt.AlignRight)

        # layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.versionLabel, 0, Qt.AlignRight | Qt.AlignVCenter)



if __name__ == "__main__":

    # test code
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    widget = FooterWidget()
    widget.show()
    app.exec_()