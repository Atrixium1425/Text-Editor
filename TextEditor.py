from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter.font import Font, families
from tkinter import ttk
from tkinter import colorchooser
from tkinter.messagebox import *
import time
from time import strftime
import os, sys
import win32print, win32api

root = Tk()
root.title("Notepad")
root.iconphoto(False, PhotoImage(file = "NotepadIcon.png"))

#Global variables
global openstatusname
openstatusname = False

global selected
selected = False

global wordwrap
wordwrap = False

global nightmode
nightmode = False

global statusbarbool
statusbarbool = True

allFileTypes = (
            ("All Files", "*.*"), ("Text Files", "*.txt"),
            ("HTML Files", "*.html"), ("Python Files", "*.py"),
            ("JavaScript Files", "*.js"), ("CSS Files", "*.css"),
            ("Markdown Files", "*.md"))

#= = = = =
#Functions
#= = = = = 

#==============
#File Functions
#==============

#New File
def newfile(self):
    #Delete previous text
    text.delete("1.0", END)
    
    #Update status bars
    root.title("Notepad - New File")
    statusbar.config(text = "New File        ")

    global openstatusname
    openstatusname = False

#Open File
def openfile(self):
    #Delete previous text
    text.delete("1.0", END)

    #Grab Filename
    textfile = filedialog.askopenfilename(
        initialdir = "C:/gui/", title = "Open File", filetypes = allFileTypes)

    #Check if there is file name
    if textfile:
        #make filename global to access later
        global openstatusname
        openstatusname = textfile

    name = textfile
    statusbar.config(text = f"Notepad - {name}        ")
    name = name.replace("C:/gui/", "")
    root.title(f"Notepad - {name}")

    #Open file
    textfile = open(textfile, "r")
    stuff = textfile.read()
    text.insert(END, stuff)

    #Add file to textbox
    textfile.close()

#Save file
def savefile(self):
    global openstatusname
    if openstatusname:
        #Save the file
        textfile = open(openstatusname, "w")
        textfile.write(text.get(1.0, END))
        #Close the file
        textfile.close()
        
        statusbar.config(text = f"Notepad - Saved: {openstatusname}        ")
    else:
        saveasfile(self)

#Save as file
def saveasfile(self):
    global openstatusname
    textfile = filedialog.asksaveasfilename(
        defaultextension = ".*", initialdir = "C:/gui/", title = "Save File", filetypes = allFileTypes)

    if textfile:
        #Update status bars
        name = textfile
        statusbar.config(text = f"Notepad - Saved: {name}        ")
        name = name.replace("C:/gui/", "")
        root.title(f"Notepad - {name}")

        #Save the file
        textfile = open(textfile, "w")
        textfile.write(text.get(1.0, END))
        #Close the file
        textfile.close()
    openstatusname = True

#Print file function
def printfile(self):
    #printername = win32print.GetDefaultPrinter()
    #statusbar.config(text = printername)
    
    #Grab Filename
    filetoprint = filedialog.askopenfilename(
        initialdir = "C:/gui/", title = "Open File", filetypes = allFileTypes)

    if filetoprint:
        win32api.ShellExecute(0, "print", filetoprint, None, ".", 0)

#Quit program
def quitprogram(self):
    root.quit()

#==============
#Edit Functions
#==============

#Cut Text
def cuttext(e):
    global selected
    #Check if used keyboard shortcuts
    if e:
        selected = root.clipboard_get()
    else:
        if text.selection_get():
            #Grab selected text from textbox
            selected = text.selection_get()
            #Delete selected text from textbox
            text.delete("sel.first", "sel.last")
            #Clear clipboard, append
            root.clipboard_clear()
            root.clipboard_append(selected)

#Copy Text
def copytext(e):
    global selected
    #Check if used keyboard shortcuts
    if e:
        selected = root.clipboard_get()
    if text.selection_get():
        #Grab selected text from textbox
        selected = text.selection_get()
        #Clear clipboard, append
        root.clipboard_clear()
        root.clipboard_append(selected)
        
#Paste Text
def pastetext(e):
    global selected
    #Check if used keyboard shortcuts
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = text.index(INSERT)
            text.insert(position, selected)

#Select all Text
def selectall(e):
    #Add sel tag to select all
    text.tag_add("sel", "1.0", "end")

#Clear all Text
def clearall():
    text.delete(1.0, END)

#Print time and date
def timedate(self):
     string = strftime("%H:%M %d/%m/%Y")
     position = text.index(INSERT)
     text.insert(position, string)

#================
#Toobar Functions
#================

#Bold Text
def boldit():
    #Create font
    boldfont = font.Font(text, text.cget("font"))
    boldfont.configure(weight = "bold")

    #Configure tag
    text.tag_configure("bold", font = boldfont)

    #Define current tags
    currenttags = text.tag_names("sel.first")

    #If tag been set
    if "bold" in currenttags:
        text.tag_remove("bold", "sel.first", "sel.last")
    else:
        text.tag_add("bold", "sel.first", "sel.last")

#Italics Text
def italicsit():
    #Create font
    italicsfont = font.Font(text, text.cget("font"))
    italicsfont.configure(slant = "italic")

    #Configure tag
    text.tag_configure("italic", font = italicsfont)

    #Define current tags
    currenttags = text.tag_names("sel.first")

    #If tag been set
    if "italic" in currenttags:
        text.tag_remove("italic", "sel.first", "sel.last")
    else:
        text.tag_add("italic", "sel.first", "sel.last")

#===========================
#Toolbar & Colours Functions
#===========================

#Change text colour
def textcolour():
    #Pick colour
    colour = colorchooser.askcolor()[1]
    if colour:
        #Create font
        colourfont = font.Font(text, text.cget("font"))

        #Configure tag
        text.tag_configure("coloured", font = colourfont, foreground = colour )

        #Define current tags
        currenttags = text.tag_names("sel.first")

        #If tag been set
        if "coloured" in currenttags:
            text.tag_remove("coloured", "sel.first", "sel.last")
        else:
            text.tag_add("coloured", "sel.first", "sel.last")

#=================
#Colours Functions
#=================

#Define bg colour
def bgcolour():
    #Pick colour
    colour = colorchooser.askcolor()[1]
    if colour:
        text.config(bg = colour)

#Change all text colour
def alltextcolour():
    #Pick colour
    colour = colorchooser.askcolor()[1]
    if colour:
        text.config(fg = colour)

#=================
#Options Functions
#=================

#Turn on/off Word wrap
def wordwrap():
    global wordwrap
    if wordwrap:
        text.config(wrap = "word")
        wordwrap = False
    else:
        text.config(wrap = "none")
        wordwrap = True

#Change font
def fontselect():
    box = ttk.Combobox(root, values = fontoptions).pack()
    fontframe = Frame(root).pack()
    showinfo(title = "Font" )

#Turn on/off Night mode       
def nightmode():
    global nightmode
    if nightmode:    
        maincolour = "#000000"
        secondcolour = "#373737"
        textcolour = "#FFFFFF"
        
        root.config(bg = maincolour)
        statusbar.config(bg = maincolour, fg = textcolour)
        text.config(bg = secondcolour, fg = textcolour)
        toolbarframe.config(bg = maincolour)
        #Toolbar buttons
        boldbutton.config(bg = secondcolour, fg = textcolour)
        italicsbutton.config(bg = secondcolour, fg = textcolour)
        redobutton.config(bg = secondcolour, fg = textcolour)
        undobutton.config(bg = secondcolour, fg = textcolour)
        colourtextbutton.config(bg = secondcolour, fg = textcolour)
        #Menu colours
        filemenu.config(bg = maincolour, fg = textcolour)
        editmenu.config(bg = maincolour, fg = textcolour)
        colourmenu.config(bg = maincolour, fg = textcolour)
        optionsmenu.config(bg = maincolour, fg = textcolour)
        viewmenu.config(bg = maincolour, fg = textcolour)
        helpmenu.config(bg = maincolour, fg = textcolour)

        nightmode = False
    else:
        maincolour = "SystemButtonFace"
        secondcolour = "SystemButtonFace"
        textcolour = "#000000"
        
        root.config(bg = maincolour)
        statusbar.config(bg = maincolour, fg = textcolour)
        text.config(bg = "White", fg = textcolour)
        toolbarframe.config(bg = maincolour)
        #Toolbar buttons
        boldbutton.config(bg = secondcolour, fg = textcolour)
        italicsbutton.config(bg = secondcolour, fg = textcolour)
        redobutton.config(bg = secondcolour, fg = textcolour)
        undobutton.config(bg = secondcolour, fg = textcolour)
        colourtextbutton.config(bg = secondcolour, fg = textcolour)
        #Menu colours
        filemenu.config(bg = maincolour, fg = textcolour)
        editmenu.config(bg = maincolour, fg = textcolour)
        colourmenu.config(bg = maincolour, fg = textcolour)
        optionsmenu.config(bg = maincolour, fg = textcolour)
        viewmenu.config(bg = maincolour, fg = textcolour)
        helpmenu.config(bg = maincolour, fg = textcolour)

        nightmode = True

#==============
#View Functions
#==============

#Display about info
def statusbar():
    global statusbarbool
    if statusbarbool:
        statusbar.pack(fill = X, side = BOTTOM, ipady = 15)
        statusbarbool = False
    else:
        statusbar.pack_forget()
        statusbarbool = True
    
#==============
#Help Functions
#==============

#Display about info
def about():
    showinfo(title = "About Notepad", message = "Created by Brooklyn :D")
   
#Create toolbar frame
toolbarframe = Frame(root)
toolbarframe.pack(fill = X)

#Main frame
frame = Frame(root)
frame.pack(pady = 5)

#Vertical Scrollbar
textscroll = Scrollbar(frame)
textscroll.pack(side = RIGHT, fill = Y)

#Horizontal Scrollbar
horscroll = Scrollbar(frame, orient = "horizontal")
horscroll.pack(side = BOTTOM, fill = X)

#Text box
text = Text(frame, width = 100, height = 25, font = ("roboto", 16), selectbackground = "yellow",
            selectforeground = "black", undo = True, yscrollcommand = textscroll.set, wrap = "none", xscrollcommand = horscroll.set)
text.pack()

#Config scrollbar
textscroll.config(command = text.yview)
horscroll.config(command = text.xview)

#Menus
menu = Menu(root)
root.config(menu = menu)

#File menu
filemenu = Menu(menu, tearoff = False)
menu.add_cascade(label = "File", menu = filemenu)
filemenu.add_command(label = "New", command = lambda: newfile(False), accelerator = "(Ctrl+N)")
filemenu.add_command(label = "Open", command = lambda: openfile(False), accelerator = "(Ctrl+O)")
filemenu.add_command(label = "Save", command = lambda: savefile(False), accelerator = "(Ctrl+S)")
filemenu.add_command(label = "Save As", command = lambda: saveasfile(False), accelerator = "(Ctrl+Shift+S)")
filemenu.add_separator()
filemenu.add_command(label = "Print", command = lambda: printfile(False), accelerator = "(Ctrl+P)")
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = lambda: quitprogram(False), accelerator = "(Ctrl+Q)")

#Edit menu
editmenu = Menu(menu, tearoff = False)
menu.add_cascade(label = "Edit", menu = editmenu)
editmenu.add_command(label = "Cut", command = lambda: cuttext(False), accelerator = "(Ctrl+X)")
editmenu.add_command(label = "Copy", command = lambda: copytext(False), accelerator = "(Ctrl+C)")
editmenu.add_command(label = "Paste", command = lambda: pastetext(False), accelerator = "(Ctrl+V)")
editmenu.add_separator()
editmenu.add_command(label = "Undo", command = text.edit_undo, accelerator = "(Ctrl+Z)")
editmenu.add_command(label = "Redo", command = text.edit_redo, accelerator = "(Ctrl+Y)")
editmenu.add_separator()
editmenu.add_command(label = "Select All", command = lambda: selectall(False), accelerator = "(Ctrl+A)")
editmenu.add_command(label = "Clear All", command = clearall, accelerator = "(Ctrl+A+Del)")
editmenu.add_command(label = "Time/Date", command = lambda: timedate(False), accelerator = "(F5)")

#Colour menu
colourmenu = Menu(menu, tearoff = False)
menu.add_cascade(label = "Colours", menu = colourmenu)
colourmenu.add_command(label = "Change Selected Text Colour", command = textcolour)
colourmenu.add_command(label = "All Text", command = alltextcolour)
colourmenu.add_command(label = "Background", command = bgcolour)

#Options menu
optionsmenu = Menu(menu, tearoff = False)
menu.add_cascade(label = "Options", menu = optionsmenu)
optionsmenu.add_command(label = "Word Wrap", command = wordwrap)
optionsmenu.add_command(label = "Font", command = fontselect)
fontoptions = families(root)
optionsmenu.add_command(label = "Night Mode", command = nightmode)

#View menu
viewmenu = Menu(menu, tearoff = False)
menu.add_cascade(label = "View", menu = viewmenu)
viewmenu.add_command(label = "Status Bar", command = statusbar)

#Help menu
helpmenu = Menu(menu, tearoff = False)
menu.add_cascade(label = "Help", menu = helpmenu)
helpmenu.add_command(label = "About Notepad", command = about)

#Status Bar
statusbar = Label(root, text = "Ready       ", bd=1, relief=GROOVE, anchor = E)
statusbar.pack(fill = X, side = BOTTOM)

#File bindings
root.bind("<Control-Key-n>", newfile)
root.bind("<Control-Key-o>",openfile)
root.bind("<Control-Key-s>", savefile)
root.bind("<Control-Shift-Key-S>", saveasfile)
root.bind("<Control-Key-p>", printfile)
root.bind("<Control-Key-q>", quitprogram)

#Edit bindings
root.bind("<Control-Key-x>", cuttext)
root.bind("<Control-Key-c>", copytext)
root.bind("<Control-Key-v>", pastetext)
root.bind("<Control-A>", selectall)
root.bind("<Control-a>", selectall)
root.bind("<F5>", timedate)

#Buttons
#Bold Button
boldbutton = Button(toolbarframe,text = "Bold", command = boldit)
boldbutton.grid(row = 0, column = 0, sticky = W, padx = 5, pady = 5)
#Italics Button
italicsbutton = Button(toolbarframe,text = "Italics", command = italicsit)
italicsbutton.grid(row = 0, column = 1, sticky = W, padx = 5, pady = 5)
#Undo/Redo Buttons
undobutton = Button(toolbarframe,text = "Undo", command = text.edit_undo)
undobutton.grid(row = 0, column = 2, sticky = W, padx = 5, pady = 5)
redobutton = Button(toolbarframe,text = "Redo", command = text.edit_redo)
redobutton.grid(row = 0, column = 3, sticky = W, padx = 5, pady = 5)

#Text Colour
colourtextbutton = Button(toolbarframe, text = "Text Colour", command = textcolour)
colourtextbutton.grid(row = 0, column = 4, padx = 5, pady = 5)
root.mainloop()

