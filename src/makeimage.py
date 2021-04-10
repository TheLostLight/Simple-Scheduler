from PIL import Image, ImageDraw

HEIGHT_PER_ROOM = 100
NOTCH_PROTRUSION = 2
TIME_STEP = 50
LABEL_FLOAT = 8
DF = '{0:2g}'

def drawClass(draw, room, x_origin, tpp, start, stop):

    center_y = HEIGHT_PER_ROOM*room + HEIGHT_PER_ROOM/2
    top_left = (x_origin + start/tpp, center_y-20)
    bottom_right = (x_origin + stop/tpp, center_y+20)
    center_x = (top_left[0]+bottom_right[0])/2

    draw.rectangle([top_left, bottom_right], fill="red", outline="blue")

    label = str(start) + "-" + str(stop)

    draw.text((center_x-(draw.textlength(label)/2), center_y-25-draw.textsize(label)[1]), label, fill="black")

def createDiagram(classrooms):
    max_time = 0

    #Find maximum class time for scaling purposes
    for c in classrooms:
        max_time = c[-1][1] if c[-1][1] > max_time else max_time

    if max_time/0.01 + TIME_STEP + 10 < 2400:
        time_per_pixel = 0.01
    elif max_time/0.1 + TIME_STEP + 10 < 2400:
        time_per_pixel = 0.1
    elif max_time/0.5 + TIME_STEP + 10 < 2400:
        time_per_pixel = 0.5
    else:
        time_per_pixel = 1
    

    number_of_rooms = len(classrooms)

    result = Image.new('RGBA', (int(max_time/time_per_pixel + TIME_STEP + 10), int(HEIGHT_PER_ROOM*(number_of_rooms+1))), (0, 255, 0, 0))
    draw = ImageDraw.Draw(result)

    y_origin = result.size[1] + NOTCH_PROTRUSION - HEIGHT_PER_ROOM
    x_origin = 10

    #Draw y_axis
    draw.line([(x_origin, 0), (x_origin, y_origin)], fill="black", width=2)
    #Draw x_axis
    draw.line([(x_origin, y_origin), (result.size[0]-1, y_origin)], fill="black", width=2)
    cursor = x_origin
    label = 0
    while cursor < result.size[0]:
        draw.line([(cursor, y_origin-NOTCH_PROTRUSION), (cursor, y_origin+NOTCH_PROTRUSION+1)], fill="grey", width=2)
        draw.text((cursor-(draw.textlength(DF.format(label))/2)+1, y_origin+LABEL_FLOAT+NOTCH_PROTRUSION), DF.format(label), fill="black")
        label += TIME_STEP*time_per_pixel
        cursor += TIME_STEP


    #Draw Class labels + class times
    for i in range(0, number_of_rooms):
        text = "Classroom " + str(i+1)
        cursor = (result.size[0]-x_origin)/2 - draw.textlength(text)/2 + 1
        draw.text((cursor, HEIGHT_PER_ROOM*i + 1), text, fill="black")

        for class_time in classrooms[i]:
            drawClass(draw, i, x_origin, time_per_pixel, class_time[0], class_time[1])

    return result

def getDiagram(data, file_name, save):
    image = createDiagram(data)

    if(save):
        image.save(file_name, "PNG")
    else:
        image.show()