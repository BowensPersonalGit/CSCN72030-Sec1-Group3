# water tank class
# an instance of this class will be created in main
# from abstract_classes.abstractTank import abstractTank as Tank

from WaterMonitor import WaterMonitor


class WaterTank:
    def __init__(self, sourceNames: list):
        self.waterMonitor = WaterMonitor(sourceNames)
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


if __name__ == "__main__":
    w = WaterTank(["./test/water_levels.txt", "./test/water_puritys.txt"])
    print(w.getCurrentLevel())
    print(w.getPurity())
