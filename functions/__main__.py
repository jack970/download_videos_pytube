from PIL import Image
import customtkinter, io, requests, os, sys

def loadThumbnail(url):
        u = requests.get(url)
        image_open = Image.open(io.BytesIO(u.content))
        return customtkinter.CTkImage(image_open, size=(200, 200))

def resourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.getcwd())
    return os.path.join(base_path, relative_path)

LOGO = resourcePath("assets/logo.png")
ICON = resourcePath("assets/logo.ico")
LOCATION_FFMPEG = resourcePath("bin/ffmpeg.exe")