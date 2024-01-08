import sys

from plane import Plane
from path import *

WIDTH = 700
HEIGHT = 700

def __main__():
    file_str = request_file()

    plane = Plane(file_str, WIDTH, HEIGHT)

    plane.run()

def request_file():
    file_str: str | None = None

    if len(sys.argv) == 2:
        file_str = sys.argv[1]
    else:
        file_str = input('path to svg file: ')
        
    return file_str.replace('\'', '').strip()
    

if __name__ == "__main__":
    __main__()
