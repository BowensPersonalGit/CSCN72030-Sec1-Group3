# this class is used to create buttons for the GUI

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt


class Button(QPushButton):
    def __init__(self, text: str):
        """ creates a button with the given text"""
        super().__init__(text)
        self.setStyleSheet(
            """
                *{
                background-color: rgb(47, 93, 140);
                color: black;
                font-size: 20px;
                border-radius: 20px;
                padding: 10px 20px;
                }
                *:hover{
                    background: rgb(213, 94, 45);
                    }
                """
        )
        self.setCursor(Qt.PointingHandCursor)

    def enable(self):
        """ enables the button """
        self.setStyleSheet(
            """
                *{
                background-color: rgb(47, 93, 140);
                color: black;
                font-size: 20px;
                border-radius: 20px;
                padding: 10px 20px;
                }
                *:hover{
                    background: rgb(213, 94, 45);
                    }
                """
        )
        self.setCursor(Qt.PointingHandCursor)

    def disable(self):
        """ disables the button """
        self.setStyleSheet(
            """
                *{
                background-color: rgb(213, 94, 45);
                color: black;
                font-size: 20px;
                border-radius: 20px;
                padding: 10px 20px;
                }
                """
        )
        self.setCursor(Qt.ForbiddenCursor)
