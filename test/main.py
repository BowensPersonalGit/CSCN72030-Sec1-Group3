# main stuff
# only run this plz
import sys

from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer

from gui.MainWidget import MainWidget
from gui.TitleWidget import TitleWidget
from gui.FooterWidget import FooterWidget
from CiderTank import *

app = QApplication(sys.argv)

# window
window = QFrame()
window.setWindowFlags(Qt.FramelessWindowHint)
window.setFrameStyle(QFrame.Panel | QFrame.Raised)
window.move(0, 0)
window.show()

# layout
layout = QVBoxLayout()
window.setLayout(layout)
layout.setContentsMargins(0, 0, 0, 0)
layout.setSpacing(0)

# title bar
title = TitleWidget()


# main widget
main = MainWidget()

# footer widget
footer = FooterWidget()

# add widgets to layout
layout.addWidget(title)
layout.addWidget(main)
layout.addWidget(footer)

# show
title.show()
main.show()

sys.exit(app.exec())
