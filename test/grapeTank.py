# from abstract_classes.abstractTank import Tank
from grapeController import GrapeController
from grapeMonitor import GrapeMonitor


class GrapeTank:
    def __init__(self, Level_File, Bacteria_File):
        self.controller = GrapeController(Level_File, Bacteria_File)
        self.monitor = GrapeMonitor(Level_File, Bacteria_File)
        self._currentLevel = 0
        self._bacteria = 0
        self.update()

    def getCurrentLevel(self):
        self._current_level = self.monitor.monitorCurrentLevel()
        return self._current_level

    def getBacteriaLevel(self):
        self._bacteria = self.monitor.monitorBacteriaLevel()
        return self._bacteria

    def getLinePtrValue(self):
        return self._lvlFileLine

    def getBacteriaLinePtrValue(self):
        return self._bacteriaFileLine

    def setCurrentLevel(self, newLevel):
        self.controller.changeCurrentLevel(newLevel)
        self._currentLevel = newLevel

    def setBacteriaLevel(self, newLevel):
        self.controller.changeBacteriaLevel(newLevel)
        self._bacteria = newLevel
    
    def update(self):
        self._currentLevel = self.monitor.monitorCurrentLevel()
        self._bacteria = self.monitor.monitorBacteriaLevel()
