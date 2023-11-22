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


#
# Main widget for Apple
#
class AppleWidget(QFrame):
    def __init__(self):
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

    # Set the levels (PASS IN VALUES HERE)
    def changeLevels(self, value):
        if value <= 100:
            self.appleTankWidget.level = value

    # Set the concentration (PASS IN VALUES HERE)
    def changeConcentration(self, value):
            self.appleMonitorWidget.concentration = 22


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

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.refillButton = QPushButton("REFILL TANK")
        self.refillButton.setCursor(Qt.PointingHandCursor)

        self.refillButton.setStyleSheet(
            """
            *{
            background-color: rgb(47, 93, 140);
            color: black;
            font-size: 20px;
            border-radius: 20px;
            padding: 10px 20px;
            }
            *:hover{
                background: rgb(213, 94, 45);
                }
            """
        )

        # monitor concentration button
        self.monitorConcentrationButton = QPushButton("MONITOR CONCENTRATION")
        self.monitorConcentrationButton.setCursor(Qt.PointingHandCursor)

        self.monitorConcentrationButton.setStyleSheet(
            """
            *{
            background-color: rgb(47, 93, 140);
            color: black;
            font-size: 20px;
            border-radius: 20px;
            padding: 10px 20px;
            }
            *:hover{
                background: rgb(213, 94, 45);
                }
            """
        )

        # connect button to refill tank
        self.refillButton.clicked.connect(self.refillTank)

        # add widgets to layout
        layout.addWidget(self.refillButton, 0, Qt.AlignBottom | Qt.AlignCenter)
        layout.addWidget(self.monitorConcentrationButton, 0, Qt.AlignBottom | Qt.AlignCenter)


    def refillTank(self):
        tank_value = 80; 
        parent_widget = self.parent()
        if parent_widget:
            monitor_widget = parent_widget.appleTankWidget
            monitor_widget.level = tank_value

 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppleWidget()
    win.show()
    sys.exit(app.exec())
