import os
import sys
from PIL import Image,ImageTk
def openImage(path,width,height):
    img=Image.open(path)
    img=img.resize((width,height),Image.ANTIALIAS)
    img=ImageTk.PhotoImage(img)
    return img
    
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)