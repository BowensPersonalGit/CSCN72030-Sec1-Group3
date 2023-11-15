from collections import defaultdict
from abstract_classes.controller import Controller
from gui.MainWidget import MainWidget


class grapeController(Controller):       
    def __init__(self):
        self
        
    def changeCurrentLevel(self, newLinePtr):
        return newLinePtr
    
    def UpdateGUI(self, main, currentLevel, bacteriaLevel):
        main.grapeWidget.changeLevels(currentLevel)
        main.grapeWidget.changeBacteria(bacteriaLevel)
        
    def changeBacteriaLevel(self, newLinePtr):
        return newLinePtr

    