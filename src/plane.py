from numpy import pi as PI
import arcade as arc
from arcade.color import WHITE

from circle import Circle


class Plane(arc.Window):
    def __init__(self, width: int = 600, height: int = 600):
        super().__init__(width, height, "Fourier")
        # self.set_update_rate(1 / 30)

        self.center = {"x": width / 2, "y": height / 2}

        self.period = 1
        num_circs = 50
        self.circles = []
        for i in range(num_circs):
            n = i + 1
            cn = 100 * ((4 * self.period**2 * (-1) ** n) / (n * PI) ** 2)
            self.circles.append(Circle(0, cn))

    def on_update(self, delta_time=10**3):
        super().on_update(delta_time)
        for n, circle in enumerate(self.circles):
            circle.update()

    def on_draw(self):
        self.clear()

        x = 900
        y = 500

        arc.start_render()
        for i, circle in enumerate(self.circles):
            angle = (i + 1) * PI
            is_last = i + 1 == len(self.circles)
            x, y = circle.draw({"x": x, "y": y}, is_last, angle)
