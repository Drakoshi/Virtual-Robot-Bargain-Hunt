from TextureHandler import Textures
from Gui import GUI
try:
    # for Python 3
    from tkinter import *
except ImportError:
    # for Python 2
    from Tkinter import *
from random import randint

class Cat:
    """ Class for the cat; a.k.a the main character of the game"""

    deaths = 0
    inventory = []
          
    def __init__(self, gui, name, catBody,x,y,box = None):
        self.name = name
        self.catID = gui.CreateImageRectangle(catBody,x,y,returnOn = True)
        self.CatKeyBinds(gui,box)

    def death(self):
        """Drops an item and increases death count"""
        Cat.deaths += 1

        if not len(Cat.inventory) == 0:
            rInt = randint(0,len(Cat.inventory)-1)
            Cat.inventory.pop(rInt)
            print(self.name + " #" + str(Cat.deaths) +" died\nAnd dropped an item")
        else:
            print(self.name + " #" + str(Cat.deaths) +" died")

    def itemPickUp(self, Item):
        """takes item, the item should be class Item"""

        Cat.inventory.append(Item)
        print(str(Item)  + " added to inventory")

    def openBox(self,gui,box):
        """Checks if standing on box,
           and if its true it picks it up"""

        # in case of other map instances
        try:
            cX, cY = gui.canvas.coords(self.catID)

            boxUnd, ID = box.CheckOverlap(cX,cY,True)
            if not boxUnd:
                self.itemPickUp(box.GiveItem(ID,gui))
        except:
            pass

    def SortItems(self,criteria,gui,gameover):
        """Sorting items by different criteria,
           Using modifief Selection sort algorithm"""
        sortList = self.inventory 

        if criteria == "qualityD": # quality high to low
            for i in range(len(sortList)):
                for j in range(i+1,len(sortList)):
                    if sortList[i].quality < sortList[j].quality:
                        # Swapping elements
                        tmp = sortList[i]
                        sortList[i] = sortList[j]
                        sortList[j] = tmp
        
        elif criteria == "qualityA": # quality low to high
            for i in range(len(sortList)):
                for j in range(i+1,len(sortList)):
                    if sortList[i].quality > sortList[j].quality:
                        tmp = sortList[i]
                        sortList[i] = sortList[j]
                        sortList[j] = tmp

        elif criteria == "nameD": # name A-Z
            for i in range(len(sortList)):
                for j in range(i+1,len(sortList)):
                    if sortList[i].item > sortList[j].item:
                        tmp = sortList[i]
                        sortList[i] = sortList[j]
                        sortList[j] = tmp

        elif criteria == "nameA": # name Z-A
            for i in range(len(sortList)):
                for j in range(i+1,len(sortList)):
                    if sortList[i].item < sortList[j].item:
                        tmp = sortList[i]
                        sortList[i] = sortList[j]
                        sortList[j] = tmp

        # refresh window
        gui.ClearFrame()
        self.showInventory(gui,GameOver = gameover)

    def showInventory(self,gui = None, GameOver = False):
        """Seperate window for inventory"""

        # in case if the function is called from SortItems
        if gui == None:
            root = Tk()
            gui = GUI(root,"Inventory")

        # if we called this from entering the grass 
        if GameOver:
            label = Label(gui.frame,text = "Game over",fg = "red",font = ("Arial",16,"bold"))
            label.pack(padx = 100)

        label = Label(gui.frame,text = "Your cat has " + str(len(Cat.inventory)) + " items:")
        label.pack(padx = 100)

        for i in Cat.inventory:
            label = Label(gui.frame,text = str(i))
            label.pack(padx = 100)

        # Sort button stuff
        frame = Frame(gui.frame)
        frame.pack()

        b2 = Button(frame,text = "Name Z-A",command = lambda: self.SortItems("nameA",gui,GameOver))
        b2.pack(side = RIGHT)
        b1 = Button(frame,text = "Name A-Z",command = lambda: self.SortItems("nameD",gui,GameOver))
        b1.pack(side = RIGHT)    

        b3 = Button(frame,text = "Quality high-low",command = lambda: self.SortItems("qualityD",gui,GameOver))
        b3.pack(side = LEFT)
        b4 = Button(frame,text = "Quality low-high",command = lambda: self.SortItems("qualityA",gui,GameOver))
        b4.pack(side = LEFT)
        

        # Exit for the game!
        if GameOver:
            button = Button(gui.frame,text = "Exit",fg = "red",font = ("Arial",14,"bold"),command = lambda:gui.root.destroy())
            button.pack()

            gui.root.protocol("WM_DELETE_WINDOW",lambda:sys.exit()) 

        # Main loop
        gui.root.mainloop

    def CatKeyBinds(self,gui,box):
        """All key bindings associated with Cat"""

        gui.root.bind("<Left>", lambda event: self.LeftKey(gui,-50,0))
        gui.root.bind("<Right>", lambda event: self.RightKey(gui,50,0,500))
        gui.root.bind("<Up>", lambda event: self.UpKey(gui,0,-50))
        gui.root.bind("<Down>", lambda event: self.DownKey(gui,0,50,500))
        gui.root.bind("<x>",lambda event: self.openBox(gui,box))
        gui.root.bind("<c>",lambda event: self.showInventory())

    # Arrow key movement, and checking if not out of border
    def CheckAhead(self,gui,x,y):
        """Prevents from walking on fences and trees"""

        cX,cY = gui.canvas.coords(self.catID)

        cX += x
        cY += y

        ground = gui.canvas.itemcget(gui.canvas.find_overlapping(cX,cY,cX+50,cY+50)[0],"image")

        if not ground == Textures.TextStr("tree") and \
           not ground == Textures.TextStr("fenceH") and \
           not ground == Textures.TextStr("fenceV") and \
           not ground == Textures.TextStr("wall"):
            return True
        else:
            return False

    def LeftKey(self,gui,nX,nY):
        try:
            if gui.canvas.coords(self.catID)[0] > 0 and self.CheckAhead(gui,nX,nY):
                gui.MoveObject(self.catID, nX, nY)
        except:
            pass

    def RightKey(self,gui,nX,nY, canvasWidth):
        try:
            if gui.canvas.coords(self.catID)[0] < canvasWidth-50 and self.CheckAhead(gui,nX,nY):
                gui.MoveObject(self.catID, nX, nY)
        except:
            pass
        
    def DownKey(self,gui,nX,nY, canvasHeight):
        try:
            if gui.canvas.coords(self.catID)[1] < canvasHeight-50 and self.CheckAhead(gui,nX,nY):
                gui.MoveObject(self.catID, nX, nY)
        except:
            pass

    def UpKey(self,gui,nX,nY):
        try:
            if gui.canvas.coords(self.catID)[1] > 0 and self.CheckAhead(gui,nX,nY):
                gui.MoveObject(self.catID, nX, nY)
        except:
            pass
