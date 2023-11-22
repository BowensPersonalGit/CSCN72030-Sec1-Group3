from abstract_classes.controller import Controller

class WaterController(Controller):
    def __init__(self, sourceName):
        super().__init__(sourceName, filePointer = None)
    
    def changeCurrentLevel(self):
        pass

    def changePurity(self):
        pass