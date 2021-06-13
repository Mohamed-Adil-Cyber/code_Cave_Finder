# import all components from the tkinter library
from tkinter import *

# used to make the icon file temporary
import tempfile
  
# import filedialog module
from tkinter import filedialog

# to Compress Image Icon
import base64, zlib

# browsed file
filename = ''

# nop inside an exe
empty_Space = 0


# icon image as base64
ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

# creating the icon image 
_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)
  
# function for opening the file explorer window
def browseFiles():
    global filename

    # select file types on browser
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("EXE files","*.exe*"),
                                                       ("DLL files","*.dll*"),                                                       
                                                       ("all files","*.*")))
      
    # change label contents
    label_file_explorer.configure(text="File Opened: "+filename)
      
    # activate cave button
    if filename != "":
        button_Caves.configure(state="normal")
    

# function to find caves
def caves():
                # initialize values
                global filename
                global empty_Space
                nop_Address = []
                nop_Saves = []
                nop_Ranges = []
                nop_Caves = []
                address = 0
                range_Size = 0
                file = open(filename, "rb")
                byte = file.read(1)

                
                #search for NOP
                while byte:
                    if byte == b'\x90':
                        empty_Space = empty_Space + 1
                        if len(nop_Address) != 0:
                            if address == nop_Address[len(nop_Address)-1]+1 :
                                nop_Address.append(address)
                                nop_Caves.append(address)
                                nop_Caves.append(address-1)
                            else:
                                nop_Address.append(address)
                        else:
                            nop_Address.append(address)
                        
                    byte = file.read(1)
                    address = address + 1

                    
                # sort and remove duplicates
                nop_Caves.sort()
                nop_Caves = list(dict.fromkeys(nop_Caves))
                if nop_Caves[len(nop_Caves)-1] != nop_Caves[len(nop_Caves)-2]:
                    nop_Caves.remove(nop_Caves[len(nop_Caves)-1]) 
                address = nop_Caves[0]


                # find ranges
                for i in range(len(nop_Caves)-1):        
                    if nop_Caves[i] > address and nop_Caves[i]+1 != nop_Caves[i+1] :
                        nop_Ranges.append(str(address) + '-' + str(nop_Caves[i]))
                        try:
                          address = nop_Caves[i+1]
                        except: 
                          break                    

                # turn offset into hex
                splitter = nop_Ranges[0].split("-")
                range_Size = int(splitter[1]) - int(splitter[0])
                target = nop_Ranges[0]
                

                # find largest offset
                for i in range(len(nop_Ranges)-1):
                    xsplit = nop_Ranges[i].split("-")
                    if range_Size<(int(xsplit[1]) - int(xsplit[0])):
                        range_Size = int(xsplit[1]) - int(xsplit[0])
                        target = nop_Ranges[i]
                    elif range_Size == (int(xsplit[1]) - int(xsplit[0])):
                        if target != nop_Ranges[i]:
                            target = target + "|" + nop_Ranges[i]

                            

                # store largest offset as hex
                splitted = target.split("-")
                label_Output = str(hex(int(splitted[0]))+ "-" + hex(int(splitted[1])))
                

                #write caves to cave.txt
                with open('cave.txt', 'w') as file_Handle:
                    for listitem in nop_Ranges:
                        splited_Caves = listitem.split("-")
                        file_Handle.write(str(hex(int(splited_Caves[0]))))
                        file_Handle.write("-")
                        file_Handle.write('%s\n' % str(hex(int(splited_Caves[1]))))
                        

                # update label        
                label_file_explorer.configure(text = "There are " + str(int(empty_Space/2)) + " bytes of empty space in the exe" + "\n Biggest offset is  "
                                              + label_Output + "\n The rest are stored in cave.txt")
                        

                                                                                                  
# create the root window
window = Tk()


window.iconbitmap(default=ICON_PATH)
  
# set window title
window.title('Code cave finder')
  
# set window size
window.geometry("330x173")
  
# set window background color
window.config(background = "grey")
  
# create a File Explorer label
label_file_explorer = Label(window,
                            text = "Browse your EXE/DLL file",
                            width = 50, height = 3,
                            fg = "black")
  
# file explorer button size     
button_Explore = Button(window,
                        text = "Browse Files",
                        width = 30, height = 2,
                        command = browseFiles)
# exe cave button finder  
button_Caves = Button(window,
                     text = "Find code caves",
                     state = DISABLED,
                     width = 30, height = 2,
                     command = caves)
# exit button size
button_Exit = Button(window,
                     text = "Exit",
                     width = 30, height = 2,
                     command = exit)
  
# grid method is chosen for placing the widgets at respective positions in a table like structure by specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)

  
# file explorer button
button_Explore.grid(column = 1, row = 2)
  
# find code caves
button_Caves.grid(column = 1,row = 3)

# exit button
button_Exit.grid(column = 1,row = 4)
  
# let the window wait for any events
window.mainloop()
