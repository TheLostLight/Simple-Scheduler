import tkinter
from tkinter import filedialog
from tkinter import messagebox
import os

from filegenerator import createExampleFile
from filegenerator import saveDataToFile
from filereader import getDataset
import scheduler
from makeimage import getDiagram

def showFileDialog(top):
    top.withdraw()
    of = filedialog.askopenfilename(parent=top, initialdir=os.getcwd())
    top.deiconify()
    return of

def showFileSave(top):
    top.withdraw()
    sf = filedialog.asksaveasfilename(parent=top, initialdir=os.getcwd())
    top.deiconify()
    return sf

def isNotDigit(text):
    return text.isdigit()

def showTargetPanel(current_frame, target_frame):
    current_frame.pack_forget()
    target_frame.pack()

def saveExampleFile(top, nclass, max_n):
    
    if nclass == "" or max_n == "":
        messagebox.showerror(title="User error", message="Please enter a number in the above fields")
        return
    
    top.withdraw()
    save_filename = filedialog.asksaveasfilename(parent=top, title="Save example to txt", initialdir=os.getcwd(), defaultextension=".txt")
    top.deiconify()

    if save_filename == '':
        return

    try:
        createExampleFile(save_filename, int(nclass), int(max_n))
    except TypeError:
        tkinter.messagebox.showerror(title="How did that happen?", message="Type error. Was a non-integer entered in input fields?")
    except IOError:
        tkinter.messagebox.showerror(title="IOError", message="There was an error creating the file.")

def saveToText(top, data):
    try:
        top.withdraw()
        file_name = filedialog.asksaveasfilename(parent=top, title="Save to text", initialdir=os.getcwd(), defaultextension=".txt")
        top.deiconify()
    except IOError:
        messagebox.showerror(title="IOError", message="There was an error opening selected file.")
        return False

    if file_name == "":
        return False

    try:
        saveDataToFile(file_name, data)
    except IOError:
        messagebox.showerror(title="IOError", message="There was an error saving results to file...")
        return False
    except TypeError:
        messagebox.showerror(title="TypeError", message="There was an error saving results to file...")
        return False

    return True

def saveToPNG(top, data):
    try:
        top.withdraw()
        file_name = filedialog.asksaveasfilename(parent=top, title="Save to png", initialdir=os.getcwd(), defaultextension=".png")
        top.deiconify()
    except IOError:
        messagebox.showerror(title="IOError", message="There was an error opening selected file.")
        return False

    if file_name == "":
        return False

    try:
        getDiagram(data, file_name, True)
    except IOError:
        messagebox.showerror(title="IOError", message="There was an error saving results to file...")
        return False

    return True

def saveToBoth(top, data):
    if not saveToText(top, data):
        return
    saveToPNG(top, data)

def createOutput(top, main_frame, use_matt_algo):
    try:
        file_name = showFileDialog(top)

        if file_name == "":
            return

        data = getDataset(file_name)

        if(use_matt_algo):
            data.sort()
            classrooms = scheduler.matt_algorithm(data)
        else:
            data.sort(reverse=True)
            classrooms = scheduler.greedy_algorithm(data.copy())
    
    except IOError:
        messagebox.showerror(title="IOError", message="An error with the input file.")
        return

    # Output frame
    #------------------------------------------------------------------------
    output_frame = tkinter.Frame(top)

    outputf_label = tkinter.Label(output_frame, text="Results ready!")
    outputf_label.pack()

    mimage_button = tkinter.Button(output_frame, text="Show diagram", command=lambda: getDiagram(classrooms, "", False))
    mimage_button.pack()

    simage_button = tkinter.Button(output_frame, text="Save diagram to png file", command=lambda: saveToPNG(top, classrooms))
    simage_button.pack()

    stext_button = tkinter.Button(output_frame, text="Save raw data to txt file", command=lambda: saveToText(top, classrooms))
    stext_button.pack()

    both_button = tkinter.Button(output_frame, text="Save raw data and diagram", command=lambda: saveToBoth(top, classrooms))
    both_button.pack()

    output_return_button = tkinter.Button(output_frame, text="Return", command=lambda: showTargetPanel(output_frame, main_frame))
    output_return_button.pack()

    showTargetPanel(main_frame, output_frame)
    


def createGUI():
    top = tkinter.Tk()
    top.title("CPSC-482 Scheduling")


    # Main frame
    #------------------------------------------------
    main_frame = tkinter.Frame(top)

    generator_button = tkinter.Button(main_frame, text="Create new example file", command=lambda: showTargetPanel(main_frame, example_frame))
    generator_button.pack()

    matt_button = tkinter.Button(main_frame, text="Use Matt's Algorithm", command=lambda: createOutput(top, main_frame, True))
    matt_button.pack()

    greedy_button = tkinter.Button(main_frame, text="Use Greedy Algorithm", command=lambda: createOutput(top, main_frame, False))
    greedy_button.pack()

    exit_button = tkinter.Button(main_frame, text="Quit", command=top.quit)
    exit_button.pack()

    main_frame.pack()
    #--------------------------------------------------

    # Example frame
    #--------------------------------------------------
    example_frame = tkinter.Frame(top)
    vcmd = example_frame.register(isNotDigit)

    nclass_label = tkinter.Label(example_frame, text='Enter # of classes:')
    nclass_label.pack()

    class_num = tkinter.Entry(example_frame, validate='key', validatecommand=(vcmd, '%S'))
    #class_num.insert(0, "1")
    class_num.pack()

    maxn_label = tkinter.Label(example_frame, text="Enter maximum timeslot:")
    maxn_label.pack()

    max_time = tkinter.Entry(example_frame, validate='key', validatecommand=(vcmd, '%S'))
    #max_time.insert(0, '2')
    max_time.pack()

    ex_save_button = tkinter.Button(example_frame, text='Save to file', command=lambda: saveExampleFile(top, class_num.get(), max_time.get()))
    ex_save_button.pack()

    ex_return_button = tkinter.Button(example_frame, text='Return', command=lambda: showTargetPanel(example_frame, main_frame))
    ex_return_button.pack()
    #------------------------------------------------------------------------

    
    top.mainloop()