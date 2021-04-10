import scheduler
from filereader import getDataset

classes = getDataset("test.txt")

#classes.sort()
classes.sort(reverse=True)

#classrooms = scheduler.matt_algorithm(classes)
classrooms = scheduler.greedy_algorithm(classes.copy())

for i in range(0, len(classrooms)):
    print("Classroom " + str(i+1) + ":")

    for c in classrooms[i]:
        print("Class " + str(classes.index(c)+1) + ": (" + str(c[0]) + "-" + str(c[1]) + ")")