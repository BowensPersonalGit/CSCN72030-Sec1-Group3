import sys
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QSlider,
    QLabel,
    QDialogButtonBox,
    QSpinBox,
)
from PyQt5.QtCore import Qt

class InputDialog(QDialog):
    def __init__(self, title: str, description: str, defaultValue: float = 0):
        """A dialog that allows the user to input a value from a slider and/or a line edit"""
        super().__init__()
        self.title = title
        self.description = description
        self.value = defaultValue

        self.initUI()

    def initUI(self):
        """Initialize the UI"""
        # Window properties
        self.setWindowTitle(self.title)
        self.setMinimumSize(300, 100)

        # layout
        self.windowLayout = QVBoxLayout()
        self.setLayout(self.windowLayout)

        # label
        self.label = QLabel(self.description)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setTickInterval(1)
        self.slider.setValue(self.value)

        # spin box
        self.spinBox = QSpinBox()
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(100)
        self.spinBox.setValue(self.value)

        # Button box
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        # add widgets to layout
        self.windowLayout.addWidget(self.label)
        self.windowLayout.addWidget(self.slider)
        self.windowLayout.addWidget(self.spinBox)
        self.windowLayout.addWidget(self.buttonBox)

        # sync slider and line edit
        self.slider.valueChanged.connect(self.syncLineEdit)
        self.spinBox.textChanged.connect(self.syncSlider)

        # button box
        self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)

    def syncLineEdit(self, value):
        """Sync the line edit with the slider"""
        self.spinBox.setValue(int(value))
        self.value = value

    def syncSlider(self, value):
        """Sync the slider with the line edit"""
        self.slider.setValue(int(value))
        self.value = int(value)

    def accepted(self):
        self.accept()

    def rejected(self):
        self.reject()
