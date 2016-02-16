﻿import sys
from tkinter import *
from random import * # for random placement of houses 

class GUI:

    def __init__(self,root):
        self.root = root
        self.frame = Frame(self.root)
        self.frame.pack()

        self.root.title("Cat Hunt")
       
    def CreateCanvas(self,wWidth,wHeight,Div,background = "white"):
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
        image = self.canvas.create_image(x,y,image = photo,anchor = anch)
        self.canvas.pack()
        
        if returnOn == True:
            return image

    def MoveObject(self,ID,X,Y):
        """Moves object,
           doesn't require canvas ouside :)"""
        self.canvas.move(ID,X,Y)

    def LeftKey(self,ID,nX,nY):
        self.canvas.move(ID, nX, nY)

    def RightKey(self,ID,nX,nY):
        self.canvas.move(ID, nX, nY)
        
    def DownKey(self,ID,nX,nY):
        self.canvas.move(ID, nX, nY)

    def UpKey(self,ID,nX,nY):
        self.canvas.move(ID, nX, nY)
    def GetCanvas(self):
        return self.canvas

    def GetMainFrame(self):
        return self.__frame

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
        Textures.TextureDict["cat"] = PhotoImage(file = "Textures/cat.png")
        Textures.TextureDict["house"] = PhotoImage(file = "Textures/House.png")
        Textures.TextureDict["a"] = PhotoImage(file = "Textures/pc1.png")
        Textures.TextureDict["b"] = PhotoImage(file = "Textures/pc2.png")

    def GetTextureKeys():
        return Textures.TextureDict.keys()

class Map():
    def __init__(self):
        self.mapList = [] 

    def ReadSplit(self,filePath):
        """Reads the map and places into 2D array/list,
           No returns, puts it directly into class"""

        # Read and close
        file = open(filePath,"r")
        string = file.read()
        file.close()
        # --------------

        # Splitting
        Pre = string.rsplit("\n")

        for i in Pre:
            self.mapList.append(i.split())

    def DisplayMap(self,gui,h,w,d):

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
                    gui.CreateImageRectangle(Textures.TextureDict["a"],x,y)
                elif self.mapList[i][j] == "4":
                    gui.CreateImageRectangle(Textures.TextureDict["b"],x,y)
                else:
                    raise ValueError("Unidentified symbol was found in MapList")    

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

def Outside(gui):
    gui.ClearFrame()
    mCanvasW= 500 # canvas width
    mCanvasH = 500 # canvas heigh
    mCanvasD = 50 # determines size of 1 block
    hNR = 5 # number of houses in game
    gui.CreateCanvas(mCanvasW,mCanvasH,mCanvasD,"black")

    # Reads and displays map
    map = Map()
    map.ReadSplit("Layouts/Outside Layout.txt")
    map.DisplayMap(gui,mCanvasW,mCanvasH,mCanvasD)

    # House part
    House.CreateHouses(gui.GetCanvas(),hNR)
    House.PlaceHouses(gui)
    # ----------------------

    # Make cat into class(OOP)
    Cat = gui.CreateImageRectangle(Textures.TextureDict["cat"],100,100,returnOn = True)

    gui.root.bind("<Left>", lambda event: gui.LeftKey(Cat,-50,0))
    gui.root.bind("<Right>", lambda event: gui.RightKey(Cat,50,0))
    gui.root.bind("<Up>", lambda event: gui.UpKey(Cat,0,-50))
    gui.root.bind("<Down>", lambda event: gui.DownKey(Cat,0,50))

    gui.root.bind("<a>",lambda event: Inside(gui)) # changes to inside map 

def Inside(gui):
    gui.ClearFrame()
    mCanvasW= 500 # canvas width
    mCanvasH = 500 # canvas heigh
    mCanvasD = 50 # determines size of 1 block
    hNR = 5 # number of houses in game

    gui.CreateCanvas(mCanvasW,mCanvasH,mCanvasD,"black")

    map2 = Map()
    map2.ReadSplit("Layouts/Inside Layout.txt")
    map2.DisplayMap(gui,mCanvasW,mCanvasH,mCanvasD)

    gui.root.bind("<a>",lambda event: Outside(gui)) # changes to ouside map
    
def main():

    mCanvasW= 500 # canvas width
    mCanvasH = 500 # canvas heigh
    mCanvasD = 50 # determines size of 1 block
    hNR = 5 # number of houses in game

    # Setup
    root = Tk()
    gui = GUI(root)  
    # ---------

    Textures.ReadTexture()

    Outside(gui)


    # Mainloop, MUST ALWAYS BE ON BOTTOM
    root.mainloop()
    
if __name__ == "__main__":
	sys.exit(main())