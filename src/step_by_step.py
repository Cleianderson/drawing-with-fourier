import sys
from xml.dom import minidom

import arcade
from arcade.csscolor import DARK_RED, ROYAL_BLUE, WHITE
from numpy import arctan2, cos, e, pi, sin, sqrt

from svg_parser import points_from_doc

SCALE = 5
TRANS_X = -50
TRANS_Y = -50

def __main__():
    _file = sys.argv[1]
    out_file = sys.argv[2]
    points = parse_file(_file)
    # points = [-191 - 191j, -191 + 191j, 191 + 191j, 191 - 191j]

    coefs = fourier_coefs(points)

    complex_plane = ComplexPlane(coefs, out_file)
    complex_plane.run()


class ComplexPlane(arcade.Window):
    def __init__(self, fourier_coefs, file):
        super().__init__(700, 550, fullscreen=False)
        arcade.set_background_color(WHITE)

        self.file = file
        self.n = 0
        self.track = []
        self.f_coefs = fourier_coefs

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            image = arcade.draw_commands.get_image().convert("RGB")
            image.save(f"{self.file}{self.n}.pdf")
        if key == arcade.key.UP:
            self.n += 1

    def on_draw(self):
        x0, y0 = self.width / 2, self.height / 2
        cN_1 = self.f_coefs[-1]
        arcade.start_render()
        arcade.draw_text(f'n = {self.n}', 0.05 * x0, 1.9 * y0, arcade.color.BLACK, 12)
        for coef in self.f_coefs:
            angle, amplitude, frequence = coef

            wn = frequence * self.n + angle
            x1 = amplitude * cos(wn) + x0
            y1 = amplitude * sin(wn) + y0

            arcade.draw_circle_outline(x0, y0, amplitude, (215, 215, 215), 3)
            arcade.draw_line(x1, y1, x0, y0, DARK_RED, 3)

            if coef is cN_1:
                self.track.extend([(x1, y1)])

                if len(self.track) > len(self.f_coefs):
                    # self.track.pop(0)
                    pass

                arcade.draw_line_strip(self.track, ROYAL_BLUE, 4)

            x0, y0 = x1, y1

        arcade.finish_render()
        # self.n += 1


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
