from abc import abstractmethod
from abstract_classes.monitor import Monitor

class grapeMonitor(Monitor):
    def __init__(self, Level_File, Bacteria_File):
        self.Level_File = Level_File
        self.Bacteria_File = Bacteria_File
        
    def monitorCurrentLevel(self, linePtr):
        with open (self.Level_File, "r") as file:
            lines = file.readlines()
            numbers_from_file = [int(line.strip()) for line in lines]
            
        return numbers_from_file[linePtr]
    
    def monitorBacteriaLevel(self, linePtr):
        with open (self.Bacteria_File, "r") as file:
            lines = file.readlines()
            numbers_from_file = [int(line.strip()) for line in lines]
            
        return numbers_from_file[linePtr]

    