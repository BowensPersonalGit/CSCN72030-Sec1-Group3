#from abstract_classes.controller import Controller

class WaterController():
    def __init__(self, sourceNames: list):
        print("WaterController __init__")
        self.sourceNames = sourceNames
        
    def controlCurrentLevel(self, value):
        print(f"WaterController.changeCurrentLevel({value})")
        with open(self.sourceNames[0], "a") as f:
            f.write(str(value) + "\n")


    def controlPurity(self, value):
        print(f"WaterController.changePurity({value})")
        with open(self.sourceNames[1], "a") as f:
            f.write(str(value) + "\n")