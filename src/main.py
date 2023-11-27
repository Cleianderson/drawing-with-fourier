from numpy import arctan2, sqrt, e, pi
from svg_parser import points_from_doc
from xml.dom import minidom


from plane import Plane
from path import *

global Y
global fourier_Y

WIDTH = 700
HEIGHT = 700
RADIUS = 100

CENTER = {"x": WIDTH / 2, "y": HEIGHT / 2}

STEP = 1
SCALE = 1.5
TRANS_X = -200
TRANS_Y = -200


def __main__():
    Y = []
    file_str = input('path to svg file: ')
    file_str = file_str.replace('\'', '').strip()
    print(file_str)

    _file = open(file_str)

    path_str = _file.read()

    doc = minidom.parseString(path_str)
    path = points_from_doc(doc, density=0.5, scale=5, offset=(25, 0))

    for coord in path[::STEP]:
        Y.append((coord[0] / SCALE + TRANS_X) + (coord[1] / SCALE + TRANS_Y) * 1j)

    fourier_Y = discrete_fourier_transform(Y)

    plane = Plane(WIDTH, HEIGHT, fourier_Y, len(fourier_Y))
    plane.run()

    doc.unlink()


def discrete_fourier_transform(arr_x):
    X = []
    N = len(arr_x)

    for k in range(N):
        S = 0
        for n in range(N):
            S += arr_x[n] * e ** (-2j * pi * k * n / N)

        re, im = S.real / N, S.imag / N
        S = re + im * 1j
        X.append(
            {
                "re": re,
                "im": im,
                "phase": arctan2(re, im),
                "amp": sqrt(re**2 + im**2),
                "freq": k,
            }
        )

    return X


if __name__ == "__main__":
    __main__()
