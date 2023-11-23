# main stuff
# only run this plz
import sys

from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from grapeController import grapeController

from gui.MainWidget import MainWidget
from gui.TitleWidget import TitleWidget
from gui.FooterWidget import FooterWidget

from grapeTank import grapeTank

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
grapeControllerWidget = main.grapeWidget.grapeControllerWidget

########################## DEMO TEST CODE ##########################
counter = 0

def update():
    
    grapeControllerWidget.incrementCurrentLevel()
    grapeControllerWidget.incrementBacteriaLevel()
    updateAllTankValues(grapeControllerWidget.returnCurrentLevel(), grapeControllerWidget.returnBacteriaLevel(), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    

def updateAllTankValues(grapeLevel, bacteriaLevel, appleLevel, appleConcentration, waterLevel, waterPurity, ciderLevel, ciderPressure,ciderAlcohol, wineLevel, winePressure, wineAlcohol):
    main.grapeWidget.changeLevels(grapeLevel)
    main.grapeWidget.changeBacteria(bacteriaLevel)       
    main.appleWidget.changeLevels(appleLevel)
    main.appleWidget.changeConcentration(appleConcentration)
    main.waterWidget.changeLevels(waterLevel)
    main.waterWidget.changePurity(waterPurity)    
    main.ciderWidget.changeLevels(ciderLevel)
    main.ciderWidget.changePressure(ciderPressure)
    main.ciderWidget.changeAlcohol(ciderAlcohol)
    main.wineWidget.changeLevels(wineLevel)
    main.wineWidget.changePressure(winePressure)
    main.wineWidget.changeAlcohol(wineAlcohol)
        
# def increment_level():
#     global counter
    
#     main.waterWidget.changeLevels(counter)
#     main.appleWidget.changeLevels(counter)
#     main.ciderWidget.changeLevels(counter)
#     main.grapeWidget.changeLevels(counter)
#     main.wineWidget.changeLevels(counter)

#     main.waterWidget.changePurity(counter)
#     main.appleWidget.changeConcentration(counter)
#     main.ciderWidget.changePressure(counter)
#     main.ciderWidget.changeAlcohol(counter)
#     main.grapeWidget.changeBacteria(counter)
#     main.wineWidget.changePressure(counter)
#     main.wineWidget.changeAlcohol(counter)

#     counter += 5

# timer to space out the level changes
# MUST USE QTIMER, NO time.sleep()
timer = QTimer()

timer.timeout.connect(update)  # set what happend when timer times out
timer.start(500)  # start timer by milliseconds

###############################################################


sys.exit(app.exec())


