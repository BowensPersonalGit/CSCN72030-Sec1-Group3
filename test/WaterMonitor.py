# from abstract_classes.monitor import Monitor


class WaterMonitor:
    def __init__(self, sourceNames: list):
        print("WaterMonitor __init__")
        self.sourceNames = sourceNames

    def monitorCurrentLevel(self):
        """reads the water_levels.txt (index0) file and returns the value at last line"""
        print("WaterMonitor.mointorCurrentLevel()")
        with open(self.sourceNames[0], "r") as f:
            f_contents = f.readlines()
        return int(f_contents[-1])

    def monitorPurity(self):
        """reads the water_puritys.txt (index1) file and returns the value at last line"""
        print("WaterMonitor.monitorPurity()")
        with open(self.sourceNames[1], "r") as f:
            f_contents = f.readlines()
        return int(f_contents[-1])


if __name__ == "__main__":
    fileNames = ["./test/water_levels.txt", "./test/water_puritys.txt"]
    w = WaterMonitor(fileNames)
    print(f"currentlevel:{w.monitorCurrentLevel()}")
    print(f"purity:{w.monitorPurity()}")
