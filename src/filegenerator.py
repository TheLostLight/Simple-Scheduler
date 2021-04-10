import random
from datetime import datetime

# Randomly generates an example file which can be used as
# input in fileread.py
# 
# file_name - Name of resulting output file
# nclass    - Number of individual class times to generate
# max_time  - The maximum latest time a class can end at
def createExampleFile(file_name, nclass, max_time):
    result = open(file_name, "w")

    result.write("Classes (start_time::end_time) : \n")

    for _ in range(0, nclass):
        start = random.randint(0, max_time-1)
        result.write("(" + str(start) + "::" + str(random.randint(start+1, max_time)) + ")\n")

    result.close()

# Saves the result of a scheduling algorithm to a text file
def saveDataToFile(file_name, data):
    result = open(file_name, "w")

    result.write("File generated " + datetime.now().strftime("%B %d, %Y - %H:%M:%S") + "\n\n")
    result.write("Minimum classrooms: " + str(len(data)) + "\n")
    result.write("---------\n\n")

    for i in range(0, len(data)):
        result.write("Classroom " + str(i+1) + ":\n----------------\n")
        ind = 1

        for class_time in data[i]:
            result.write("Class " + str(ind) + ": (" + str(class_time[0]) + "-" + str(class_time[1]) + ")\n")
            ind += 1
        
        #result.write("----------------\n")
        result.write("\n")

    result.close()