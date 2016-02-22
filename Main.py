﻿import sys
from tkinter import *
from random import * # for random placement of houses 
from Dog import Dog
from Cat import Cat

class GUI:

    def __init__(self,root):
        self.root = root
        self.frame = Frame(self.root)
        self.frame.pack()

        self.root.title("Cat Hunt")
       
    def CreateCanvas(self,wWidth = 500, wHeight = 500, Div = 50,background = "white"):
        # Creates Canvas
        self.canvas = Canvas(self.frame,width = wWidth,height = wHeight,bg = background)
        self.canvas.pack()
        self.Div = Div

    def CreateRectangle(self,x,y,Fill = "white",Outline = "black", returnOn = False):
        # Wrapper for create rectangle function
        rect = self.canvas.create_rectangle(x, y, x + self.Div,y + self.Div, fill = Fill,outline = Outline)
        self.canvas.pack()
        
        # in case the ractangle as an object its needed else where
        if returnOn == True:
            return rect

    def CreateImageRectangle(self,photo,x,y,anch = NW,returnOn = False):
        """ Needs a loaded Photo .... """    
        imRect = self.canvas.create_image(x,y,image = photo,anchor = anch)
        self.canvas.pack()
        
        if returnOn == True:
            return imRect

    def CreatCheckBox(self,frame,Text):
        check = IntVar()
        checkbox = Checkbutton(frame, text= Text, variable = check)
        checkbox.pack()
        
        return check

    def CreateEmptySpace(self, frame,x = 1, y = 5):
        space = Frame(frame)
        space.pack(padx = x, pady = y)

    def MoveObject(self,ID,X,Y):
        """Moves object"""
        self.canvas.move(ID,X,Y)

    def ClearFrame(self):
        # As name suggests, cleats the main frame
        self.frame.destroy()
        self.frame = Frame(self.root)
        self.frame.pack()

class Textures():
    TextureDict = {} # DICTIONARY POWAAHHH!

    def ReadTexture():
        """ Loads textures that are used in game
            USE ONCE ONLY """

        Textures.TextureDict["grass"] = PhotoImage(file = "Textures/grass.png")
        Textures.TextureDict["path"] = PhotoImage(file = "Textures/path.png")
        Textures.TextureDict["fenceH"] = PhotoImage(file = "Textures/fenceH.png")
        Textures.TextureDict["fenceV"] = PhotoImage(file = "Textures/fenceV.png")
        Textures.TextureDict["tree"] = PhotoImage(file = "Textures/tree.png")
        Textures.TextureDict["house"] = PhotoImage(file = "Textures/house.png")
        Textures.TextureDict["cat"] = PhotoImage(file = "Textures/cat.png")
        Textures.TextureDict["dog"] = PhotoImage(file = "Textures/dog.png")
        Textures.TextureDict["bush"] = PhotoImage(file = "Textures/bush.png")
        Textures.TextureDict["floor"] = PhotoImage(file = "Textures/floorboards.png")
        Textures.TextureDict["books"] = PhotoImage(file = "Textures/bookshelf.png")
        Textures.TextureDict["table"] = PhotoImage(file = "Textures/table.png")
        Textures.TextureDict["bed"] = PhotoImage(file = "Textures/bed.png")
        Textures.TextureDict["sofa"] = PhotoImage(file = "Textures/sofa.png")
        Textures.TextureDict["box"] = PhotoImage(file = "Textures/box.png")

    def GetTextureKeys():
        return Textures.TextureDict.keys()

class Map():
    def __init__(self,filePath):
        self.mapList = [] 
        self.ReadSplit(filePath)

    def ReadSplit(self,filePath):
        """Reads the map and places into 2D array/list,
           no returns, puts it directly into class"""

        file = open(filePath,"r")
        string = file.read()
        file.close()

        Pre = string.rsplit("\n")

        for i in Pre:
            self.mapList.append(i.split())

    def DisplayMap(self,gui,h = 500, w = 500, d = 50):

        for i in range(int(h / d)):
            y = i * d
            for j in range(int(w / d)):
                x = j * d
                
                #add more elif for more options

                if self.mapList[i][j] == "1":
                    gui.CreateImageRectangle(Textures.TextureDict["grass"],x,y)
                elif self.mapList[i][j] == "2":
                    gui.CreateImageRectangle(Textures.TextureDict["path"],x,y)
                elif self.mapList[i][j] == "3":
                    gui.CreateImageRectangle(Textures.TextureDict["tree"],x,y)
                elif self.mapList[i][j] == "4":
                    gui.CreateImageRectangle(Textures.TextureDict["fenceH"],x,y)
                elif self.mapList[i][j] == "5":
                    gui.CreateImageRectangle(Textures.TextureDict["fenceV"],x,y)
                elif self.mapList[i][j] == "6":
                    gui.CreateImageRectangle(Textures.TextureDict["bush"],x,y)
                elif self.mapList[i][j] == "7":
                    gui.CreateImageRectangle(Textures.TextureDict["floor"],x,y)
                elif self.mapList[i][j] == "8":
                    gui.CreateImageRectangle(Textures.TextureDict["books"],x,y)
                elif self.mapList[i][j] == "9":
                    gui.CreateImageRectangle(Textures.TextureDict["table"],x,y)
                elif self.mapList[i][j] == "10":
                    gui.CreateImageRectangle(Textures.TextureDict["bed"],x,y)
                elif self.mapList[i][j] == "11":
                    gui.CreateImageRectangle(Textures.TextureDict["sofa"],x,y)
                elif self.mapList[i][j] == "12":
                    gui.CreateImageRectangle(Textures.TextureDict["box"],x,y)    
                else:
                    raise ValueError("Unidentified symbol was found in MapList")       

    def Execute():
        print("BASE CLASS, shit went wrong OR u suck, @execute")

    def preChange():
        print("BASE CLASS, shit went wrong OR u suck, @change")

class mExterior(Map): # make into class like inside 
    def __init__(self, filePath):
        super().__init__(filePath)
        self.hNR = 5 # number of houses in game

    def Execute(self,gui,dMaps):  
        gui.ClearFrame()
        gui.CreateCanvas()
        
        self.DisplayMap(gui)
        
        House.CreateHouses(gui.canvas,self.hNR)    
        House.PlaceHouses(gui)

        cat = Cat(gui,Info.name,Textures.TextureDict["cat"],100,100)

        gui.root.bind("<Return>",lambda event: self.preChange(gui.canvas.coords(cat.catID),gui,dMaps)) # changes to inside map, <Return> is "enter" key

    def preChange(self,coords,gui,dMaps): # move into one of the classes
        """Takes x,y coords in list,
           Checks if cat is standing on house and if yes proceeds to inside"""
        if not House.CheckOverlap(coords[0],coords[1]):
            dMaps["inside"].Execute(gui,dMaps)

class mInterior(Map): # adapt for multiple instances
    def __init__(self, filePath):
        super().__init__(filePath)

    def Execute(self,gui,dMaps):
        gui.ClearFrame()
        gui.CreateCanvas()

        self.DisplayMap(gui)

        cat = Cat(gui,Info.name,Textures.TextureDict["cat"],200,200)

        dog = Dog(int(Info.difficulty),gui,Textures.TextureDict["dog"],cat.catID)
        dog.movement(gui)

        gui.root.bind("<Return>",lambda event: self.preChange(gui,dMaps)) # changes to ouside map, <Return> is "enter" key

    def preChange(self,gui,dMaps):
        """PLACE HOLDER FOR NOW, goes to another map"""
        dMaps["outside"].Execute(gui,dMaps)

class House():
    """If used via CreateHouses then
       It contains list of itself"""
    HouseList = []

    def __init__(self,x,y,texture):
        self.x = x
        self.y = y
        self.texture = texture
        self.ID = None

    def CreateHouses(canvas,amount):
        """Creates specified amount of houses"""
        
        while len(House.HouseList) != amount:
            rInt = randint(1,100) 
            x,y = canvas.coords(rInt)
            currImage = canvas.itemcget(rInt,"image")


            # place only on grass and not on another house
            if currImage == "pyimage1" and House.CheckOverlap(x,y):
                House.HouseList.append(House(x,y,Textures.TextureDict["house"]))

    def CheckOverlap(x,y):
        """return true if none of current houses use the spot"""
        for h in House.HouseList:
            if h.x == x and h.y == y:
                return False
        
        return True

    def PlaceHouses(gui):
        """places created houses on tkinter canvas,
           requires gui because it uses its function"""
        for h in House.HouseList:
            h.ID = gui.CreateImageRectangle(h.texture,h.x,h.y,NW,True)

class Info:
    name = ""
    difficulty = ""
    itemList = []

    def MenuMapTrans(diffvar, catname, items,gui,dMaps):

        list = []
        for i in items:
            list.append(i.get())

        Info.name = catname.get()
        Info.difficulty = diffvar.get()
        Info.itemList = list
    
        dMaps["outside"].Execute(gui,dMaps)

def mainmenu(gui,dMaps):
    #title
    title = Label(gui.frame, text= "CAT HUNT!", fg="blue",font = 'bold' )
    title.pack()

    gui.CreateEmptySpace(gui.frame)

    #inputing the cats name
    frame1 = Frame(gui.frame)
    frame1.pack( )

    catnametext = Label(frame1,text="Cat name?", fg = "blue").pack(side = LEFT)
    catname = Entry(frame1, fg = "blue")
    catname.pack(side = LEFT)
    
    gui.CreateEmptySpace(gui.frame)

    #Different types of items

    framebig =Frame(gui.frame)
    framebig.pack()
      
    lookfor = Label(framebig, text= "What do you wish to look for?", fg="blue")
    lookfor.pack()

    var = []
    var.append(gui.CreatCheckBox(framebig,"Food"))
    var.append(gui.CreatCheckBox(framebig,"Toy"))
    var.append(gui.CreatCheckBox(framebig,"Mouse"))
    var.append(gui.CreatCheckBox(framebig,"Bells"))
    var.append(gui.CreatCheckBox(framebig,"Catnip"))
    var.append(gui.CreatCheckBox(framebig,"Milk"))
    var.append(gui.CreatCheckBox(framebig,"Mittens"))
    
    #select difficutly
    diffvar = IntVar()
        
    diff = Label(gui.frame, text="Select a difficulty",fg="blue", font = ("Arial",14))
    diff.pack()

    frame3 = Frame(gui.frame)
    frame3.pack()

    easy = Radiobutton(frame3, text = "Easy", fg = "green", variable = diffvar, value = 1)
    easy.pack(side = LEFT,)
    med = Radiobutton(frame3, text = "Medium", fg = "orange", variable = diffvar, value = 2)
    med.pack(side = LEFT)
    hard = Radiobutton(frame3, text = "Hard", fg = "red", variable = diffvar, value = 3)
    hard.pack(side = LEFT)

    gui.CreateEmptySpace(gui.frame)

    #Start Button
    startbutton = Button(gui.frame, text="PLAY!",font = ("Arial",14,"bold"),fg ='purple',command = lambda: Info.MenuMapTrans(diffvar,catname,var,gui,dMaps)) 
    startbutton.pack()

    gui.CreateEmptySpace(gui.frame)
    
def main():   
    # Setup
    root = Tk()
    gui = GUI(root)

    Textures.ReadTexture()

    dMaps = {}
    
    # add other maps here
    dMaps["outside"] = mExterior("Layouts/Outside Layout.txt")
    dMaps["inside"] = mInterior("Layouts/Inside Layout.txt")

    # Main Stuff
    mainmenu(gui,dMaps)
    
    # Mainloop, MUST ALWAYS BE ON BOTTOM
    root.mainloop()
    
if __name__ == "__main__":
	sys.exit(main())
