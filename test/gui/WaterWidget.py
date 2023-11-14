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


#
# Main widget for Water
#
class WaterWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.waterTankWidget = WaterTankWidget()
        self.waterMonitorWidget = WaterMonitorWidget()
        self.waterControllerWidget = WaterControllerWidget()

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

    # Set the levels (PASS IN VALUES HERE)
    def changeLevels(self, value):
        self.waterTankWidget.level = value

    # Set the purity (PASS IN VALUES HERE)
    def changePurity(self, value):
        self.waterMonitorWidget.purity = value


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

        # layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # buttons
        self.button = QPushButton("REFILL TANK")
        self.button.setCursor(Qt.PointingHandCursor)
        self.button.setStyleSheet(
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

        # add widgets to layout
        layout.addWidget(self.button, 0, Qt.AlignBottom | Qt.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WaterWidget()
    win.show()
    sys.exit(app.exec())
