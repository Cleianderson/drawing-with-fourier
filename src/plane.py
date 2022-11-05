from numpy import pi as PI
import arcade as arc
from arcade.color import WHITE

from circle import Circle


class Plane(arc.Window):
    def __init__(self, width: int = 600, height: int = 600):
        super().__init__(width, height, "Fourier")
        # self.set_update_rate(1 / 30)

        self.center = {"x": width / 2, "y": height / 2}

        num_circs = 50
        self.circles = []
        for i in range(num_circs):
            n = 2*i + 1
            cn = 100 * (2 / (n * PI))
            self.circles.append(Circle(0, cn))

    def on_update(self, delta_time=10**3):
        super().on_update(delta_time)
        for n, circle in enumerate(self.circles):
            circle.update()

    def on_draw(self):
        self.clear()

        x = 900
        y = self.center.get("y")

        arc.start_render()
        for i, circle in enumerate(self.circles):
            angle = 2 * i + 1
            is_last = i + 1 == len(self.circles)
            x, y = circle.draw({"x": x, "y": y}, is_last, angle)
