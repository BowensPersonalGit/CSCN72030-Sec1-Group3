# Apple widget
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QDialog
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

from .buttons import Button
from .graph import Graph, GraphWindow
from .file_reader import readFromFile
from .InputDialog import InputDialog

from AppleTank import AppleTank


class AppleWidget(QFrame):
    """Main widget for Apple"""

    def __init__(self, appleTank: AppleTank):
        """Creates a apple widget with an apple tank object"""
        super().__init__()
        # init widgets
        self._appleDrawingWidget = AppleDrawingWidget()
        self._appleLabelWidget = AppleLabelWidget()
        self._appleButtonWidget = AppleButtonWidget()

        # TANK OBJ HERE ##############
        self.appleTank = appleTank
        # TANK OBJ HERE ##############

        # displayed values
        self._displayedLevel = self.appleTank.getCurrentLevel()
        self._displayedConcentration = self.appleTank.getConcentration()

        # target values, set to None if no target
        self._targetLevel = None
        self._targetConcentration = None

        # graph obj with data
        self._concentrationGraph = Graph(
            "Apple Concentration",
            readFromFile(self.appleTank.appleMonitor.sourceNames[1]),
        )

        # init UI
        self.initUI()
        self.update()

        #############button clicked events################
        self._appleButtonWidget.refillButton.clicked.connect(self.refill)
        self._appleButtonWidget.concentrateButton.clicked.connect(self.concentrate)

    def initUI(self):
        """Initialize the UI"""
        # set frame properties
        self.setStyleSheet("background-color: rgb(216, 216, 214);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)
        # define layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # add widgets to layout
        layout.addWidget(self._appleLabelWidget, 0, Qt.AlignCenter)
        layout.addWidget(self._appleButtonWidget, 0, Qt.AlignCenter | Qt.AlignBottom)
        layout.addWidget(self._appleDrawingWidget, 0, Qt.AlignCenter)

    def showConcentrationGraph(self):
        """Show the concentration graph"""
        self._graphWindow = GraphWindow(self._concentrationGraph)
        return self._graphWindow.show()

    # Update the GUI
    def update(self):
        """Update the GUI based on the target values and actual values"""
        # get actual values from tank class
        self._displayedLevel = self.appleTank.getCurrentLevel()
        self._displayedConcentration = self.appleTank.getConcentration()

        # meet target values
        self.meetTargets()

        # update widgets to actual values
        self._appleDrawingWidget.level = self._displayedLevel
        self._appleLabelWidget.concentrationLabelValue = self._displayedConcentration

        # update graph with displayed values
        self._concentrationGraph.update(self._displayedConcentration)

    def meetTargets(self):
        """checks if target values are set and meets them by incrementing or decrementing the actual values"""
        # check if target values are set
        if self._targetLevel is not None:
            if int(self._displayedLevel) < self._targetLevel:
                # increment to meet target
                self.appleTank.setCurrentLevel(self._displayedLevel + 1)
            elif int(self._displayedLevel) > self._targetLevel:
                # decrement to meet target
                self.appleTank.setCurrentLevel(self._displayedLevel - 1)
            else:  # target met
                print("target apple level target reached")
                self._targetLevel = None
                self._appleButtonWidget.refillButton.enable()
                self._appleButtonWidget.refillButton.setText("REFILL APPLES")

        if self._targetConcentration is not None:
            if int(self._displayedConcentration) < self._targetConcentration:
                self.appleTank.concentrate()
            elif int(self._displayedConcentration) > self._targetConcentration:
                self.appleTank.dilute()
            else:  # target met
                print("target apple concentration target reached")
                self._targetConcentration = None
                self._appleButtonWidget.concentrateButton.enable()
                self._appleButtonWidget.concentrateButton.setText("CONCENTRATE APPLES")

    def refill(self):
        """Refill the apple tank - for refill button"""
        # pop up input dialog
        self.inputDialog = InputDialog(
            "Apple Refill",
            "Enter the amount of apples to refill",
            int(self._displayedLevel),
        )
        result = self.inputDialog.exec_()
        if result == QDialog.Accepted:
            # set target level
            self._targetLevel = self.inputDialog.value
            # disable button
            self._appleButtonWidget.refillButton.disable()
            self._appleButtonWidget.refillButton.setText("REFILLING...")

    def concentrate(self):
        """Concentrate the apple tank - for concentrate button"""
        # pop up input dialog
        self.inputDialog = InputDialog(
            "Apple Concentrate",
            "Enter the amount of apples to concentrate",
            int(self._displayedConcentration),
        )
        result = self.inputDialog.exec_()
        if result == QDialog.Accepted:
            # set target concentration
            self._targetConcentration = self.inputDialog.value
            # disable button
            self._appleButtonWidget.concentrateButton.disable()
            self._appleButtonWidget.concentrateButton.setText("CONCENTRATING...")


class AppleDrawingWidget(QWidget):
    """Widget for Apple level graphic"""

    def __init__(self):
        """Creates an apple level graphic widget"""
        super().__init__()
        # properties
        self.l = 300  # length of tank drawing
        self.w = 50  # width of tank drawing
        self._level = 0  # determines the level of the tank 0 - 100

        self.initUI()

    def initUI(self):
        """Initialize the UI"""
        self.setMinimumSize(150, 400)
        self.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel()
        self.label.setStyleSheet("font-size: 12px;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.label, 0, Qt.AlignBottom | Qt.AlignCenter)

    def paintEvent(self, event):
        """repaints the widget - trigered by update()"""
        painter = QPainter(self)

        # draw liquid
        self.drawLiquid(painter)
        # draw tank
        self.drawTank(painter)

        self.label.setText(f"Apple Tank: {self._level}%")

    def drawTank(self, painter):
        """Draw the tank"""
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

    def drawLiquid(self, painter):
        """Draw the liquid"""
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
        """Set the level and update the widget"""
        self._level = value
        # level value check
        if self._level > 100:
            self._level = 100
            print("Apple Tank Overflow")
        elif self._level < 0:
            self._level = 0
            print("Apple Tank Underflow")

        self.update()  # calls the paintEvent() function


class AppleLabelWidget(QFrame):
    """Widget for Apple stats"""

    def __init__(self):
        """Creates an apple stats widget"""
        super().__init__()

        # info
        self._concentrationLabelValue = 0

        self.initUI()

    def initUI(self):
        """Initialize the UI"""
        # frame
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)
        self.setFixedHeight(75)
        self.setMaximumWidth(200)
        self.setToolTip("Double click to view graph")

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
            f"Apple Concentration: \n{self._concentrationLabelValue} %"
        )
        self.concentrationLabel.setAlignment(Qt.AlignCenter)

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.concentrationLabel, 0, Qt.AlignCenter)

    def mouseDoubleClickEvent(self, event):
        """Event for double clicking the widget - calls parent functions to show graphs"""
        # show concentration graph
        self.parent().showConcentrationGraph()

    # Getter
    @property
    def concentrationLabelValue(self):
        return self._concentrationLabelValue

    # Setter
    @concentrationLabelValue.setter
    def concentrationLabelValue(self, value):
        """Set the concentration label value and update the label"""
        self._concentrationLabelValue = value
        self.concentrationLabel.setText(
            f"Apple Concentration: \n{self._concentrationLabelValue} %"
        )


class AppleButtonWidget(QWidget):
    """Widget for Apple buttons/controls"""

    def __init__(self):
        """Creates apple buttons widget"""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the UI"""
        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.refillButton = Button("REFILL APPLES")
        self.concentrateButton = Button("CONCENTRATE APPLES")

        # add widgets to layout
        layout.addWidget(self.concentrateButton, 0, Qt.AlignTop | Qt.AlignCenter)
        layout.addWidget(self.refillButton, 0, Qt.AlignBottom | Qt.AlignCenter)
