import sys
try:
    # for Python 3
    from tkinter import *
except ImportError:
    # for Python 2
    from Tkinter import *
from random import * # for random placement of houses

# Import from our files
from TextureHandler import Textures
from Dog import Dog
from Cat import Cat
from Gui import GUI

class Map():
    """Base class for maps"""
    def __init__(self,filePath):
        self.mapList = [] 
        self.ReadSplit(filePath)
        self.ExitX = 100
        self.ExitY = 100

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
                
                # Add more elif for more options
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
                    gui.CreateImageRectangle(Textures.TextureDict["wall"],x,y)
                elif self.mapList[i][j] == "9":
                    gui.CreateImageRectangle(Textures.TextureDict["table"],x,y)
                elif self.mapList[i][j] == "10":
                    gui.CreateImageRectangle(Textures.TextureDict["bed"],x,y)
                elif self.mapList[i][j] == "11":
                    gui.CreateImageRectangle(Textures.TextureDict["door"],x,y)
                    # used to determine where the exit is in a house
                    self.ExitX = x 
                    self.ExitY = y
                elif self.mapList[i][j] == "12":
                    gui.CreateImageRectangle(Textures.TextureDict["box"],x,y)    
                else:
                    raise ValueError("Unidentified symbol was found in MapList")   
                
    def Search(self,gui,strTarget):
        """Search Imlementation
           Find all objects with specified texture
           strTarget - string for targeted texture"""
        canvasItems = gui.canvas.find_all()

        foundList = []

        # Linear search through list of items on canvas
        # we cannot use binary search since its not a number and there is no good criteria to sort by
        # since we are searching for an object with specific picture
        for i in canvasItems:
            if gui.canvas.itemcget(i,"image") == Textures.TextStr(strTarget):
                foundList.append(gui.canvas.coords(i))

        return foundList

    # Should be changed in child class or not used
    def Execute():
        print("BASE CLASS, shit went wrong OR u suck, @execute")

    def preChange():
        print("BASE CLASS, shit went wrong OR u suck, @change")

class mExterior(Map):
    """Exterior map class, 
       Inherits from map"""

    def __init__(self, filePath):
        super().__init__(filePath)

    def Execute(self,gui,dMaps,house):  

        gui.ClearFrame()
        gui.CreateCanvas()
        
        self.DisplayMap(gui)
        
        house.CreateObjects(gui.canvas,5,"house","grass")
        house.PlaceAllObjects(gui)

        cat = Cat(gui,Info.name,Textures.TextureDict["cat"],self.ExitX,self.ExitY)

        gui.root.bind("<z>",lambda event: self.preChange(gui.canvas.coords(cat.catID),gui,dMaps,house,cat)) # changes to inside map, <Return> is "enter" key                 

    def preChange(self,coords,gui,dMaps,house,cat): # move into one of the classes
        """Takes x,y coords in list,
           Checks if cat is standing on house and if yes proceeds to inside,
           or if the cat is on grass, ends the game"""

        ground = gui.canvas.itemcget(gui.canvas.find_overlapping(coords[0],coords[1],coords[0]+50,coords[1]+50)[0],"image")
        if ground == Textures.TextStr("bush"):
            cat.showInventory(GameOver = True)

        bool, ID = house.CheckOverlap(coords[0],coords[1],True)
        self.ExitX, self.ExitY = coords
        if not bool:
            dMaps["inside"].Execute(gui,dMaps,house,ID)

class mInterior(Map):
    """Interior map class, 
       Inherits from map"""

    def __init__(self, filePath):
        super().__init__(filePath)

    def Execute(self,gui,dMaps,house,ID):

        gui.ClearFrame()
        gui.CreateCanvas()

        self.DisplayMap(gui)

        house.FillHouse(gui,2,ID)

        cat = Cat(gui,Info.name,Textures.TextureDict["cat"],self.ExitX,self.ExitY,house.List[ID].item)
        dog = Dog(int(Info.difficulty),gui,Textures.TextureDict["dog"],cat)

        gui.root.bind("<z>",lambda event: self.preChange(cat.catID,gui,dMaps,house,dog)) # changes to ouside map, <Return> is "enter" key

        dog.movement(gui)

    def preChange(self,cat,gui,dMaps,house,dog):
        """changes into outside when on sofa only :D"""
        x,y = gui.canvas.coords(cat)
        if x == self.ExitX and y == self.ExitY:
            dog.STOP = True # DO NOT REMOVE, UNLESS U WANT MOVING HOUSES ...
            dMaps["outside"].Execute(gui,dMaps,house)

class Obj:
    # This would be a Struct if it was written in C++
    def __init__(self,x,y,texture):
        self.x = x
        self.y = y
        self.texture = texture
        self.ID = None
        # used for puting in boxes inside houses and putting items inside boxes :)
        self.item = None

class BaseRandomObject:
    """Random object Base class"""

    def __init__(self):
        self.List = []

    def PlaceObject(self,gui,i):
        """places created object on tkinter canvas,
           requires gui"""

        self.List[i].ID = gui.CreateImageRectangle(self.List[i].texture,self.List[i].x,self.List[i].y,returnOn = True)

    def CreateObjects(self,canvas,amount,texture,chkImage):
        """Creates specified amount of objects"""
        
        while len(self.List) != amount:
            rInt = randint(1,100) 
            x,y = canvas.coords(rInt)
            currImage = canvas.itemcget(rInt,"image")

            # Only place on specific tile and not overlap
            if currImage == Textures.TextStr(chkImage) and self.CheckOverlap(x,y):
                self.List.append(Obj(x,y,Textures.TextureDict[texture]))

    def CheckOverlap(self,x,y,returnID = False):
        """return true if none of current objects use the spot
           if returnID is True return bool and ID where it stopped"""

        ID = 0

        for h in self.List:
            if h.x == x and h.y == y:
                if returnID:
                    return False, ID
                else:
                    return False
            ID += 1
        if returnID:
            return True, ID
        else:
            return True

    def PlaceAllObjects(self,gui):
        """places ALL created objects on tkinter canvas,
           uses PlaceObject method"""

        for i in range(len(self.List)):
            self.PlaceObject(gui,i)

class Item:
    """Items go inside boxes! and to cat inventory"""
    def __init__(self,item,quality):
        """Enter item name, and quality int(1 being low quality, 5 being high quality) """
        self.item = item
        self.quality = quality

    # few special methods for printing
    def __repr__(self):
        return ("<" + self.item + ", " + str(self.quality) + " quality>")
    def __str__(self):
        return ("<" + self.item + ", " + str(self.quality) + " quality>")

class Box(BaseRandomObject):
    """Boxes Inside houses!"""
    def __init__(self):
       super().__init__()

       self.created = False

    def FillBox(self,ID):
        # places item into the box randomly 

        while self.List[ID].item == None:
            rInt = randint(0,len(Info.availableItems)-1)
            rInt2 = randint(1,5)

            if Info.selectedItems[rInt]:
                self.List[ID].item = Item(Info.availableItems[rInt],rInt2)

    def CreateObjects(self, canvas, amount, texture, chkImage):

        super().CreateObjects(canvas, amount, texture, chkImage)

        for i in range(len(self.List)):
            self.FillBox(i)

    def GiveItem(self,ID,gui):
        # gives item to cat and destroys box 

        item = self.List[ID].item

        gui.canvas.delete(self.List[ID].ID)
        self.List.pop(ID)
        
        return item     

class House(BaseRandomObject):
    """Houses placeable in Outside map """

    def __init__(self):
        super().__init__()

        self.boxCreated = False

    def FillHouse(self,gui,amount,ID):

        if self.List[ID].item == None:
            self.List[ID].item = Box()
            self.List[ID].item.CreateObjects(gui.canvas,amount,"box","floor")

        self.List[ID].item.PlaceAllObjects(gui)    

class Info:
    """Basic info from main menu"""

    name = ""
    difficulty = ""
    availableItems = ["Food","Toys","Mouse","Bells","Catnip","Milk","Trophy"]
    selectedItems = []

    def Transition(diffvar, catname, items,gui):
        for i in items:
            if i.get() == 1:
                Info.selectedItems.append(True)
            else:
                Info.selectedItems.append(False)

        Info.name = catname.get()
        Info.difficulty = diffvar.get()

        # Setup for rest of the program
        Textures.ReadTexture()

        dMaps = {}
    
        dMaps["outside"] = mExterior("Layouts/Outside Layout.txt")
        dMaps["inside"] = mInterior("Layouts/Inside Layout.txt")

        house = House()
    
        dMaps["outside"].Execute(gui,dMaps,house)

def mainmenu(gui):
    """Main menu, allows to choose all the things"""
    
    title = Label(gui.frame, text= "CAT HUNT!", fg="blue",font = "bold" )
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

    framebig = Frame(gui.frame)
    framebig.pack()
      
    lookfor = Label(framebig, text= "What do you wish to look for?", fg="blue")
    lookfor.pack()

    # adds a chechbox for every item in availableItems
    var = []
    for item in Info.availableItems:
        var.append(gui.CreatCheckBox(framebig,item))
    
    #select difficutly
    diffvar = IntVar()
        
    diff = Label(gui.frame, text="Select a difficulty",fg="blue", font = ("Arial",14))
    diff.pack()

    frame3 = Frame(gui.frame)
    frame3.pack()

    easy = Radiobutton(frame3, text = "Easy", fg = "green", variable = diffvar, value = 1)
    easy.pack(side = LEFT)
    med = Radiobutton(frame3, text = "Medium", fg = "orange", variable = diffvar, value = 2)
    med.pack(side = LEFT)
    med.select() # default difficulty
    hard = Radiobutton(frame3, text = "Hard", fg = "red", variable = diffvar, value = 3)
    hard.pack(side = LEFT)

    gui.CreateEmptySpace(gui.frame)
    
    #Tutorial Button
    tutorialbutton = Button(gui.frame, text="TUTORIAL",font = ("Arial",14,"bold"),fg = 'blue', command = lambda: tut_window(gui))
    tutorialbutton.pack()

    #Start Button
    startbutton = Button(gui.frame, text="PLAY!",font = ("Arial",14,"bold"),fg ='purple',command = lambda: Info.Transition(diffvar,catname,var,gui)) 
    startbutton.pack()

    gui.CreateEmptySpace(gui.frame)
    
def tut_window(self):
    # Function to create tutorial window.
    root2 = Tk()
    root2.title("Tutorial")

    # Text to be displayed in window.
    Tutorial_text = "Welcome to CatGame tutorial. Below is the controls for the game:\n\nTo move the cat simply use the directional arrow keys.\n\nz - enter/exit house. Press this when on the house icon from outside to enter; or on the couch when inside the house to exit.\n\nx - pick up item. Inside the house there will be boxes to collect with items inside. Simply go over the box and press x. The item is then stored in your inventory.\n\nc - view the inventory. If you wish to see what is currently in your inventory simply press c.\n\nAvoid the dogs! If you come in contact with a dog this will result in death. You will also lose an item that was collected.\n\nTo finish the game go to any of the bushes and press 'z'."

    # Creates the message withe the text being 'Tutorial_text'.
    msg = Message(root2, text = Tutorial_text)

    # Configurates the text font and background.
    msg.config(bg='white',fg='blue', font=('times',16,'bold'))

    # Packs the message into the window root2.
    msg.pack(side=LEFT)
    
def main():   
    # Setup tkinter
    root = Tk()
    gui = GUI(root,"Cat Hunt")

    # To main menu and beyond
    mainmenu(gui)
    
    # added to exit the program if the main window is closed. 
    # to close inventory window or any others if the main one is closed
    root.protocol("WM_DELETE_WINDOW",lambda:sys.exit()) 
    # Mainloop, MUST ALWAYS BE ON BOTTOM
    root.mainloop()
    
if __name__ == "__main__":
	sys.exit(main())
