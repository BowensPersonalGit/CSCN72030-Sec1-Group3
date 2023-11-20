# water tank class
# an instance of this class will be created in main 
from abstract_classes.abstractTank import abstractTank as Tank


class WaterTank(Tank):
    def __init__(self, file_name: list):
        super().__int__()
        self._purity = 0
        self._waterMonitor = WaterMonitor(file_name[0])
        self._waterController = WaterController(file_name[1])
    
    # Getters and Setters
    def getCurrentLevel(self):
        return self.current_level

    def setCurrentLevel(self, value):
        self.current_level = value

    def getPurity(self):
        return self._purity

    def setPurity(self, value):
        self._purity = value

    
if __name__ == "__main__":
    pass
