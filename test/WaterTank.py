# water tank class
# an instance of this class will be created in main
from abstract_classes.tank import Tank

from WaterMonitor import WaterMonitor
from WaterController import WaterController


class WaterTank(Tank):
    def __init__(self, sourceNames: list):
        super().__init__()
        self.waterMonitor = WaterMonitor(sourceNames)
        self.waterController = WaterController(sourceNames)
        self.purity = 0
        self.current_level = 0
        self.update()

    # Getters and Setters
    def getCurrentLevel(self):
        self.current_level = self.waterMonitor.monitorCurrentLevel()
        return self.current_level

    def setCurrentLevel(self, value):
        self.waterController.controlCurrentLevel(value)
        self.current_level = value

    def getPurity(self):
        self.purity = self.waterMonitor.monitorPurity()
        return self.purity

    def setPurity(self, value):
        self.waterController.controlPurity(value)
        self.purity = value
    
    def update(self):
        """Update values from the water monitor"""
        self.current_level = self.waterMonitor.monitorCurrentLevel()
        self.purity = self.waterMonitor.monitorPurity()


if __name__ == "__main__":
    w = WaterTank(["./test/water_levels.txt", "./test/water_puritys.txt"])
    print(w.getCurrentLevel())
    print(w.getPurity())

    w.waterController.controlCurrentLevel(85)
    w.waterController.controlPurity(85)
    w.update()
    print(w.getCurrentLevel())
    print(w.getPurity())
