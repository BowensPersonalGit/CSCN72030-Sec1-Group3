# Wine widget
import sys

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

from .buttons import Button

from WineTank import WineTank


#
# Main widget for Wine
#
class WineWidget(QFrame):
    def __init__(self, wineTank: WineTank):
        super().__init__()
        self.wineTankWidget = WineTankWidget()
        self.wineMonitorWidget = WineMonitorWidget()
        self.wineControllerWidget = WineControllerWidget()

        self.setStyleSheet("background-color: rgb(216, 216, 214);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)

        # define layout
        layout = QVBoxLayout()
        self.setLaselfyout(layout)

        # add widgets to layout
        layout.addWidget(self.wineMonitorWidget, 0, Qt.AlignCenter)
        layout.addWidget(self.wineControllerWidget, 0, Qt.AlignCenter | Qt.AlignBottom)
        layout.addWidget(self.wineTankWidget, 0, Qt.AlignCenter)

        # TANK OBJ HERE ##############
        self.wineTank = wineTank
        # TANK OBJ HERE ##############
        self.update()

        #############button clicked events################

    # Update the GUI
    def update(self):
        """Update the GUI based on the target values and actual values"""
        currentLevel = self.wineTank.getCurrentLevel()
        currentPressure = self.wineTank.getPressure()
        currentAlcohol = self.wineTank.getAlcohol()
        # check if level target values are set
        if self.wineControllerWidget.targetLevel is not None:
            if currentLevel < self.wineControllerWidget.targetLevel:
                self.wineTank.setCurrentLevel(currentLevel + 1)
                #################################################
                # TODO: decrement water and apple levels in the FILES
                # hard code dat shit!
                ###################################################
            else:
                self.wineTank.setCurrentLevel(currentLevel - 1)
        # check if pressure target values are set
        if self.wineControllerWidget.targetPressure is not None:
            if currentPressure < self.wineControllerWidget.targetPressure:
                self.wineTank.setPressure(currentPressure + 1)
            else:
                self.wineTank.setPressure(currentPressure - 1)
        # check if alcohol target values are set
        if self.wineControllerWidget.targetAlcohol is not None:
            if currentAlcohol < self.wineControllerWidget.targetAlcohol:
                self.wineTank.setAlcohol(currentAlcohol + 1)
            else:
                self.wineTank.setAlcohol(currentAlcohol - 1)

        # if target values are reached, set target values to None
        if self.wineControllerWidget.targetLevel == currentLevel:
            print("target wine level target reached")
            self.wineControllerWidget.targetLevel = None
            self.wineControllerWidget.refillButton.enable()
        if self.wineControllerWidget.targetPressure == currentPressure:
            print("target wine pressure target reached")
            self.wineControllerWidget.targetPressure = None
        if self.wineControllerWidget.targetAlcohol == currentAlcohol:
            print("target wine alcohol target reached")
            self.wineControllerWidget.targetAlcohol = None

        # update widgets to actual values
        self.wineTankWidget.level = currentLevel
        self.wineMonitorWidget.pressure = currentPressure
        self.wineMonitorWidget.alcohol = currentAlcohol

    # FOR SETTING TARGET VALUES
    def setLevelTarget(self, value):
        """Set the target level of the wine tank"""
        self.wineControllerWidget.targetLevel = value

    def setPressureTarget(self, value):
        """Set the target pressure of the wine tank"""
        self.wineControllerWidget.targetPressure = value

    def setAlcoholTarget(self, value):
        """Set the target alcohol of the wine tank"""
        self.wineControllerWidget.targetAlcohol = value

    def ferment(self):
        """Refill the wine tank - for refill button"""
        self.setLevelTarget(100)
        self.wineControllerWidget.fermentButton.disable()


#
# Widget for Tank GUI
#
class WineTankWidget(QWidget):
    def __init__(self):
        super().__init__()
        # properties
        self.l = 500  # length of tank drawing
        self.w = 200  # width of tank drawing
        self._level = 0  # determines the level of the tank 0 - 100

        self.setMinimumSize(300, 600)
        self.setContentsMargins(0, 0, 0, 0)
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
        painter.setBrush(QColor(115, 48, 60, 75))  # Wine purple
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
            print("Wine Tank Overflow")
        elif self._level < 0:
            self._level = 0
            print("Wine Tank Underflow")
        self.update()


#
# Widget for Monitor GUI
#
class WineMonitorWidget(QFrame):
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
        self.pressureLabel.setText(f"Wine Pressure: \n {self._pressure} psi")
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
        self.alcoholLabel.setText(f"Wine Alcohol: \n {self._alcohol} %")
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
        self.pressureLabel.setText(f"Wine Pressure: \n {self._pressure} psi")

    # Getter
    @property
    def alcohol(self):
        return self._alcohol

    # Setter
    @alcohol.setter
    def alcohol(self, value):
        self._alcohol = value
        self.alcoholLabel.setText(f"Wine Alcohol: \n {self._alcohol} %")


#
# widget for Controllers
#
class WineControllerWidget(QWidget):
    def __init__(self):
        super().__init__()
        # target values
        self._targetLevel = None
        self._targetPressure = None
        self._targetAlcohol = None

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.fermentButton = Button("FERMENT")

        # add widgets to layout
        layout.addWidget(self.fermentButton, 0, Qt.AlignBottom | Qt.AlignCenter)

    # Getter and Setter for target values
    @property
    def targetLevel(self):
        return self._targetLevel

    @targetLevel.setter
    def targetLevel(self, value):
        self._targetLevel = value

    @property
    def targetPressure(self):
        return self._targetPressure

    @targetPressure.setter
    def targetPressure(self, value):
        self._targetPressure = value

    @property
    def targetAlcohol(self):
        return self._targetAlcohol

    @targetAlcohol.setter
    def targetAlcohol(self, value):
        self._targetAlcohol = value

