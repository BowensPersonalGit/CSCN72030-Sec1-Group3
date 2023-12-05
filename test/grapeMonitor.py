from abstract_classes.monitor import Monitor
class GrapeMonitor(Monitor):
    def __init__(self, Level_File, Bacteria_File):
        super().__init__()
        self.Level_File = Level_File
        self.Bacteria_File = Bacteria_File
        
    def monitorCurrentLevel(self):
        with open (self.Level_File, "r") as file:
            lines = file.readlines()     
        return float(lines[-1])
    
    def monitorBacteriaLevel(self):
        with open (self.Bacteria_File, "r") as file:
            lines = file.readlines()
        return float(lines[-1])

    