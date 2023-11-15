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

# relative path for imports
if __name__ != "__main__":
    from .WaterWidget import WaterWidget
    from .WineWidget import WineWidget
    from .CiderWidget import CiderWidget
    from .GrapeWidget import GrapeWidget
    from .AppleWidget import AppleWidget


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
        self.waterWidget = WaterWidget()
        self.wineWidget = WineWidget()
        self.ciderWidget = CiderWidget()
        self.appleWidget = AppleWidget()
        self.grapeWidget = GrapeWidget()

        # add widgets to layout
        layout.addWidget(self.appleWidget)
        layout.addWidget(self.ciderWidget)
        layout.addWidget(self.waterWidget)
        layout.addWidget(self.wineWidget)
        layout.addWidget(self.grapeWidget)


if __name__ == "__main__":
    # test code
    from WaterWidget import WaterWidget
    from WineWidget import WineWidget
    from CiderWidget import CiderWidget
    from GrapeWidget import GrapeWidget
    from AppleWidget import AppleWidget

    app = QApplication(sys.argv)
    win = MainWidget()
    win.show()

    counter = 0

    def increment_level():
        global counter
        win.waterWidget.changeLevels(counter)
        win.wineWidget.changeLevels(counter)
        win.ciderWidget.changeLevels(counter)
        win.appleWidget.changeLevels(counter)
        win.grapeWidget.changeLevels(counter)
        counter += 5

    # Create a QTimer
    timer = QTimer()
    timer.timeout.connect(
        increment_level
    )  # Connect timeout signal to increment_level slot
    timer.start(1000)  # Set the timer to time out every second

    sys.exit(app.exec())
