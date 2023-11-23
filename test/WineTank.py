from abstractTank import *
from controller import *
from monitor import *

#WineTank:
#- alcohol - setter + getter - setAlcohol(value), getAlcohol()
#- pressure - setter + getter - setPressure(value), getPressure()
#- current_level - setter + getter - setCurrentLevel(value), getCurrentLevel()


## Backend File Reading for Wine Tank
class WineMonitor():
    def __init__(self, fileName):
        self.fileName = fileName

    def getValue(self):
        with open(self.fileName, 'r') as file:

            # Read all lines into a list
            lines = file.readlines()

            # Check if the file is not empty
            if lines:
                # Return the last line
                return lines[-1]
            else:
                # If the file is empty it means we havnt brewed any Wine yet so we return 0
                return "0"
    
## Backend File Writing for Wine Tank
class WineController():
    def __init__(self, fileName):
        self.fileName = fileName
    
    def setValue(self, value):
        # Open the file in append mode to add content without overwriting existing content
        with open(self.fileName, 'a') as file:
            # Write the value to the last line
            file.write(value + '\n')

## Object the GUI interacts with:
class WineTank():
    def __init__(self):
        self.alcMonitor = WineMonitor("winealcohol.txt")
        self.alcController = WineController("winealcohol.txt")
        self.pressureMonitor = WineMonitor("winepressure.txt")
        self.pressureController = WineController("winepressure.txt")
        self.volumeMonitor = WineMonitor("winevolume.txt")
        self.volumeController = WineController("winevolume.txt")
        
    def getAlcVolume(self):
        return self.alcMonitor.getValue()

    def setAlcVolume(self, value):
        self.alcController.setValue(value)

    def getPressure(self):
        return self.pressureMonitor.getValue()
    
    def setPressure(self, value):
        self.pressureController.setValue(value)

    def getVolume(self):
        return self.volumeMonitor.getValue()
    
    def setVolume(self, value):
        self.volumeController.setValue(value)



### Testing
if __name__ == "__main__":
    
    wineTank = WineTank()
    wineTank.setAlcVolume("5.99%")
    wineTank.setPressure("11 PSI")
    wineTank.setVolume("1 MILLION Litres")
    wineTank.setVolume("500 MILLION Litres")

    print(wineTank.getAlcVolume())
    print(wineTank.getPressure())
    print(wineTank.getVolume())

### Testing