import sys
from xml.dom import minidom

import arcade as arc
import numpy as np
from arcade.csscolor import DARK_RED, ROYAL_BLUE, WHITE
from numpy import arctan2, cos, e, pi, sin, sqrt

from svg_parser import points_from_doc

SCALE = 200 * (4/pi)
TRANS_X = 4
TRANS_Y = 0

def __main__():
    # _file = sys.argv[1]
    # out_file = sys.argv[2]
    # points = parse_file(_file)
    # points = [-191 - 191j, -191 + 191j, 191 + 191j, 191 - 191j]

    # coefs = fourier_coefs(points)
    f = lambda x: sin(x)
    X = np.linspace(0 , 2*pi)
    Y = f(X)

    complex_plane = ComplexPlane(X, Y, 0)
    complex_plane.run()


class ComplexPlane(arc.Window):
    def __init__(self, x, y, n):
        super().__init__(700, 550, fullscreen=True)
        arc.set_background_color(WHITE)

        # x = np.array(x) + TRANS_X
        # y = np.array(y) + TRANS_Y

        # complex_points = SCALE * (x + 1j * y)
        # self.f_coefs = fourier_coefs(complex_points)
        self.f_coefs = [(0, (1 / (2*k - 1)) * SCALE, 2*k - 1) for k in range(1, 51)]
        self.track = []
        self.t = 0
        self.Y = []
        self.X = []
        # self.n = n
        # self.f = function

    def on_key_press(self, key, modifiers):
        if key == arc.key.SPACE:
            image = arc.draw_commands.get_image().convert("RGB")
            image.save(f"{self.file}{self.t}.pdf")
        if key == arc.key.UP:
            self.t += 1

    def on_draw(self):
        x0, y0 = self.width / 2 - 400, self.height / 2
        cN_1 = self.f_coefs[-1]
        arc.start_render()
        arc.draw_text(f'n = {self.t}', 0.05 * x0, 1.9 * y0, arc.color.BLACK, 12)
        for coef in self.f_coefs:
            angle, amplitude, frequence = coef

            wn = frequence * self.t + angle
            x1 = amplitude * cos(wn) + x0
            y1 = amplitude * sin(wn) + y0

            arc.draw_circle_outline(x0, y0, amplitude, arc.color.LIGHT_GRAY)
            arc.draw_point(x1, y1, arc.color.DARK_GRAY, 6)
            arc.draw_line(x1, y1, x0, y0, arc.color.DARK_GRAY, 3)

            if coef is cN_1:
                _t = SCALE * (self.t + TRANS_X)
                self.Y.extend([y1])
                # self.track.extend([(SCALE * (self.t + TRANS_X), y1)])

                if len(self.track) > 220:
                    # self.track.pop(0)
                    # self.X.pop(0)
                    self.Y.pop(0)
                else:
                    self.X.extend([_t])

                self.track = np.column_stack([self.X[::-1], self.Y])

                arc.draw_line_strip(self.track, arc.color.BLACK, 5)
                arc.draw_line(x1, y1, self.X[0], y1, [120, 120, 120], line_width=2)

            
            x0, y0 = x1, y1

        arc.finish_render()
        self.t += 1.5e-2


def parse_file(file_str: str):
    _file = open(file_str)

    file_content = _file.read()

    doc = minidom.parseString(file_content)
    path = points_from_doc(doc, density=0.5, scale=SCALE, offset=(TRANS_X, TRANS_Y))

    points = []
    for coord in path:
        x = coord[0] 
        y = coord[1]

        points.extend([x + y * 1j])

    doc.unlink()
    return points


def fourier_coefs(X):
    COEFS = []
    N = len(X)
    for k in range(N):
        S = 0
        for n in range(N):
            S += X[n] * e ** (-2j * k * pi * n / N)
        S = S / N

        re, im = S.real, S.imag
        angle = arctan2(-im, re)
        amplitude = sqrt(re**2 + im**2)
        frequence = 2 * k * pi / N

        COEFS.extend([(angle, amplitude, frequence)])
    return COEFS


if __name__ == "__main__":
    __main__()
