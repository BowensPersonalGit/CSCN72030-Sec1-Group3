# Apple widget
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

from AppleTank import AppleTank


#
# Main widget for Apple
#
class AppleWidget(QFrame):
    def __init__(self, appleTank: AppleTank):
        super().__init__()
        self.appleTankWidget = AppleTankWidget()
        self.appleMonitorWidget = AppleMonitorWidget()
        self.appleControllerWidget = AppleControllerWidget()

        self.setStyleSheet("background-color: rgb(216, 216, 214);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)

        # define layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.appleMonitorWidget, 0, Qt.AlignCenter)
        layout.addWidget(self.appleControllerWidget, 0, Qt.AlignCenter | Qt.AlignBottom)
        layout.addWidget(self.appleTankWidget, 0, Qt.AlignCenter)

        # TANK OBJ HERE ##############
        self.appleTank = appleTank
        # TANK OBJ HERE ##############
        self.update()

        #############button clicked events################
        self.appleControllerWidget.refillButton.clicked.connect(self.refill)
        self.appleControllerWidget.concentrateButton.clicked.connect(self.concentrate)

    # Update the GUI
    def update(self):
        """Update the GUI based on the target values and actual values"""
        currentLevel = self.appleTank.getCurrentLevel()
        currentConcentration = self.appleTank.getConcentration()
        # check if level target values are set
        if self.appleControllerWidget.targetLevel is not None:
            # check if actual values less than target values
            if currentLevel < self.appleControllerWidget.targetLevel:
                self.appleTank.setCurrentLevel(currentLevel + 1)
            else:
                self.appleTank.setCurrentLevel(currentLevel - 1)
        # check if concentration target values are set
        if self.appleControllerWidget.targetConcentration is not None:
            if currentConcentration < self.appleControllerWidget.targetConcentration:
                self.appleTank.setConcentration(currentConcentration + 1)
            else:
                self.appleTank.setConcentration(currentConcentration - 1)

        # if target values are reached, set target values to None
        if self.appleControllerWidget.targetLevel == currentLevel:
            print("target apple level target reached")
            self.appleControllerWidget.targetLevel = None
            self.appleControllerWidget.refillButton.enable()
        if self.appleControllerWidget.targetConcentration == currentConcentration:
            print("target apple concentration target reached")
            self.appleControllerWidget.targetConcentration = None
            self.appleControllerWidget.concentrateButton.enable()

        # update widgets to actual values
        self.appleTankWidget.level = currentLevel
        self.appleMonitorWidget.concentration = currentConcentration

    # FOR SETTING TARGET VALUES
    def setLevelTarget(self, value):
        """Set the target level of the apple tank"""
        self.appleControllerWidget.targetLevel = value

    def setConcentrationTarget(self, value):
        """Set the target purity of the apple tank"""
        self.appleControllerWidget.targetConcentration = value

    def refill(self):
        """Refill the apple tank - for refill button"""
        self.setLevelTarget(100)
        self.appleControllerWidget.refillButton.disable()
    
    def concentrate(self):
        """Concentrate the apple tank - for concentrate button"""
        self.setConcentrationTarget(100)
        self.appleControllerWidget.concentrateButton.disable()


#
# Widget for Tank GUI
#
class AppleTankWidget(QWidget):
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
        painter.setBrush(QColor(255, 79, 79, 75))  # Apple red
        painter.setPen(Qt.NoPen)

        # rect dimensions
        mod = 3  # modifier x number of pixels per percentq
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
            print("Apple Tank Overflow")
        elif self._level < 0:
            self._level = 0
            print("Apple Tank Underflow")
        # change level
        self.update()


#
# Widget for Monitor GUI
#
class AppleMonitorWidget(QFrame):
    def __init__(self):
        super().__init__()

        # info
        self._concentration = 0

        # frame
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)
        self.setFixedHeight(75)
        self.setMaximumWidth(200)

        # label
        self.concentrationLabel = QLabel()
        self.concentrationLabel.setStyleSheet(
            """
            *{
            color: black;
            font-size: 15px;
            }
            """
        )
        self.concentrationLabel.setText(
            f"Apple Concentration: \n{self._concentration} %"
        )
        self.concentrationLabel.setAlignment(Qt.AlignCenter)

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.concentrationLabel, 0, Qt.AlignCenter)

    # Getter
    @property
    def concentration(self):
        return self._concentration

    # Setter
    @concentration.setter
    def concentration(self, value):
        self._concentration = value
        self.concentrationLabel.setText(
            f"Apple Concentration: \n{self._concentration} %"
        )


#
# widget for Controllers
#
class AppleControllerWidget(QWidget):
    def __init__(self):
        super().__init__()
        # target values
        self._targetLevel = None
        self._targetConcentration = None

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.refillButton = QPushButton("REFILL")

        self.concentrateButton = QPushButton("CONCENTRATE")
        # add widgets to layout
        layout.addWidget(self.concentrateButton, 0, Qt.AlignTop | Qt.AlignCenter)
        layout.addWidget(self.refillButton, 0, Qt.AlignBottom | Qt.AlignCenter)

    # getters and setters
    @property
    def targetLevel(self):
        return self._targetLevel
    
    @targetLevel.setter
    def targetLevel(self, value):
        self._targetLevel = value

    @property
    def targetConcentration(self):
        return self._targetConcentration
    
    @targetConcentration.setter
    def targetConcentration(self, value):
        self._targetConcentration = value
    

