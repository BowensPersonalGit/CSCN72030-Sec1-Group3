# read from a file and return a list of values
def readFromFile(fileName):
    with open(fileName, "r") as file:
        # Read all lines into a list
        lines = file.readlines()

        # Check if the file is not empty
        if lines:
            # Return the last line
            return [int(line) for line in lines]
        else:
            # If the file is empty it means we havnt brewed any Cider yet so we return 0
            return 0
