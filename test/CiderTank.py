# from abstractTank import *
# from controller import *
# from monitor import *

# CiderTank:
# - alcohol - setter + getter - setAlcohol(value), getAlcohol()
# - pressure - setter + getter - setPressure(value), getPressure()
# - current_level - setter + getter - setCurrentLevel(value), getCurrentLevel()


## Backend File Reading for Cider Tank
class CiderMonitor:
    def __init__(self, fileName):
        self.fileName = fileName

    def getValue(self):
        with open(self.fileName, "r") as file:
            # Read all lines into a list
            lines = file.readlines()

            # Check if the file is not empty
            if lines:
                # Return the last line
                return int(lines[-1])
            else:
                # If the file is empty it means we havnt brewed any Cider yet so we return 0
                return 0


## Backend File Writing for Cider Tank
class CiderController:
    def __init__(self, fileName):
        self.fileName = fileName

    def setValue(self, value):
        # Open the file in append mode to add content without overwriting existing content
        with open(self.fileName, "a") as file:
            # Write the value to the last line
            file.write(str(value) + "\n")


## Object the GUI interacts with:
class CiderTank:
    def __init__(self):
        self.alcMonitor = CiderMonitor("./test/cideralcohol.txt")
        self.alcController = CiderController("./test/cideralcohol.txt")
        self.pressureMonitor = CiderMonitor("./test/ciderpressure.txt")
        self.pressureController = CiderController("./test/ciderpressure.txt")
        self.levelMonitor = CiderMonitor("./test/ciderlevel.txt")
        self.levelController = CiderController("./test/ciderlevel.txt")

    def getAlcohol(self):
        return self.alcMonitor.getValue()

    def setAlcohol(self, value):
        self.alcController.setValue(value)

    def getPressure(self):
        return self.pressureMonitor.getValue()

    def setPressure(self, value):
        self.pressureController.setValue(value)

    def getCurrentLevel(self):
        return self.levelMonitor.getValue()

    def setCurrentLevel(self, value):
        self.levelController.setValue(value)


### Testing
if __name__ == "__main__":
    ciderTank = CiderTank()
    ciderTank.setAlcohol(10)
    ciderTank.setPressure(11)
    ciderTank.setCurrentLevel(12)

    print(ciderTank.getAlcohol())
    print(ciderTank.getPressure())
    print(ciderTank.getCurrentLevel())

### Testing
