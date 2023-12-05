from abc import ABC, abstractmethod
class Device(ABC):
    def __init__(self):
        self.sourceName = None