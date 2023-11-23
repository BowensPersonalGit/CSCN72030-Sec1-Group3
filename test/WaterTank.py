# water tank class
# an instance of this class will be created in main
# from abstract_classes.abstractTank import abstractTank as Tank

from WaterMonitor import WaterMonitor
from WaterController import WaterController


class WaterTank:
    def __init__(self, sourceNames: list):
        self.waterMonitor = WaterMonitor(sourceNames)
        self.waterController = WaterController(sourceNames)
        self.purity = self.waterMonitor.monitorCurrentLevel()
        self.current_level = self.waterMonitor.monitorPurity()

    # Getters and Setters
    def getCurrentLevel(self):
        return self.current_level

    def setCurrentLevel(self, value):
        self.current_level = value

    def getPurity(self):
        return self.purity

    def setPurity(self, value):
        self.purity = value
    
    def update(self):
        self.current_level = self.waterMonitor.monitorCurrentLevel()
        self.purity = self.waterMonitor.monitorPurity()


if __name__ == "__main__":
    w = WaterTank(["./test/water_levels.txt", "./test/water_puritys.txt"])
    print(w.getCurrentLevel())
    print(w.getPurity())

    w.waterController.changeCurrentLevel(85)
    w.waterController.changePurity(85)
    w.update()
    print(w.getCurrentLevel())
    print(w.getPurity())
