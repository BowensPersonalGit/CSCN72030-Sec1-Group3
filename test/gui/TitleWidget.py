# widget for custom title bar

import sys

from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)

from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QMouseEvent, QPixmap


class TitleWidget(QFrame):
    def __init__(self):
        """Creates a title bar widget"""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize UI elements"""
        # frame
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(75)
        self.setStyleSheet(
            "background-color: rgb(50, 50, 50);padding: 0px; margin: 0px;"
        )

        # icon label
        self.iconLabel = QLabel()
        self.iconLabel.setFixedSize(60, 60)
        self.iconLabel.setStyleSheet("margin: 0px, 5px, 0px, 0px;")
        pixmap = QPixmap("test/gui/imgs/icon.png")
        self.iconLabel.setPixmap(pixmap)
        self.iconLabel.setScaledContents(True)

        # logo label
        self.logoLabel = QLabel()
        self.logoLabel.setFixedSize(210, 60)
        self.logoLabel.setStyleSheet("margin: 0px, 0px, 0px, 0px;")
        pixmap = QPixmap("test/gui/imgs/logo.png")
        self.logoLabel.setPixmap(pixmap)
        self.logoLabel.setScaledContents(True)

        # minimize button
        self.minimizeButton = QPushButton()
        self.minimizeButton.setText("-")
        self.minimizeButton.setFixedSize(30, 30)
        self.minimizeButton.setStyleSheet(
            "background-color: rgb(50, 50, 50); color: white; font-size: 20px; "
        )
        self.minimizeButton.setCursor(Qt.PointingHandCursor)
        self.minimizeButton.clicked.connect(self.minimizeWindow)

        # maximize button
        self.maximizeButton = QPushButton()
        self.maximizeButton.setText("O")
        self.maximizeButton.setFixedSize(30, 30)
        self.maximizeButton.setStyleSheet(
            "background-color: rgb(50, 50, 50); color: white; font-size: 20px;"
        )
        self.maximizeButton.setCursor(Qt.PointingHandCursor)
        self.maximizeButton.clicked.connect(self.maximizeWindow)

        # close button
        self.closeButton = QPushButton()
        self.closeButton.setText("X")
        self.closeButton.setFixedSize(30, 30)
        self.closeButton.setStyleSheet(
            "background-color: rgb(50, 50, 50); color: white; font-size: 20px;"
        )
        self.closeButton.setCursor(Qt.PointingHandCursor)
        self.closeButton.clicked.connect(self.closeWindow)

        # horizontal spacer to separte logo and window buttons
        spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Fixed)

        # layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.iconLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.logoLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        layout.addSpacerItem(spacer)
        layout.addWidget(self.minimizeButton, 0, Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.maximizeButton, 0, Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.closeButton, 0, Qt.AlignRight | Qt.AlignVCenter)

        self.IsDraggable = False
        self.offset = None

    # drag window functions
    def mousePressEvent(self, event: QMouseEvent):
        """Draggable window function - on mouse click"""
        if event.button() == Qt.LeftButton:
            self.IsDraggable = True
            self.offset = (
                event.globalPos() - self.parent().pos()
            )  # global pos of the click event - the pos of the parent (window)

    def mouseMoveEvent(self, event: QMouseEvent):
        """Draggable window function - on mouse move"""
        if self.IsDraggable:
            self.parent().move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Draggable window function - on mouse release"""
        self.IsDraggable = False

    # maximize window fucntion
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Maximize window function - on double click"""
        self.maximizeWindow()

    # button functions
    def minimizeWindow(self):
        """Minimize window button function"""
        self.parent().showMinimized()

    def maximizeWindow(self):
        """Maximize window button function"""
        if self.parent().isMaximized():
            self.parent().showNormal()
        else:
            self.parent().showMaximized()

    def closeWindow(self):
        """Close window button function"""
        self.parent().close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TitleWidget()
    widget.show()
    sys.exit(app.exec())
