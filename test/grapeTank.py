from abstract_classes.monitor import Monitor
from grapeController import grapeController
from grapeMonitor import grapeMonitor
from abstract_classes.abstractTank import Tank

class grapeTank(Tank):
    def __init__(self, current_level_file, grapeBacteria_File, main):
        self.controller = grapeController()
        self.monitor = grapeMonitor(current_level_file, grapeBacteria_File)
        self.main = main
        self._lvlFileLine = 0
        self._bacteriaFileLine = 0

    def updateGrapeTank(self):
        self.setCurrentLevel(5)
        self.setBacteriaLevel(5)
        self.controller.UpdateGUI(self.main, self.getCurrentLevel(),self.getBacteriaLevel())
        
    def getCurrentLevel(self):
        return self.monitor.monitorCurrentLevel(self._lvlFileLine)

    def getBacteriaLevel(self):
        return self.monitor.monitorBacteriaLevel(self._lvlFileLine)

    def setCurrentLevel(self, newLevel):
        self._lvlFileLine = self.controller.changeCurrentLevel(newLevel)
        
    def setBacteriaLevel(self, newLevel):
        self._bacteriaFileLine = self.controller.changeBacteriaLevel(newLevel)
    