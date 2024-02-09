import sys
from xml.dom import minidom

import matplotlib.pyplot as plt

import arcade as arc
import numpy as np
from arcade.csscolor import DARK_RED, ROYAL_BLUE, WHITE
from numpy import arctan2, cos, e, pi, sin, sqrt

from svg_parser import points_from_doc

SCALE = 300
TRANS_X = 450
TRANS_Y = 0
MAX_LEN = 400
K = 10

def __main__():
    def f(x):
      q = x // pi
      if q % 2 == 0:
        return 1
      return -1
    f = np.vectorize(f)
    
    U = fourier_coefs(f, K, 10**3, pi)

    complex_plane = ComplexPlane(U)
    complex_plane.run()


class ComplexPlane(arc.Window):
    def __init__(self, x):
        super().__init__(700, 550, fullscreen=True)
        arc.set_background_color(WHITE)

        # x = np.array(x) + TRANS_X
        # y = np.array(y) + TRANS_Y

        # complex_points = SCALE * (x + 1j * y)
        # self.f_coefs = fourier_coefs(complex_points)
        self.f_coefs = x
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
                _t = (SCALE / 3) * self.t + TRANS_X
                self.Y.extend([y1])
                # self.track.extend([(SCALE * (self.t + TRANS_X), y1)])

                if len(self.track) > MAX_LEN:
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
        self.t += 3e-2


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


def fourier_coefs(f, N, M, L):
    COEFS = []
    DX = 2 * L / M
    for k in range(1, N + 1):
        S = 0
        x = -L
        for _ in range(M):
            S += f(x) * e ** (-1j * k * pi * x / L) * DX
            x += DX
        S = S / (2*L)

        re, im = S.real, S.imag
        angle = arctan2(re, im)
        amplitude = sqrt(re**2 + im**2)
        frequence = k * pi / L

        COEFS.extend([(angle, SCALE * amplitude, frequence)])
    return COEFS


if __name__ == "__main__":
    __main__()
