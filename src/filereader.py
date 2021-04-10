import re

# Take an input file and return a list of tuples of two ints
# (starting time and ending time).
def getDataset(file_name):
    with open(file_name, "r") as file:
        
        input_text = file.read()
        values = [int(num) for num in re.findall("[0-9]+", input_text)]

    if(len(values) < 2):
        raise Exception("Less than two numbers found in file.\n Incorrect formatting.")
    
    data_set = list()

    for i in range(0, len(values), 2):
        data_set.append((values[i], values[i+1]))

    return data_set