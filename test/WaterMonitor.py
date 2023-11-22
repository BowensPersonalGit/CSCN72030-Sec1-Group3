from abstract_classes.monitor import Monitor

class WaterMonitor(Monitor):
    def __init__(self, sourceName):
        super().__init__(sourceName, filePointer = None)
    
    def monitorCurrentLevel(self):
        pass

    def monitorPurity(self):
        pass


