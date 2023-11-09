from abc import ABC, abstractmethod

class Tank(ABC):
    def __init__(self, max_capacity, current_capacity, max_pressure, current_pressure, file_name):
        self.max_capacity = max_capacity
        self.current_capacity = current_capacity
        self.file_name = file_name

    @abstractmethod
    def getCurrentCapacity(self):
        #Access fileIO class to interact with the file.
        return
    
    @abstractmethod
    def getMaxCapacity(self):
        #Access fileIO class to interact with the file.
        return
    
    def setCurrentCapacity(self):
        #Access fileIO class to interact with the file.
        return
    
    def setMaxCapacity(self):
        #Access fileIO class to interact with the file.
        return
    
    
