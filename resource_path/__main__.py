import os, sys

def resourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.getcwd())
    return os.path.join(base_path, "assets", relative_path)