from abc import abstractmethod
from abstract_classes.device import Device
class Monitor(Device):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def monitorCurrentLevel(self):
        pass

