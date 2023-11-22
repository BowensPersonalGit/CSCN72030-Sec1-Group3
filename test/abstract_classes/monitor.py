from abc import abstractmethod
from abstract_classes.device import Device


class Monitor(Device):
    @abstractmethod
    def monitorCurrentLevel(self):
        #Checks FileIO for the current level and returns it
        return

