# Takes a list of classes (tuple of two ints) 
# sorted by starting time (ascending).
# Then fills up classrooms one by one,
# iterating over the list and removing 
# classes each time they are assigned a classroom
def matt_algorithm(class_list):
    classrooms = list()
    minimum_classrooms = 0

    while(class_list):

        # Unecessary variable, but makes code easier to read
        # (Probably removed by optimizer)
        minimum_classrooms += 1

        # Keeps track of index in list of classrooms
        m = minimum_classrooms-1

        # Create a new classroom, append first element in the list to it as a list.
        classrooms.append([class_list[0]])

        # Temporary list to keep track of unassigned classes.
        temp_list = list()

        # Go through all unassigned classes. If they fit into
        # current classroom, add them. Otherwise, add to temp list
        for i in range(1, len(class_list)):
            
            # Change to '>=' if class start times and end times should overlap
            if class_list[i][0] > classrooms[m][-1][1]:
                classrooms[m].append(class_list[i])
            else:
                temp_list.append(class_list[i])

        class_list = temp_list.copy()

    # Schedule has been made with minimum number of classrooms.
    return classrooms

#Takes a list of classes (tuple of two ints) and
# treats it as a stack. Sorted by start times
# (descending as a list, earliest time first out).
# Sorts each class into the first available classroom one by one.
# Returns a list of classrooms with their scheduled classes
def greedy_algorithm(class_stack):
    classrooms = list()

    # Pop elements from stack one by one and find a classroom
    # in which it has no time conflicts
    while(class_stack):
        current_class = class_stack.pop()

        # Index to track the next unchecked classroom
        index = 0

        # First check if the classroom exists. If not, make it.
        # If it does check if there is no time conflict.
        # If not, add current_class to the classroom.
        # Otherwise, increment the index.
        while(True):
            if index >= len(classrooms):
                classrooms.append([current_class])
                break
            else:
                # Change to '>=' if class start times and end times should overlap 
                if current_class[0] > classrooms[index][-1][1]:
                    classrooms[index].append(current_class)
                    break
                else:
                    index += 1
        #End of inner loop
    #End of outer loop

    #Schedule has been created. 
    return classrooms

