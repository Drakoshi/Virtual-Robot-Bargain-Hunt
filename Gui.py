from tkinter import *

"""Faced problems when i needed this class in Main and Cat files
   So moved it into seperate file"""


class GUI:
    """Gui wrapper, using tkinter"""
    # pretty much everything is self-explanationary

    def __init__(self,root,title):
        self.root = root
        self.frame = Frame(self.root)
        self.frame.pack()

        self.root.title(title)    
       
    def CreateCanvas(self,wWidth = 500, wHeight = 500, Div = 50,background = "white"):
        self.canvas = Canvas(self.frame,width = wWidth,height = wHeight,bg = background)
        self.canvas.pack()
        self.Div = Div

    def CreateRectangle(self,x,y,Fill = "white",Outline = "black", returnOn = False):
        # Wrapper for create rectangle function
        rect = self.canvas.create_rectangle(x, y, x + self.Div,y + self.Div, fill = Fill,outline = Outline)
        self.canvas.pack()
        
        # Returns object ID
        if returnOn == True:
            return rect

    def CreateImageRectangle(self,photo,x,y,anch = NW,returnOn = False):
        """ Needs a loaded Photo .... """    
        imRect = self.canvas.create_image(x,y,image = photo,anchor = anch)
        self.canvas.pack()
        
        # Returns object ID
        if returnOn == True:
            return imRect

    def CreatCheckBox(self,frame,Text):
        check = IntVar()
        checkbox = Checkbutton(frame, text= Text, variable = check)
        checkbox.pack(side = LEFT)
        
        return check

    def CreateEmptySpace(self, frame,x = 1, y = 5):
        space = Frame(frame)
        space.pack(padx = x, pady = y)

    def MoveObject(self,ID,X,Y):
        self.canvas.move(ID,X,Y)

    def ClearFrame(self):
        self.frame.destroy()
        self.frame = Frame(self.root)
        self.frame.pack()
