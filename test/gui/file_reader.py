# read from a file and return a list of values
def readFromFile(fileName):
    """Read ENTIRE file and return a list of values"""
    with open(fileName, "r") as file:
        # Read all lines into a list
        lines = file.readlines()

        # Check if the file is not empty
        if lines:
            return [float(line) for line in lines]
        else:
            return 0
