from abc import abstractmethod
from device import Device

class Monitor(Device):
    @abstractmethod
    def monitorCurrentLevel(self):
        #Checks FileIO for the current level and returns it
        return
    
    @abstractmethod
    def monitorMaxCapacity(self):
        #Checks FileIO for the max capacity and returns it
        return
    