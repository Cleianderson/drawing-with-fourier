from numpy import pi as PI
import arcade as arc

from circle import Circle


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

        self.period = period
        self.num_circs = num_circs
        self.create_circles(num_circs)

    def create_circles(self, num_circs: int = 1):
        _circles = []
        for i in range(num_circs):
            n = 2 * i + 1
            cn = 50 * (4 / (n * PI))
            _circles.append(Circle(0, cn))
        self.circles = _circles

    def on_key_press(self, key, modifiers):

        if key == arc.key.RIGHT:
            self.num_circs += 1
            self.create_circles(self.num_circs)
        elif key == arc.key.LEFT and self.num_circs > 0:
            self.num_circs -= 1
            self.create_circles(self.num_circs)

    def on_update(self, delta_time=10**3):
        super().on_update(delta_time)
        for n, circle in enumerate(self.circles):
            circle.update()

    def on_draw(self):
        self.clear()

        x = self.width / 2
        y = self.height / 2

        arc.start_render()
        for i, circle in enumerate(self.circles):
            angle = 2 * i + 1
            is_last = i + 1 == len(self.circles)
            x, y = circle.draw({"x": x, "y": y}, is_last, angle, x * 2, y * 2)
