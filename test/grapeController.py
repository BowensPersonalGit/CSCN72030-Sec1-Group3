#from abstract_classes.controller import Controller


class GrapeController():       
    def __init__(self, Level_File, Bacteria_File):
        self.Level_File = Level_File
        self.Bacteria_File = Bacteria_File
        
    def changeCurrentLevel(self, x):
        with open (self.Level_File, "a") as file:
            file.write(str(x) + "\n")
    
        
    def changeBacteriaLevel(self, x):
        with open (self.Bacteria_File, "a") as file:
            file.write(str(x) + "\n")

    