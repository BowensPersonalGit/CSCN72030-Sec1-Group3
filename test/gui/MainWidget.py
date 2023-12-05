# this will the main window widget for the application
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
)
from PyQt5.QtCore import Qt, QTimer

# import WIDGETS
from .WaterWidget import WaterWidget
from .WineWidget import WineWidget
from .CiderWidget import CiderWidget
from .GrapeWidget import GrapeWidget
from .AppleWidget import AppleWidget

# import TANKS
from WaterTank import WaterTank
from AppleTank import AppleTank
from CiderTank import CiderTank
from WineTank import WineTank
from grapeTank import GrapeTank

waterLevelFile = "./test/water_levels.txt"
waterPurityFile = "./test/water_puritys.txt"
appleLevelFile = "./test/apple_levels.txt"
appleConcentrationFile = "./test/apple_concentration.txt"
grapeLevelFile = "./test/grapeLevel.txt"
grapeBacteriaFile = "./test/grapeBacteria.txt"


#
# Main widget for the application
#
class MainWidget(QFrame):
    def __init__(self):
        """Main widget for the application"""
        super().__init__()
        # tank objects###################
        self.waterTank = WaterTank([waterLevelFile, waterPurityFile])
        self.appleTank = AppleTank([appleLevelFile, appleConcentrationFile])
        self.ciderTank = CiderTank()
        self.wineTank = WineTank()
        self.grapeTank = GrapeTank(grapeLevelFile, grapeBacteriaFile)
        # tank objects###################

        self.initUI()

    def initUI(self):
        """Initialize UI elements"""
        # window properties
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("BrewMaster")

        # frame properties
        self.setStyleSheet("background-color: rgb(76, 99, 83);")

        # layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        # widgets
        self.waterWidget = WaterWidget(self.waterTank)
        self.wineWidget = WineWidget(self.wineTank)
        self.ciderWidget = CiderWidget(self.ciderTank)
        self.appleWidget = AppleWidget(self.appleTank)
        self.grapeWidget = GrapeWidget(self.grapeTank)

        # add widgets to layout
        layout.addWidget(self.appleWidget)
        layout.addWidget(self.ciderWidget)
        layout.addWidget(self.waterWidget)
        layout.addWidget(self.wineWidget)
        layout.addWidget(self.grapeWidget)

    def update(self):
        """Update all the widgets in the main widget"""
        print("MainWidget.update()")
        self.waterWidget.update()
        self.wineWidget.update()
        self.ciderWidget.update()
        self.appleWidget.update()
        self.grapeWidget.update()
