#from abstract_classes.controller import Controller

class AppleController():
    def __init__(self, sourceNames: list):
        self.sourceNames = sourceNames
        
    def controlCurrentLevel(self, value):
        print(f"AppleController.changeCurrentLevel({value})")
        with open(self.sourceNames[0], "a") as f:
            f.write(str(value) + "\n")


    def controlConcentration(self, value):
        print(f"AppleController.changeConcentration({value})")
        with open(self.sourceNames[1], "a") as f:
            f.write(str(value) + "\n")