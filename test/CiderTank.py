from abstractTank import *
from controller import *
from monitor import *
from grapeTank import *
from appleTank import *

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
    def __init__(self):
        self.waterLevel = waterTank.getCurrentWaterLevel()
        self.appleLevel = appleTank.getCurrentAppleLevel()
    
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

    def brewCider(self):
        appleTank.takeProduct(50)
        waterTank.takeProduct(50)
        self.ciderMonitor.setNewCurrentLevel(100)
        return self.ciderMonitor.monitorCurrentLevel()



