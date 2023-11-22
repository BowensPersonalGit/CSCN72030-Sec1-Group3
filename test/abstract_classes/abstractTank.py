from abc import ABC, abstractmethod

class Tank(ABC):
    def __init__(self, max_capacity, current_level, max_pressure, controller, monitor, pressure_file):
        self.max_capacity = max_capacity
        self.current_level = current_level
        self.controller = controller
        self.monitor = monitor
        self.max_pressure = max_pressure
        self.pressure_file = pressure_file

    @abstractmethod
    def getCurrentLevel(self):
        #Use Monitor to get current_level
        return
    
    
    def setCurrentLevel(self):
        #Use Controller to change the current_level
        return
    
    
