from abstractTank import *
from controller import *
from monitor import *

class CiderMonitor(Monitor):
    def __init__(self, curCap, curPressure):
        self.curCap = curCap
        self.curPressure = curPressure

    def setNewCurrentLevel(self, newLevel):
        self.curCap = newLevel

    def monitorPressure(self):
        return self.curPressure
    
    def monitorCurrentLevel(self):
        return self.curCap

class CiderController(Controller):
    def __init__(self, cap, pressure):
        self.cap = cap
        self.pressure = pressure
        return
    
    def addWater(self):
        #interact with water module to change file pointer.
        return

    def addApples(self):
        #interact with apple module to change file pointer
        return

class CiderTank(Tank):
    def __init__(self, maxCapacity, maxPressure):
        self.ciderController = CiderController(maxCapacity, maxPressure)
        self.ciderMonitor = CiderMonitor

    def getCurrentLevel(self):
        return
    
    def getMaxCapacity(self):
        return
    
    def setCurrentLevel(self):
        return
    
    def setMaxCapacity(self):
        return
    
    def brewCider(self, applesTaken, waterTaken):
        self.applesTaken = applesTaken
        self.watertaken = waterTaken
        self.ciderMonitor.setNewCurrentLevel(applesTaken + waterTaken)
        return self.ciderMonitor.monitorCurrentLevel()



