# water tank class

import abstractTank


class WaterTank(abstractTank):
    def __init__(self, file_name: list):
        super().__int__()
        self.purity = 0
        self.waterMonitor = None #WaterMonitor(file_name[0])
        self.waterController = None #WaterController(file_name[1])
    
    # Getters and Setters
    def getCurrentLevel(self):
        pass

    def setCurrentLevel(self):
        pass

    def getPurity(self):
        pass

    def setPurity(self):
        pass

    
if __name__ == "__main__":
    pass
