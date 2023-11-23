# Water widget
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

from WaterTank import WaterTank


#
# Main widget for Water
#
class WaterWidget(QFrame):
    def __init__(self, waterTank: WaterTank):
        super().__init__()
        # create widgets
        self.waterTankWidget = WaterTankWidget()
        self.waterMonitorWidget = WaterMonitorWidget()
        self.waterControllerWidget = WaterControllerWidget()
        # set frame properties
        self.setStyleSheet("background-color: rgb(216, 216, 214);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)

        # define layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.waterMonitorWidget, 0, Qt.AlignCenter)
        layout.addWidget(self.waterControllerWidget, 0, Qt.AlignCenter | Qt.AlignBottom)
        layout.addWidget(self.waterTankWidget, 0, Qt.AlignCenter)

        # TANK OBJ HERE ##############
        self.waterTank = waterTank
        self.update()

        #############button clicked events################
        self.waterControllerWidget.refillButton.clicked.connect(self.refill)
        self.waterControllerWidget.purifyButton.clicked.connect(self.purify)

    # Update the GUI
    def update(self):
        """Update the GUI based on the target values and actual values"""
        currentLevel = self.waterTank.getCurrentLevel()
        currentPurity = self.waterTank.getPurity()

        # check if level target values are set
        if self.waterControllerWidget.targetLevel is not None:
            # check if actual values less than target values
            if currentLevel < self.waterControllerWidget.targetLevel:
                self.waterTank.setCurrentLevel(currentLevel + 1)
            else:
                self.waterTank.setCurrentLevel(currentLevel - 1)
        # check if purity target values are set
        if self.waterControllerWidget.targetPurity is not None:
            if currentPurity < self.waterControllerWidget.targetPurity:
                self.waterTank.setPurity(currentPurity + 1)
            else:
                self.waterTank.setPurity(currentPurity - 1)

        # if target values are reached, set target values to None
        if self.waterControllerWidget.targetLevel == currentLevel:
            print("target water level target reached")
            self.waterControllerWidget.targetLevel = None
            self.waterControllerWidget.refillButton.enable()

        if self.waterControllerWidget.targetPurity == currentPurity:
            print("target water purity target reached")
            self.waterControllerWidget.targetPurity = None
            self.waterControllerWidget.purifyButton.enable()

        # update widgets to actual values
        self.waterTankWidget.level = currentLevel
        self.waterMonitorWidget.purity = currentPurity

    # FOR SETTING TARGET VALUES
    def setLevelTarget(self, value):
        """Set the target level of the water tank"""
        self.waterControllerWidget.targetLevel = value

    def setPurityTarget(self, value):
        """Set the target purity of the water tank"""
        self.waterControllerWidget.targetPurity = value

    def refill(self):
        """Refill the water tank - for refill button"""
        self.setLevelTarget(100)
        self.waterControllerWidget.refillButton.disable()

    def purify(self):
        """Purify the water tank - for purify button"""
        self.setPurityTarget(100)
        self.waterControllerWidget.purifyButton.disable()


#
# Widget for Tank GUI
#
class WaterTankWidget(QWidget):
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
        painter.setBrush(QColor(29, 114, 219, 75))  # Water blue
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
            print("Water Tank Overflow")
        elif self._level < 0:
            self._level = 0
            print("Water Tank Underflow")

        self.update()


#
# Widget for Monitor GUI
#
class WaterMonitorWidget(QFrame):
    def __init__(self):
        super().__init__()

        # info
        self._purity = 0

        # frame
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)
        self.setFixedHeight(75)
        self.setMaximumWidth(150)

        # label
        self.purityLabel = QLabel()
        self.purityLabel.setStyleSheet(
            """
            *{
            color: black;
            font-size: 15px;
            }
            """
        )
        self.purityLabel.setText(f"Water Purity: \n {self._purity} %")
        self.purityLabel.setAlignment(Qt.AlignCenter)

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.purityLabel, 0, Qt.AlignCenter)

    # Getter
    @property
    def purity(self):
        return self._purity

    # Setter
    @purity.setter
    def purity(self, value):
        self._purity = value
        self.purityLabel.setText(f"Water Purity: \n {self._purity} %")


#
# widget for Controllers
#
class WaterControllerWidget(QWidget):
    def __init__(self):
        super().__init__()
        # target values
        self._targetLevel = None
        self._targetPurity = None

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.refillButton = Button("REFILL WATER")
        self.purifyButton = Button("PURIFY WATER")

        # add widgets to layout
        layout.addWidget(self.purifyButton, 0, Qt.AlignTop | Qt.AlignCenter)
        layout.addWidget(self.refillButton, 0, Qt.AlignBottom | Qt.AlignCenter)

    # getters and setters
    @property
    def targetLevel(self):
        return self._targetLevel

    @targetLevel.setter
    def targetLevel(self, value):
        self._targetLevel = value

    @property
    def targetPurity(self):
        return self._targetPurity

    @targetPurity.setter
    def targetPurity(self, value):
        self._targetPurity = value


