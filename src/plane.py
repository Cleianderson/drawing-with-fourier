from numpy import pi as PI, e, sum, array, sqrt
from cmath import phase
import arcade as arc

from circle import Circle
from rabbit import rabbit
from pi import pi as _pi


class Plane(arc.Window):
    def __init__(
        self,
        width: int = 600,
        height: int = 600,
        period: float = 1,
        num_circs: int = 1,
        center=None,
    ):
        super().__init__(width, height, "Fourier", center_window=True)
        self.width = width
        self.height = height
        # self.set_update_rate(1 / 30)

        self.center = center if center != None else {"x": width / 2, "y": height / 2}

        X = []

        path = _pi[::8]
        scale = 1.5

        for point in path:
            X.append(point.get("x") / scale + point.get("y") / scale * 1j)

        fourier_y = self.discrete_fourier_transform(X)

        self.period = period
        self.num_circs = num_circs
        _circles = []
        for y in fourier_y:
            self.create_circles(num_circs)
            _circles.append(
                Circle(0, y.get("amp"), y.get("freq"), y.get("phase") + PI / 2)
            )
        self.circles = _circles

    def create_circles(self, num_circs: int = 1):
        for i in range(num_circs):
            n = 2 * i + 1
            cn = 50 * (4 / (n * PI))

    def on_update(self, delta_time=10**3):
        super().on_update(delta_time)
        for n, circle in enumerate(self.circles):
            circle.update(2 * PI / len(self.circles))

    def on_draw(self):
        self.clear()

        x = self.width / 2
        y = self.height / 2

        arc.start_render()
        for i, circle in enumerate(self.circles):
            angle = 1
            is_last = i + 1 == len(self.circles)
            x, y = circle.draw({"x": x, "y": y}, is_last, angle, x * 2, y * 2)

    def discrete_fourier_transform(self, arr_x):
        X = []
        N = len(arr_x)

        for k in range(N):
            S = 0
            for n in range(N):
                S += arr_x[n] * e ** (-2j * PI * k * n / N)

            re, im = S.real / N, S.imag / N
            S = re + im * 1j
            X.append(
                {
                    "re": re,
                    "im": im,
                    "phase": phase(S),
                    "amp": sqrt(re**2 + im**2),
                    "freq": k,
                }
            )

        return X
