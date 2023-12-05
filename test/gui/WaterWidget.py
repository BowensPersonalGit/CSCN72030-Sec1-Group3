# Water widget
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QDialog
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

from .buttons import Button
from .graph import Graph, GraphWindow
from .file_reader import readFromFile
from .InputDialog import InputDialog

from WaterTank import WaterTank


#
# Main widget for Water
#
class WaterWidget(QFrame):
    """Main widget for Water"""

    def __init__(self, waterTank: WaterTank):
        """Creates a water widget with a water tank object"""
        super().__init__()
        # init widgets
        self._waterDrawingWidget = WaterDrawingWidget()
        self._waterLabelWidget = WaterLabelWidget()
        self._waterButtonWidget = WaterButtonWidget()

        # TANK OBJ HERE ##############
        self.waterTank = waterTank
        # TANK OBJ HERE ##############

        # displayed values
        self._displayedLevel = self.waterTank.getCurrentLevel()
        self._displayedPurity = self.waterTank.getPurity()

        # target values, set to None if no target
        self._targetLevel = None
        self._targetPurity = None

        # graph obj with data
        self._purityGraph = Graph(
            "Water Purity", readFromFile(self.waterTank.waterMonitor.sourceNames[1])
        )

        # init UI
        self.initUI()
        self.update()

        #############button clicked events################
        self._waterButtonWidget.refillButton.clicked.connect(self.refill)
        self._waterButtonWidget.purifyButton.clicked.connect(self.purify)

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
        layout.addWidget(self._waterLabelWidget, 0, Qt.AlignCenter)
        layout.addWidget(self._waterButtonWidget, 0, Qt.AlignCenter | Qt.AlignBottom)
        layout.addWidget(self._waterDrawingWidget, 0, Qt.AlignCenter)

    def showPurityGraph(self):
        """Show the purity graph - creates and shows a new widget"""
        self._graphWindow = GraphWindow(self._purityGraph)
        return self._graphWindow.show()

    # Update the GUI
    def update(self):
        """Update the GUI based on the target values and actual values"""
        # get actual values from tank class
        self._displayedLevel = self.waterTank.getCurrentLevel()
        self._displayedPurity = self.waterTank.getPurity()

        # meet target values
        self.meetTargets()

        # update widgets to actual values
        self._waterDrawingWidget.levelValue = self._displayedLevel
        self._waterLabelWidget.purityLabelValue = self._displayedPurity

        # update graph with displayeed values
        self._purityGraph.update(self._displayedPurity)

    def meetTargets(self):
        """checks if target values are set and meets them by incrementing or decrementing the actual values"""
        # check if target values are set
        if self._targetLevel is not None:  # level
            if self._displayedLevel < self._targetLevel:
                # increment to meet target
                self.waterTank.setCurrentLevel(self._displayedLevel + 1)
            elif self._displayedLevel > self._targetLevel:
                # decrement to meet target
                self.waterTank.setCurrentLevel(self._displayedLevel - 1)
            else: # target reached
                print("target water level target reached")
                self._targetLevel = None
                self._waterButtonWidget.refillButton.enable()
                self._waterButtonWidget.refillButton.setText("REFILL WATER")
        
        if self._targetPurity is not None:  # purity
            if self._displayedPurity < self._targetPurity:
                # increment to meet target
                self.waterTank.setPurity(self._displayedPurity + 1)
            elif self._displayedPurity > self._targetPurity:
                # decrement to meet target
                self.waterTank.setPurity(self._displayedPurity - 1)
            else:
                print("target water purity target reached")
                self._targetPurity = None
                self._waterButtonWidget.purifyButton.enable()
                self._waterButtonWidget.purifyButton.setText("PURIFY WATER")

    def refill(self):
        """Refill the water tank - for refill button"""
        # popup dialog to get target water level
        self.inputDialog = InputDialog("Refill Water", "Enter the target water level", int(self._displayedLevel))
        result = self.inputDialog.exec_()
        if result == QDialog.Accepted:
            # set target water level
            self._targetLevel = self.inputDialog.value
            self._waterButtonWidget.refillButton.disable()
            self._waterButtonWidget.refillButton.setText("REFILLING")  

    def purify(self):
        """Purify the water tank - for purify button"""
        # popup dialog to get target water purity
        self.inputDialog = InputDialog("Purify Water", "Enter the target water purity", int(self._displayedPurity))
        result = self.inputDialog.exec_()
        if result == QDialog.Accepted:
            # set target water purity
            self._targetPurity = self.inputDialog.value
            self._waterButtonWidget.purifyButton.disable()
            self._waterButtonWidget.purifyButton.setText("PURIFYING")

class WaterDrawingWidget(QWidget):
    """Widget for Water Level grahic"""
    def __init__(self):
        """creates a water level widget"""
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
        self.label.setText(f"Water Tank: {self._levelValue}%")

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
        painter.setBrush(QColor(29, 114, 219, 75))  # Water blue
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
            print("Water Tank Overflow")
        elif self._levelValue < 0:
            self._levelValue = 0
            print("Water Tank Underflow")

        self.update()  # calls the paintEvent() function


class WaterLabelWidget(QFrame):
    """Widget for Water stats"""

    def __init__(self):
        """Creates a water stats widget"""
        super().__init__()

        # info
        self._purityLabelValue = 0

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
        self.purityLabel.setText(f"Water Purity: \n {self._purityLabelValue} %")
        self.purityLabel.setAlignment(Qt.AlignCenter)

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.purityLabel, 0, Qt.AlignCenter)

    def mouseDoubleClickEvent(self, event):
        """Event for double clicking the widget - calls parent functions to show graphs"""
        # show purity graph
        self.parent().showPurityGraph()

    @property
    def purityLabelValue(self):
        return self._purityLabelValue

    @purityLabelValue.setter
    def purityLabelValue(self, value):
        """Set the purity label value and update the widget"""
        self._purityLabelValue = value
        self.purityLabel.setText(f"Water Purity: \n {self._purityLabelValue} %")


class WaterButtonWidget(QWidget):
    """Widget for Water buttons/controls"""

    def __init__(self):
        """Creates water buttons widget"""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initialize the UI"""
        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.refillButton = Button("REFILL WATER")
        self.purifyButton = Button("PURIFY WATER")

        # add widgets to layout
        layout.addWidget(self.purifyButton, 0, Qt.AlignTop | Qt.AlignCenter)
        layout.addWidget(self.refillButton, 0, Qt.AlignBottom | Qt.AlignCenter)
