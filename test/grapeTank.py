from abstract_classes.monitor import Monitor
from grapeController import grapeController
from grapeMonitor import grapeMonitor
from abstract_classes.abstractTank import Tank

class grapeTank(Tank):
    def __init__(self, current_level_file, grapeBacteria_File, grapeWidget):
        self.controller = grapeController()
        self.monitor = grapeMonitor(current_level_file, grapeBacteria_File)
        self.grapeWidget = grapeWidget
        self._lvlFileLine = 0
        self._bacteriaFileLine = 0
        
    def getCurrentLevel(self):
        return self.monitor.monitorCurrentLevel(self._lvlFileLine)

    def getBacteriaLevel(self):
        return self.monitor.monitorBacteriaLevel(self._bacteriaFileLine)
    
    def getLinePtrValue(self):
        return self._lvlFileLine

    def getBacteriaLinePtrValue(self):
        return self._bacteriaFileLine

    def setCurrentLevel(self, newLevel):
        self._lvlFileLine = self.controller.changeCurrentLevel(newLevel)
        
    def setBacteriaLevel(self, newLevel):
        self._bacteriaFileLine = self.controller.changeBacteriaLevel(newLevel)
    