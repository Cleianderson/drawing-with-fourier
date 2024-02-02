from xml.dom import minidom

import arcade as arc
from numpy import arctan2, e, pi, sqrt

from circle import Circle
from svg_parser import points_from_doc


class Plane(arc.Window):
    def __init__(
        self,
        file_str: str,
        width: int = 600,
        height: int = 600,
        bg=(200, 200, 200),
    ):
        super().__init__(
            width, height, "Fourier", center_window=True, update_rate=1 / 24
        )
        arc.set_background_color(bg)

        self.width = width
        self.height = height

        self.step = 1
        self.scale = 1.5
        self.trans_x = -200
        self.trans_y = -200

        points = self.parse_file(file_str)
        self.max_len = len(points)

        self.t = 0

        self.len_fourier = len(points)
        self.create_circles(points)

    def on_draw(self):
        self.clear()

        x = self.width / 2
        y = self.height / 2

        arc.start_render()
        for i, circle in enumerate(self.circles):
            is_last = i + 1 == len(self.circles)
            x, y = circle.draw({"x": x, "y": y}, is_last, self.t, self.max_len)
        arc.finish_render()

        self.t += 1

    def create_circles(self, points):
        _circles = []

        for y in points:
            amp = y.get("amp")
            freq = y.get("freq")
            phase = y.get("phase")

            _circles.append(Circle(amp, freq, phase))
        self.circles = _circles

    def discrete_fourier_transform(self, arr_x):
        X = []
        N = len(arr_x)
        # N = 2L => L = N / 2

        for k in range(0, N):
            S = 0
            for n in range(0, N):
                S += arr_x[n] * e ** (-2j * pi * k * n / N)
            S = S / (N)
            re, im = S.real, S.imag
            X.append(
                {
                    "re": re,
                    "im": im,
                    "phase": arctan2(re, im),
                    "amp": sqrt(re**2 + im**2),
                    "freq": 2 * k * pi / N,
                }
            )

        return X

    def parse_file(self, file_str: str):
        _file = open(file_str)

        file_content = _file.read()

        doc = minidom.parseString(file_content)
        path = points_from_doc(doc, density=0.5, scale=5, offset=(25, 0))

        points = []
        for coord in path[:: self.step]:
            x = coord[0] / self.scale + self.trans_x
            y = coord[1] / self.scale + self.trans_y

            points.extend([x + y * 1j])

        doc.unlink()

        dft_points = self.discrete_fourier_transform(points)

        def sort_fn(point):
            return point["amp"]
        
        dft_points.sort(reverse=True, key=sort_fn)

        return dft_points
