# Python program to create
# a file explorer in Tkinter
  
# import all components
# from the tkinter library
from tkinter import *
  
# import filedialog module
from tkinter import filedialog

filename = ''
  
# Function for opening the
# file explorer window
def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir = "",
                                          title = "Select a File",
                                          filetypes = (("EXE files",
                                                        "*.exe*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)
      
def caves():
                global filename
                Nop_Address = []
                Nop_caves = []
                Nop_ranges = []
                Address = 0
                range_size = 0
                file = open(filename, "rb")
                byte = file.read(1)
                while byte:
                    if byte == b'\x90':
                        if len(Nop_Address) != 0:
                            if Address == Nop_Address[len(Nop_Address)-1]+1 :
                                Nop_Address.append(Address)
                                Nop_caves.append(Address)
                                Nop_caves.append(Address-1)
                            else:
                                Nop_Address.append(Address)
                        else:
                            Nop_Address.append(Address)
                        
                    byte = file. read(1)
                    Address = Address + 1
                Nop_caves.sort()
                Nop_caves = list(dict.fromkeys(Nop_caves))
                if Nop_caves[len(Nop_caves)-1] != Nop_caves[len(Nop_caves)-2]:
                    Nop_caves.remove(Nop_caves[len(Nop_caves)-1])
                Address = Nop_caves[0]
                #print("possible code cave at "+hex(Address)+"-", end = '')
                for i in range(len(Nop_caves)-1):
                    
                    if Nop_caves[i] > Address and Nop_caves[i]+1 != Nop_caves[i+1] :
                        #print(hex(Nop_caves[i]))
                        Nop_ranges.append(str(Address) + '-' + str(Nop_caves[i]))
                        try:
                          Address = Nop_caves[i+1]
                        except: 
                          break
                        #print("possible code cave at "+hex(Address)+"-", end = '')
                    

                #print(hex(Nop_caves[len(Nop_caves)-1]))

                x = Nop_ranges[0].split("-")
                range_size = int(x[1]) - int(x[0])
                target = Nop_ranges[0]

                for i in range(len(Nop_ranges)-1):
                    x = Nop_ranges[i].split("-")
                    if range_size<(int(x[1]) - int(x[0])):
                        range_size = int(x[1]) - int(x[0])
                        target = Nop_ranges[i]
                    elif range_size == (int(x[1]) - int(x[0])):
                        if target != Nop_ranges[i]:
                            target = target + "|" + Nop_ranges[i]
                x = target.split("-")
                print(hex(int(x[0]))+ "-" + hex(int(x[1])))
                print(hex(int(x[0])+4194304)+ "-" + hex(int(x[1])+4194304))
                y = str(hex(int(x[0]))+ "-" + hex(int(x[1])))
                y = y + " : " + str(hex(int(x[0])+4194304 + 4096 + 1536)+ "-" + str(hex(int(x[1])+4194304 + 4096 + 1536)))
                with open('cave.txt', 'w') as filehandle:
                    for listitem in Nop_ranges:
                        filehandle.write('%s\n' % listitem)
                
                label_file_explorer.configure(text = "Biggest code cave(Rest are in cave.txt) \n" + y)
                print(Nop_ranges)
                        

                                                                                                  
# Create the root window
window = Tk()
  
# Set window title
window.title('File Explorer')
  
# Set window size
window.geometry("330x160")
  
#Set window background color
window.config(background = "grey")
  
# Create a File Explorer label
label_file_explorer = Label(window,
                            text = "File Explorer using Tkinter",
                            width = 50, height = 2,
                            fg = "black")
  
      
button_explore = Button(window,
                        text = "Browse Files",
                        width = 30, height = 2,
                        command = browseFiles)
  
button_caves = Button(window,
                     text = "Find code caves",
                     width = 30, height = 2,
                     command = caves)

button_exit = Button(window,
                     text = "Exit",
                     width = 30, height = 2,
                     command = exit)
  
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)

  
button_explore.grid(column = 1, row = 2)
  
button_caves.grid(column = 1,row = 3)

button_exit.grid(column = 1,row = 4)
  
# Let the window wait for any events
window.mainloop()
