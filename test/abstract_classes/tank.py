from abc import ABC, abstractmethod

class Tank(ABC):
    def __init__(self):
        self.current_level = None

    @abstractmethod
    def getCurrentLevel(self):
        #Use Monitor to get current_level
        return
    
    @abstractmethod
    def setCurrentLevel(self):
        #Use Controller to change the current_level
        return
    
    
