# from abstract_classes.monitor import Monitor


class AppleMonitor:
    def __init__(self, sourceNames: list):
        self.sourceNames = sourceNames

    def monitorCurrentLevel(self):
        """reads the apple_levels.txt (index0) file and returns the value at last line"""
        with open(self.sourceNames[0], "r") as f:
            f_contents = f.readlines()
        return float(f_contents[-1])

    def monitorConcentration(self):
        """reads the apple_concentration.txt (index1) file and returns the value at last line"""
        with open(self.sourceNames[1], "r") as f:
            f_contents = f.readlines()
        return float(f_contents[-1])


if __name__ == "__main__":
    fileNames = ["./test/apple_levels.txt", "./test/apple_concentration.txt"]
    w = AppleMonitor(fileNames)
    print(f"currentlevel:{w.monitorCurrentLevel()}")
    print(f"concentration:{w.monitorConcentration()}")
