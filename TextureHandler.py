from tkinter import * # required for PhotoImage

"""Faced problems when i needed this class in Main and Cat files
   So moved it into seperate file"""

class Textures():
    TextureDict = {} # DICTIONARY POWAAHHH!

    def ReadTexture():
        """ Loads textures that are used in game
            USE ONCE ONLY """

        Textures.TextureDict["grass"] = PhotoImage(file = "Textures/grass.png")
        Textures.TextureDict["box"] = PhotoImage(file = "Textures/box.png")
        Textures.TextureDict["path"] = PhotoImage(file = "Textures/path.png")
        Textures.TextureDict["fenceH"] = PhotoImage(file = "Textures/fenceH.png")
        Textures.TextureDict["fenceV"] = PhotoImage(file = "Textures/fenceV.png")
        Textures.TextureDict["tree"] = PhotoImage(file = "Textures/tree.png")
        Textures.TextureDict["house"] = PhotoImage(file = "Textures/house.png")
        Textures.TextureDict["cat"] = PhotoImage(file = "Textures/cat.png")
        Textures.TextureDict["dog"] = PhotoImage(file = "Textures/dog.png")
        Textures.TextureDict["bush"] = PhotoImage(file = "Textures/bush.png")
        Textures.TextureDict["floor"] = PhotoImage(file = "Textures/floorboards.png")
        Textures.TextureDict["wall"] = PhotoImage(file = "Textures/wall.png")
        Textures.TextureDict["table"] = PhotoImage(file = "Textures/table.png")
        Textures.TextureDict["bed"] = PhotoImage(file = "Textures/bed.png")
        Textures.TextureDict["door"] = PhotoImage(file = "Textures/door.png")  

    def GetTextureKeys():
        return Textures.TextureDict.keys()

    def TextStr(textureName):
        return str(Textures.TextureDict[textureName])