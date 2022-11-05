from numpy import pi as PI
import arcade as arc
from arcade.color import WHITE

from circle import Circle


class Plane(arc.Window):
    def __init__(self, width: int = 600, height: int = 600):
        super().__init__(width, height, "Fourier")

        self.center = {"x": width / 2, "y": height / 2}

        self.circles = []
        for i in range(1, 21):
            self.circles.append(Circle(0, 100 / i))

    def on_update(self, delta_time=10**3):
        super().on_update(delta_time)
        for n, circle in enumerate(self.circles):
            unit_angle = (-1) ** n * PI / 100
            circle.update(unit_angle)

    def on_draw(self):
        self.clear()

        x = 1000
        y = self.center.get("y")

        arc.start_render()
        for n, circle in enumerate(self.circles):
            is_last = n + 1 == len(self.circles)
            x, y = circle.draw({"x": x, "y": y}, is_last=is_last)
