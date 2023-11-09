from abc import abstractmethod
from device import Device

class Controller(Device):
    @abstractmethod
    def changeCurrentLevel(self):
        #moves the filePointer for currentLevel in the fileIO
        return
    
    @abstractmethod
    def changeMaxCapacity(self):
        #moves the filePointer for maxCapacity in the fileIO
        return
    