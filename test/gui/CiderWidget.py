# Cider widget
import sys
from .AppleWidget import *

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer


#
# Main widget for Cider
#
class CiderWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.ciderTankWidget = CiderTankWidget()
        self.ciderMonitorWidget = CiderMonitorWidget()
        self.ciderControllerWidget = CiderControllerWidget()

        self.setStyleSheet("background-color: rgb(216, 216, 214);")
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)

        # define layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.ciderMonitorWidget, 0, Qt.AlignCenter)
        layout.addWidget(self.ciderControllerWidget, 0, Qt.AlignCenter | Qt.AlignBottom)
        layout.addWidget(self.ciderTankWidget, 0, Qt.AlignCenter)

    # Set the levels (PASS IN VALUES HERE)
    def changeLevels(self, value):
        value = CiderTank.getCurrentLevel()
        self.ciderTankWidget.level = value

    # Set the pressure (PASS IN VALUES HERE)
    def changePressure(self, value):
        self.ciderMonitorWidget.pressure = value

    # Set the alcohol (PASS IN VALUES HERE)
    def changeAlcohol(self, value):
        self.ciderMonitorWidget.alcohol = value


#
# Widget for Tank GUI
#
class CiderTankWidget(QWidget):
    def __init__(self):
        super().__init__()
        # properties
        self.l = 500  # length of tank drawing
        self.w = 200  # width of tank drawing
        self._level = 0  # determines the level of the tank 0 - 100

        self.setMinimumSize(300, 600)
        self.label = QLabel(f"{self._level}%")
        self.label.setStyleSheet("font-size: 12px;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.label, 0, Qt.AlignBottom | Qt.AlignCenter)

    # Paint event, !triggered by update()!
    def paintEvent(self, event):
        painter = QPainter(self)

        # draw liquid
        self.drawLiquid(painter)
        # draw tank
        self.drawTank(painter)

        # update label  
        self.label.setText(f"{self._level}%")

    # Draw tank
    def drawTank(self, painter):
        # color
        color = QColor(0, 0, 0, 75)  # black
        painter.setPen(QPen(color, 4))  # line
        painter.setBrush(Qt.NoBrush)  # unfilled

        # rect dimensions
        l = self.l
        w = self.w
        r = 20

        # coordinates
        x = (self.width() - w) / 2
        y = (self.height() - l) / 2

        # draw
        painter.drawRoundedRect(int(x), int(y), int(w), int(l), r, r)

    # Draw liquid
    def drawLiquid(self, painter):
        # color
        painter.setBrush(QColor(255, 173, 125, 75))  # Cider orange??
        painter.setPen(Qt.NoPen)

        # rect dimensions
        mod = 5
        l = self._level * mod
        w = self.w
        r = 20

        # coordinates
        x = (self.width() - w) / 2
        y = ((self.height() - self.l) / 2) + (self.l - l)

        # draw
        painter.drawRoundedRect(int(x), int(y), int(w), int(l), r, r)

    # Getter
    @property
    def level(self):
        return self._level

    # Setter - use to change level plz
    @level.setter
    def level(self, value):
        self._level = value
        # level value check
        if self._level > 100:
            self._level = 100
            print("Cider Tank Overflow")
        elif self._level < 0:
            self._level = 0
            print("Cider Tank Underflow")
        self.update()


#
# Widget for Monitor GUI
#
class CiderMonitorWidget(QFrame):
    def __init__(self):
        super().__init__()

        # info
        self._pressure = 0
        self._alcohol = 0

        # frame
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)
        self.setMaximumWidth(150)

        # pressure label
        self.pressureLabel = QLabel()
        self.pressureLabel.setStyleSheet(
            """
            *{
            color: black;
            font-size: 15px;
            }
            """
        )
        self.pressureLabel.setText(f"Cider Pressure: \n {self._pressure} psi")
        self.pressureLabel.setAlignment(Qt.AlignCenter)

        # alcohol label
        self.alcoholLabel = QLabel()
        self.alcoholLabel.setStyleSheet(
            """
            *{
            color: black;
            font-size: 15px;
            }
            """
        )
        self.alcoholLabel.setText(f"Cider Alcohol: \n {self._alcohol} %")
        self.alcoholLabel.setAlignment(Qt.AlignCenter)

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.pressureLabel, 0, Qt.AlignCenter)
        layout.addWidget(self.alcoholLabel, 0, Qt.AlignCenter)

    # Getter
    @property
    def pressure(self):
        return self._pressure

    # Setter
    @pressure.setter
    def pressure(self, value):
        self._pressure = value
        self.pressureLabel.setText(f"Cider Pressure: \n {self._pressure} psi")

    # Getter
    @property
    def alcohol(self):
        return self._alcohol

    # Setter
    @alcohol.setter
    def alcohol(self, value):
        self._alcohol = value
        self.alcoholLabel.setText(f"Cider Alcohol: \n {self._alcohol} %")


#
# widget for Controllers
#
class CiderControllerWidget(QWidget):
    def __init__(self):
        super().__init__()

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.button = QPushButton("START\nFERMENTATION")
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.setStyleSheet(
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
        
        self.button.clicked.connect(self.fermentCider)
        # add widgets to layout
        layout.addWidget(self.button, 0, Qt.AlignBottom | Qt.AlignCenter)

    def fermentCider(self):
    
        # set values for the timer  
        self.current_value = 0
        self.target_value = 100
        self.increment = 5

        # create timer to increment the label
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tank_level)
        self.timer.start(300)  # Update every 40 milliseconds
        AppleControllerWidget.dec_tank_level()

    def update_tank_level(self):
        # Increment the tank level until the target is reached
        if self.current_value <= self.target_value:
            # Update the tank level in the AppleWidget instance
            parent_widget = self.parent()
            if parent_widget:
                tank_widget = parent_widget.ciderTankWidget
                tank_widget.level = self.current_value

            self.current_value += self.increment
        else:
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CiderWidget()
    win.show()
    sys.exit(app.exec())
