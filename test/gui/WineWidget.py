# Wine widget
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QDialog
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

from .warning_popup import showPopup
from .buttons import Button
from .InputDialog import InputDialog
from .graph import Graph, GraphWindow


from WineTank import WineTank


class WineWidget(QFrame):
    """Main widget for Wine"""

    def __init__(self, wineTank: WineTank):
        """Creates a wine widget with a wine tank object"""
        super().__init__()
        # init widgets
        self._wineDrawingWidget = WineDrawingWidget()
        self._wineLabelWidget = WineLabelWidget()
        self._wineButtonWidget = WineButtonWidget()

        # TANK OBJ HERE ##############
        self.wineTank = wineTank
        # TANK OBJ HERE ##############

        # displayed values
        self._displayedLevel = self.wineTank.getCurrentLevel()
        self._displayedPressure = self.wineTank.getPressure()
        self._displayedAlcohol = self.wineTank.getAlcohol()

        # target values, set to None if no target
        self._targetLevel = None
        self._targetPressure = None
        self._targetAlcohol = None

        # function states
        self._refillState = False
        self._dumpState = False
        self._fermentState = False

        # graph obj with data
        # TODO: add graph here

        # init UI
        self.initUI()
        self.update()

        #############button clicked events################
        self._wineButtonWidget.fermentButton.clicked.connect(self.ferment)
        self._wineButtonWidget.refillButton.clicked.connect(self.refill)
        self._wineButtonWidget.dumpButton.clicked.connect(self.dumpAll)

    def initUI(self):
        """Initialize the UI"""
        # set frame properties
        self.setStyleSheet("background-color: rgb(216, 216, 214);")
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)
        # define layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # add widgets to layout
        layout.addWidget(self._wineLabelWidget, 0, Qt.AlignCenter)
        layout.addWidget(self._wineButtonWidget, 0, Qt.AlignCenter | Qt.AlignBottom)
        layout.addWidget(self._wineDrawingWidget, 0, Qt.AlignCenter)

    def update(self):
        """Update the GUI based on the target values and actual values"""
        # get actual values from tank class
        self._displayedLevel = self.wineTank.getCurrentLevel()
        self._displayedPressure = self.wineTank.getPressure()
        self._displayedAlcohol = self.wineTank.getAlcohol()

        # meet targets values
        self.meetTargets()

        # update widgets to actual values
        self._wineDrawingWidget.level = self._displayedLevel
        self._wineLabelWidget.pressure = self._displayedPressure
        self._wineLabelWidget.alcohol = self._displayedAlcohol

        # update graph with displayed values
        # TODO: implemtn graph
        # self._somethingGraph.update(somrthign)

    def meetTargets(self):
        """checks if target values are set and meets them by incrementing or decrementing the actual values"""
        # check if target values are set
        if self._targetLevel is not None:
            if int(self._displayedLevel) < self._targetLevel:
                # take from grapes and water
                self.wineTank.takeGrape(1)
                self.wineTank.takeWater(1)
            elif int(self._displayedLevel) > self._targetLevel:
                self.wineTank.setCurrentLevel(self._displayedLevel - 1)
            else:
                print("target wine level target reached")
                self._targetLevel = None
                if self._dumpState is False:
                    self._wineButtonWidget.enableAllButtons()
                    self._wineButtonWidget.refillButton.setText("REFILL WINE")
                    self._refillState = False

        if self._targetPressure is not None:
            if int(self._displayedPressure) < self._targetPressure:
                self.wineTank.setPressure(self._displayedPressure + 1)
            elif int(self._displayedPressure) > self._targetPressure:
                self.wineTank.setPressure(self._displayedPressure - 1)
            else:
                print("target wine pressure target reached")
                self._targetPressure = None

        if self._targetAlcohol is not None:
            if int(self._displayedAlcohol) < self._targetAlcohol:
                self.wineTank.setAlcohol(self._displayedAlcohol + 1)
            elif int(self._displayedAlcohol) > self._targetAlcohol:
                self.wineTank.setAlcohol(self._displayedAlcohol - 1)
            else:
                print("target wine alcohol target reached")
                self._targetAlcohol = None
                if self._dumpState is False:
                    self._wineButtonWidget.enableAllButtons()
                    self._wineButtonWidget.fermentButton.setText("FERMENT WINE")
                    self._fermentState = False

        # check for dump all
        if (
            self._dumpState is True
            and self._displayedLevel == 0
            and self._displayedPressure == 0
            and self._displayedAlcohol == 0
        ):
            print("dump all sucess")
            self._wineButtonWidget.enableAllButtons()
            self._wineButtonWidget.dumpButton.setText("DUMP ALL")
            self._dumpState = False

    def refill(self):
        """Refill the wine tank - for refill button"""
        self.inputDialog = InputDialog(
            "Refill Wine", "Enter amount of wine to refill", int(self._displayedLevel)
        )
        result = self.inputDialog.exec_()
        if result == QDialog.Accepted:
            # check if there is enough grapes and water
            if self.wineTank.checkGrape((self.inputDialog.value - self._displayedLevel) / 2) is False:
                showPopup("WARNING", "Not enough grapes")
            elif self.wineTank.checkWater((self.inputDialog.value -self._displayedLevel)  / 2) is False:
                showPopup("WARNING", "Not enough water")
            else:
                self._targetLevel = self.inputDialog.value
                self._wineButtonWidget.disableAllButtons()
                self._wineButtonWidget.refillButton.setText("REFILLING")
                self._refillState = True

    def ferment(self):
        """Ferment Wine - for refill button"""

        self.inputDialog = InputDialog(
            "Ferment Wine",
            "Enter the alcohol target amount",
            int(self._displayedAlcohol),
        )
        result = self.inputDialog.exec_()
        if result == QDialog.Accepted:
            self._targetAlcohol = self.inputDialog.value
            # TODO: implement pressure level
            self._targetPressure = self.inputDialog.value / 2
            self._wineButtonWidget.disableAllButtons()
            self._wineButtonWidget.fermentButton.setText("FERMENTING")
            self._fermentState = True

    def dumpAll(self):
        """Dump all wine - for dump button"""
        self._targetLevel = 0
        self._targetPressure = 0
        self._targetAlcohol = 0
        self._wineButtonWidget.disableAllButtons()
        self._wineButtonWidget.dumpButton.setText("DUMPING")
        self._dumpState = True


class WineDrawingWidget(QWidget):
    """Widget for wine tank level graphic"""

    def __init__(self):
        super().__init__()
        # properties
        self.l = 500  # length of tank drawing
        self.w = 200  # width of tank drawing
        self._levelValue = 0  # determines the level of the tank 0 - 100

        self.initUI()

    def initUI(self):
        """Initialize the UI"""
        self.setMinimumSize(300, 600)
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
        self.label.setText(f"Wine Tank: {self._levelValue}%")

    def drawTank(self, painter):
        """draw the tank"""
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
        """draw the liquid"""
        # color
        painter.setBrush(QColor(120, 24, 48, 75))  # Wine red
        painter.setPen(Qt.NoPen)

        # rect dimensions
        mod = 5
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
    def level(self):
        return self._levelValue

    # Setter - use to change level plz
    @level.setter
    def level(self, value):
        """Set the level value and update the widget"""
        self._levelValue = value
        # level value check
        if self._levelValue > 100:
            self._levelValue = 100
            print("Wine Tank Overflow")
        elif self._levelValue < 0:
            self._levelValue = 0
            print("Wine Tank Underflow")

        self.update()  # calls the paintEvent() function


class WineLabelWidget(QFrame):
    """Widget for wine info"""

    def __init__(self):
        super().__init__()

        # info
        self._pressureLabelValue = 0
        self._alcoholLabelValue = 0

        self.initUI()

    def initUI(self):
        """Initialize the UI"""
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
        self.pressureLabel.setText(f"Wine Pressure: \n {self._pressureLabelValue} psi")
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
        self.alcoholLabel.setText(f"Wine Alcohol: \n {self._alcoholLabelValue} %")
        self.alcoholLabel.setAlignment(Qt.AlignCenter)

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # add widgets to layout
        layout.addWidget(self.pressureLabel, 0, Qt.AlignCenter)
        layout.addWidget(self.alcoholLabel, 0, Qt.AlignCenter)

    def mouseDoubleClickEvent(self, event):
        """Event for double clicking the widget"""
        # show graphs
        # TODO: implement graph
        # self.parent().showsomethingGraph()

    @property
    def pressure(self):
        return self._pressureLabelValue

    @pressure.setter
    def pressure(self, value):
        """Set the pressure label value and update the widget"""
        self._pressureLabelValue = value
        self.pressureLabel.setText(f"Wine Pressure: \n {self._pressureLabelValue} psi")

    @property
    def alcohol(self):
        return self._alcoholLabelValue

    @alcohol.setter
    def alcohol(self, value):
        """Set the alcohol label value and update the widget"""
        self._alcoholLabelValue = value
        self.alcoholLabel.setText(f"Wine Alcohol: \n {self._alcoholLabelValue} %")


class WineButtonWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.refillButton = Button("REFILL WINE")
        self.dumpButton = Button("DUMP ALL")
        self.fermentButton = Button("FERMENT WINE")

        # add widgets to layout
        layout.addWidget(self.fermentButton, 0, Qt.AlignTop | Qt.AlignCenter)
        layout.addWidget(self.dumpButton, 0, Qt.AlignBottom | Qt.AlignCenter)
        layout.addWidget(self.refillButton, 0, Qt.AlignBottom | Qt.AlignCenter)

    def disableAllButtons(self):
        """Disable all buttons"""
        self.refillButton.disable()
        self.dumpButton.disable()
        self.fermentButton.disable()

    def enableAllButtons(self):
        """Enable all buttons"""
        self.refillButton.enable()
        self.dumpButton.enable()
        self.fermentButton.enable()
