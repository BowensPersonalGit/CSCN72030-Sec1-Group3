# Grape widget
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QDialog
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

from .buttons import Button
from .graph import Graph, GraphWindow
from .file_reader import readFromFile
from .InputDialog import InputDialog

from grapeTank import GrapeTank


class GrapeWidget(QFrame):
    """Main widget for Grape"""

    def __init__(self, grapeTank: GrapeTank):
        """Creates a grape widget with a grape tank object"""
        super().__init__()
        # init widgets
        self._grapeDrawingWidget = GrapeDrawingWidget()
        self._grapeLabelWidget = GrapeLabelWidget()
        self._grapeButtonWidget = GrapeButtonWidget()

        # TANK OBJ HERE ##############
        self.grapeTank = grapeTank
        # TANK OBJ HERE ##############

        # displayed values
        self._displayedLevel = self.grapeTank.getCurrentLevel()
        self._displayedBacteria = self.grapeTank.getBacteriaLevel()

        # target values, set to None if no target
        self._targetLevel = None
        self._targetBacteria = None

        # graph obj with data
        self._bacteriaGraph = Graph(
            "Grape Bacteria Level", readFromFile(self.grapeTank.monitor.Bacteria_File)
        )

        # init UI
        self.initUI()
        self.update()

        #############button clicked events################
        self._grapeButtonWidget.refillButton.clicked.connect(self.refill)
        self._grapeButtonWidget.cleanseButton.clicked.connect(self.cleanse)

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
        layout.addWidget(self._grapeLabelWidget, 0, Qt.AlignCenter)
        layout.addWidget(self._grapeButtonWidget, 0, Qt.AlignCenter | Qt.AlignBottom)
        layout.addWidget(self._grapeDrawingWidget, 0, Qt.AlignCenter)

    def showBacteriaGraph(self):
        """Show the bacteria graph - creates and shows a new widget"""
        self._graphWindow = GraphWindow(self._bacteriaGraph)
        return self._graphWindow.show()

    # Update the GUI
    def update(self):
        """Update the GUI based on the target values and actual values"""
        # get actual values from tank class
        self._displayedLevel = self.grapeTank.getCurrentLevel()
        self._displayedBacteria = self.grapeTank.getBacteriaLevel()

        # meet target values
        self.meetTargets()

        # update widgets to actual values
        self._grapeDrawingWidget.levelValue = self._displayedLevel
        self._grapeLabelWidget.bacteriaLabelValue = self._displayedBacteria

        # update graph with displayeed values
        self._bacteriaGraph.update(self._displayedBacteria)

    def meetTargets(self):
        """checks if target values are set and meets them by incrementing or decrementing the actual values"""
        # check if target values are set
        if self._targetLevel is not None:  # level
            if self._displayedLevel < self._targetLevel:
                # increment to meet target
                self.grapeTank.setCurrentLevel(self._displayedLevel + 1)
            elif self._displayedLevel > self._targetLevel:
                # decrement to meet target
                self.grapeTank.setCurrentLevel(self._displayedLevel - 1)
            else:  # target reached
                print("target grape level target reached")
                self._targetLevel = None
                self._grapeButtonWidget.refillButton.enable()
                self._grapeButtonWidget.refillButton.setText("REFILL GRAPES")

        if self._targetBacteria is not None:  # bacteria
            if self._displayedBacteria < self._targetBacteria:
                # increment to meet target
                self.grapeTank.setBacteriaLevel(self._displayedBacteria + 1)
            elif self._displayedBacteria > self._targetBacteria:
                # decrement to meet target
                self.grapeTank.setBacteriaLevel(self._displayedBacteria - 1)
            else:
                print("target grape bacteria target reached")
                self._targetBacteria = None
                self._grapeButtonWidget.cleanseButton.enable()
                self._grapeButtonWidget.cleanseButton.setText("CLEAN GRAPES")

    def refill(self):
        """Refill the grape tank - for refill button"""
        # popup dialog to get target grape level
        self.inputDialog = InputDialog(
            "Refill Grape", "Enter the target grape level", int(self._displayedLevel)
        )
        result = self.inputDialog.exec_()
        if result == QDialog.Accepted:
            # set target grape level
            self._targetLevel = self.inputDialog.value
            self._grapeButtonWidget.refillButton.disable()
            self._grapeButtonWidget.refillButton.setText("REFILLING")

    def cleanse(self):
        """Purify the grape tank - for purify button"""
        # popup dialog to get target grape bacteria
        self.inputDialog = InputDialog(
            "Purify Grape",
            "Enter the target grape bacteria",
            int(self._displayedBacteria),
        )
        result = self.inputDialog.exec_()
        if result == QDialog.Accepted:
            # set target grape bacteria
            self._targetBacteria = self.inputDialog.value
            self._grapeButtonWidget.cleanseButton.disable()
            self._grapeButtonWidget.cleanseButton.setText("CLEANING")


class GrapeDrawingWidget(QWidget):
    """Widget for Grape Level grahic"""

    def __init__(self):
        """creates a grape level widget"""
        super().__init__()
        # properties
        self.l = 300  # length of tank drawing
        self.w = 50  # width of tank drawing
        self._levelValue = 0  # determines the level of the tank 0 - 100

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
        # update label
        self.label.setText(f"Grape Tank: {self._levelValue}%")

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
        painter.setBrush(QColor(64, 16, 219, 75))  # Grape purple
        painter.setPen(Qt.NoPen)

        # rect dimensions
        mod = 3  # modifier x number of pixels per percent
        l = self._levelValue * mod
        w = self.w
        r = 20

        # coordinates
        x = (self.width() - w) / 2
        y = ((self.height() - self.l) / 2) + (self.l - l)

        # draw
        painter.drawRoundedRect(int(x), int(y), int(w), int(l), r, r)

    # Getter
    @property
    def levelValue(self):
        return self._levelValue

    # Setter - use to change level plz
    @levelValue.setter
    def levelValue(self, value):
        """Set the level value and update the widget"""
        self._levelValue = value

        # level value check
        if self._levelValue > 100:
            self._levelValue = 100
            print("Grape Tank Overflow")
        elif self._levelValue < 0:
            self._levelValue = 0
            print("Grape Tank Underflow")

        self.update()  # calls the paintEvent() function


class GrapeLabelWidget(QFrame):
    """Widget for Grape stats"""

    def __init__(self):
        """Creates a grape stats widget"""
        super().__init__()

        # info
        self._bacteriaLabelValue = 0

        self.initUI()

    def initUI(self):
        """Initialize the UI"""
        # frame
        self.setStyleSheet("background-color: rgb(249, 249, 249);")
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)
        self.setFixedHeight(75)
        self.setMaximumWidth(150)
        self.setToolTip("Double click to view graph")

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
        self.purityLabel.setText(f"Grape Bacteria: \n {self._bacteriaLabelValue} %")
        self.purityLabel.setAlignment(Qt.AlignCenter)

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.purityLabel, 0, Qt.AlignCenter)

    def mouseDoubleClickEvent(self, event):
        """Event for double clicking the widget - calls parent functions to show graphs"""
        # show bacteria graph
        self.parent().showBacteriaGraph()

    @property
    def bacteriaLabelValue(self):
        return self._bacteriaLabelValue

    @bacteriaLabelValue.setter
    def bacteriaLabelValue(self, value):
        """Set the bacteria label value and update the widget"""
        self._bacteriaLabelValue = value
        self.purityLabel.setText(f"Grape Bacteria: \n {self._bacteriaLabelValue} %")


class GrapeButtonWidget(QWidget):
    """Widget for Grape buttons/controls"""

    def __init__(self):
        """Creates grape buttons widget"""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the UI"""
        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.refillButton = Button("REFILL GRAPES")
        self.cleanseButton = Button("CLEAN GRAPES")

        # add widgets to layout
        layout.addWidget(self.cleanseButton, 0, Qt.AlignTop | Qt.AlignCenter)
        layout.addWidget(self.refillButton, 0, Qt.AlignBottom | Qt.AlignCenter)
