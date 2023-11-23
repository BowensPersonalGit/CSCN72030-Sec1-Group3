# Grape widget
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
)
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer
from .buttons import Button
from GrapeTank import GrapeTank


#
# Main widget for Grape
#
class GrapeWidget(QFrame):
    def __init__(self, grapeTank: GrapeTank):
        super().__init__()
        self.grapeTankWidget = GrapeTankWidget()
        self.grapeMonitorWidget = GrapeMonitorWidget()
        self.grapeControllerWidget = GrapeControllerWidget()

        self.setStyleSheet("background-color: rgb(216, 216, 214);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)

        # define layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.grapeMonitorWidget, 0, Qt.AlignCenter)
        layout.addWidget(self.grapeControllerWidget, 0, Qt.AlignCenter | Qt.AlignBottom)
        layout.addWidget(self.grapeTankWidget, 0, Qt.AlignCenter)

        # TANK OBJ HERE ##############
        self.grapeTank = grapeTank
        # TANK OBJ HERE ##############
        self.update()

        #############button clicked events################
        self.grapeControllerWidget.refillButton.clicked.connect(self.refill)
        self.grapeControllerWidget.cleanseButton.clicked.connect(self.cleanse)

    # Update the GUI
    def update(self):
        """Update the GUI based on the target values and actual values"""
        currentLevel = self.grapeTank.getCurrentLevel()
        currentBacteria = self.grapeTank.getBacteria()
        # check if level target values are set
        if self.grapeControllerWidget.targetLevel is not None:
            # check if actual values less than target values
            if currentLevel < self.grapeControllerWidget.targetLevel:
                self.grapeTank.setCurrentLevel(currentLevel + 1)
            else:
                self.grapeTank.setCurrentLevel(currentLevel - 1)
        # check if bacteria target values are set
        if self.grapeControllerWidget.targetBacteria is not None:
            if currentBacteria < self.grapeControllerWidget.targetBacteria:
                self.grapeTank.setBacteria(currentBacteria + 1)
            else:
                self.grapeTank.setBacteria(currentBacteria - 1)

        # if target values are reached, set target values to None
        if self.grapeControllerWidget.targetLevel == currentLevel:
            print("target grape level target reached")
            self.grapeControllerWidget.targetLevel = None
            self.grapeControllerWidget.refillButton.enable()
        if self.grapeControllerWidget.targetBacteria == currentBacteria:
            print("target grape bacteria target reached")
            self.grapeControllerWidget.targetBacteria = None
            self.grapeControllerWidget.cleanseButton.enable()

        # update widgets to actual values
        self.grapeTankWidget.level = currentLevel
        self.grapeMonitorWidget.bacteria = currentBacteria

    # FOR SETTING TARGET VALUES
    def setLevelTarget(self, value):
        """Set the target level of the grape tank"""
        self.grapeControllerWidget.targetLevel = value

    def setBacteriaTarget(self, value):
        """Set the target bacteria of the grape tank"""
        self.grapeControllerWidget.targetBacteria = value

    def refill(self):
        """Refill the grape tank - for refill button"""
        self.setLevelTarget(100)
        self.grapeControllerWidget.refillButton.disable()

    def cleanse(self):
        """cleanse the grape tank of bacteria - for cleanse button"""
        self.setBacteriaTarget(100)
        self.grapeControllerWidget.cleanseButton.disable()


#
# Widget for Tank GUI
#
class GrapeTankWidget(QWidget):
    def __init__(self):
        super().__init__()
        # properties
        self.l = 300  # length of tank drawing
        self.w = 50  # width of tank drawing
        self._level = 0  # determines the level of the tank 0 - 100

        self.setMinimumSize(150, 400)
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
        painter.setBrush(QColor(202, 79, 255, 75))  # Grape purple]
        painter.setPen(Qt.NoPen)

        # rect dimensions
        mod = 3  # modifier x number of pixels per percent
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
            print("Grape Tank Overflow")
        elif self._level < 0:
            self._level = 0
            print("Grape Tank Underflow")

        self.update()


#
# Widget for Monitor GUI
#
class GrapeMonitorWidget(QFrame):
    def __init__(self):
        super().__init__()

        # info
        self._bacteria = 0

        # frame
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)
        self.setFixedHeight(75)
        self.setMaximumWidth(150)

        # label
        self.bacteriaLabel = QLabel()
        self.bacteriaLabel.setStyleSheet(
            """
            *{
            color: black;
            font-size: 15px;
            }
            """
        )
        self.bacteriaLabel.setText(f"Grape Bacteria: \n {self._bacteria} %")
        self.bacteriaLabel.setAlignment(Qt.AlignCenter)

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.bacteriaLabel, 0, Qt.AlignCenter)

    # Getter
    @property
    def bacteria(self):
        return self._bacteria

    # Setter
    @bacteria.setter
    def bacteria(self, value):
        self._bacteria = value
        self.bacteriaLabel.setText(f"Grape Bacteria: \n {self._bacteria} %")


#
# widget for Controllers
#
class GrapeControllerWidget(QWidget):
    def __init__(self):
        super().__init__()
        # target values
        self._targetLevel = None
        self._targetBacteria = None

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.refillButton = QPushButton("REFILL TANK")
        self.cleanseButton = QPushButton("CLEANSE TANK")

        # add widgets to layout
        layout.addWidget(self.cleanseButton, 0, Qt.AlignTop | Qt.AlignCenter)
        layout.addWidget(self.refillButton, 0, Qt.AlignBottom | Qt.AlignCenter)

    # Getters and Setters
    @property
    def targetLevel(self):
        return self._targetLevel

    @targetLevel.setter
    def targetLevel(self, value):
        self._targetLevel = value

    @property
    def targetBacteria(self):
        return self._targetBacteria

    @targetBacteria.setter
    def targetBacteria(self, value):
        self._targetBacteria = value

