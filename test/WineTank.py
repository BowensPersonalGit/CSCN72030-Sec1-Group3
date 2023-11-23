# from abstractTank import *
# from controller import *
# from monitor import *

# WineTank:
# - alcohol - setter + getter - setAlcohol(value), getAlcohol()
# - pressure - setter + getter - setPressure(value), getPressure()
# - current_level - setter + getter - setCurrentLevel(value), getCurrentLevel()


## Backend File Reading for Wine Tank
class WineMonitor:
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
                # If the file is empty it means we havnt brewed any Wine yet so we return 0
                return 0


## Backend File Writing for Wine Tank
class WineController:
    def __init__(self, fileName):
        self.fileName = fileName

    def setValue(self, value):
        # Open the file in append mode to add content without overwriting existing content
        with open(self.fileName, "a") as file:
            # Write the value to the last line
            file.write(str(value) + "\n")


## Object the GUI interacts with:
class WineTank:
    def __init__(self):
        self.alcMonitor = WineMonitor("./test/winealcohol.txt")
        self.alcController = WineController("./test/winealcohol.txt")
        self.pressureMonitor = WineMonitor("./test/winepressure.txt")
        self.pressureController = WineController("./test/winepressure.txt")
        self.levelMonitor = WineMonitor("./test/winelevel.txt")
        self.levelController = WineController("./test/winelevel.txt")

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
    wineTank = WineTank()
    wineTank.setAlcohol(6)
    wineTank.setPressure(11)
    wineTank.setCurrentLevel(1)
    wineTank.setCurrentLevel(1)

    print(wineTank.getAlcohol())
    print(wineTank.getPressure())
    print(wineTank.getCurrentLevel())

### Testing
