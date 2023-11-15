from abc import abstractmethod
from abstract_classes.device import Device

class Controller(Device):
    @abstractmethod
    def changeCurrentLevel(self):
        #moves the filePointer for currentLevel in the fileIO
        return
    