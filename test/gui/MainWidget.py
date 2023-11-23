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
#from .GrapeWidget import GrapeWidget
from .AppleWidget import AppleWidget

# import TANKS
from WaterTank import WaterTank
from AppleTank import AppleTank
from CiderTank import CiderTank
from WineTank import WineTank


#
# Main widget for the application
#
class MainWidget(QFrame):
    def __init__(self):
        super().__init__()

        # window properties
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("BrewMaster")

        # frame properties
        self.setStyleSheet("background-color: rgb(76, 99, 83);")

        # layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        # widgets
        self.waterWidget = WaterWidget(
            WaterTank(["./test/water_levels.txt", "./test/water_puritys.txt"])
        )
        self.wineWidget = WineWidget(WineTank())
        self.ciderWidget = CiderWidget(CiderTank())
        self.appleWidget = AppleWidget(
            AppleTank(["./test/apple_levels.txt", "./test/apple_concentration.txt"])
        )
        # self.grapeWidget = GrapeWidget()

        # add widgets to layout
        layout.addWidget(self.appleWidget)
        layout.addWidget(self.ciderWidget)
        layout.addWidget(self.waterWidget)
        layout.addWidget(self.wineWidget)
        #layout.addWidget(self.grapeWidget)

    def update(self):
        """Update all the widgets in the main widget"""
        print("MainWidget.update()")
        self.waterWidget.update()
        self.wineWidget.update()
        self.ciderWidget.update()
        self.appleWidget.update()
        # self.grapeWidget.update()
