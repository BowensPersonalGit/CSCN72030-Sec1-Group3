from abc import abstractmethod
from abstract_classes.device import Device


class Controller(Device):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def controlCurrentLevel(self):
        pass
    