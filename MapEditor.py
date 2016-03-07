# Create map editor here add as a button to main menu!

from Gui import *
from TextureHandler import Textures
from tkinter import *
from Map import Map


class MapEditor(Map):
    def __init__(self,origMap):
        self.root = Toplevel()
        self.gui = GUI(self.root,"Map Editor")

        self.orig = origMap.get()
        self.preChange()

        self.root.mainloop()

    def preChange(self):

        if self.orig == 1:
            Outside = "Layouts/Outside Layout Original.txt"
            Inside = "Layouts/Inside Layout Original.txt"
        else:
            Outside = "Layouts/Outside Layout.txt"
            Inside = "Layouts/Inside Layout.txt"

        but = Button(self.gui.frame,text = "Outside",command = lambda: self.Execute(Outside))
        but.pack()
        
        but2 = Button(self.gui.frame,text = "Inside",command = lambda: self.Execute(Inside))
        but2.pack()

        but3 = Button(self.gui.frame,text = "Exit",command = lambda:self.root.destroy())
        but3.pack()

    def Execute(self,filePath):
        super().__init__(filePath)

        self.instance = None
        self.fPath = filePath

        if self.fPath == "Layouts/Outside Layout.txt" or self.fPath == "Layouts/Outside Layout Original.txt":
            self.instance = "out"
            self.fPath = "Layouts/Outside Layout.txt" 

        elif self.fPath == "Layouts/Inside Layout.txt" or self.fPath == "Layouts/Inside Layout Original.txt":
            self.instance = "in"
            self.fPath = "Layouts/Inside Layout.txt"
        
        self.gui.ClearFrame()
        self.gui.CreateCanvas()
        self.DisplayMap(self.gui)

        self.selected = None

        self.MakeButtons()

        self.gui.canvas.bind("<Button-1>", self.Select)
        self.gui.canvas.pack()

    def MakeButtons(self):

        list = []
        if self.instance == "out":
            list = ["grass","path","tree","bush","fenceV","fenceH"]
        elif self.instance == "in":
            list = ["floor","wall","table","bed"]

        for i in range(len(list)):
            button = Button(self.gui.frame,image = Textures.TextureDict[list[i]],command = lambda id = i:self.SelectTile(list,id)) # Thanks David Croft 
            button.pack(side = LEFT)

        button = Button(self.gui.frame,text = "Exit",command = lambda:self.gui.root.destroy())
        button.pack(side = RIGHT)

        button = Button(self.gui.frame,text = "Reset",command = lambda: self.Reset())
        button.pack(side = RIGHT)

        button = Button(self.gui.frame,text = "Save",command = lambda: self.Save())
        button.pack(side = RIGHT)

    def SelectTile(self,list,id):
        self.selected = Textures.TextStr(list[id])

    def Select(self, event):
        objectID = self.gui.canvas.find_closest(event.x, event.y)[0]
        #print(objectID)
        if self.selected != None:
            self.gui.canvas.itemconfig(objectID,image = self.selected)

    def Save(self):
        file = open(self.fPath,"w")
        file.write("")
        file.close()

        file = open(self.fPath,"a")
        for i in range(10):
            for j in range(1,11):
                img = self.gui.canvas.itemcget(i*10+j,"image")

                if img == Textures.TextStr("grass"):
                    file.write(str(1))
                elif img == Textures.TextStr("path"):
                    file.write(str(2))
                elif img == Textures.TextStr("tree"):
                    file.write(str(3))
                elif img == Textures.TextStr("fenceH"):
                    file.write(str(4))
                elif img == Textures.TextStr("fenceV"):
                    file.write(str(5))
                elif img == Textures.TextStr("bush"):
                    file.write(str(6))
                elif img == Textures.TextStr("floor"):
                    file.write(str(7))
                elif img == Textures.TextStr("wall"):
                    file.write(str(8))
                elif img == Textures.TextStr("table"):
                    file.write(str(9))
                elif img == Textures.TextStr("bed"):
                    file.write(str(10))
                elif img == Textures.TextStr("door"):
                    file.write(str(11))
                else:
                    raise ValueError("Unknown " + str(img))

                file.write(" ")

            file.write("\n")

        file.close()

    def Reset(self):
        self.gui.ClearFrame()
        self.Execute(self.fPath)
   
