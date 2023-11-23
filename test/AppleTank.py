# apple tank class
# an instance of this class will be created in main
# from abstract_classes.abstractTank import abstractTank as Tank

from AppleMonitor import AppleMonitor
from AppleController import AppleController


class AppleTank:
    def __init__(self, sourceNames: list):
        self.appleMonitor = AppleMonitor(sourceNames)
        self.appleController = AppleController(sourceNames)
        self.concentration = 0
        self.current_level = 0
        self.update()

    # Getters and Setters
    def getCurrentLevel(self):
        self.current_level = self.appleMonitor.monitorCurrentLevel()
        return self.current_level

    def setCurrentLevel(self, value):
        self.appleController.controlCurrentLevel(value)
        self.current_level = value

    def getConcentration(self):
        return self.concentration

    def setConcentration(self, value):
        self.concentration = value
    
    def update(self):
        """Update values from the apple monitor"""
        self.current_level = self.appleMonitor.monitorCurrentLevel()
        self.concentration = self.appleMonitor.monitorConcentration()


if __name__ == "__main__":
    w = AppleTank(["./test/apple_levels.txt", "./test/apple_concentration.txt"])
    print(w.getCurrentLevel())
    print(w.getConcentration())

    w.appleController.controlCurrentLevel(80)
    w.appleController.controlConcentration(50)
    w.update()
    print(w.getCurrentLevel())
    print(w.getConcentration())
