from TextureHandler import Textures
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
        """Search Imlementation for houses, but no navigation to houses :(
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
