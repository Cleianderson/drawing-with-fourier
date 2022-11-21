from numpy import pi
import arcade as arc

from circle import Circle


class Plane(arc.Window):
    def __init__(
        self,
        width: int = 600,
        height: int = 600,
        fourier_Y=[],
        max_len=300,
        bg=(200, 200, 200),
    ):
        super().__init__(width, height, "Fourier", center_window=True)
        arc.set_background_color(bg)

        self.width = width
        self.height = height
        self.max_len = max_len

        self.t = 0

        _circles = []
        self.len_fourier = len(fourier_Y)
        for y in fourier_Y:
            amp = y.get("amp")
            freq = y.get("freq")
            phase = y.get("phase")

            _circles.append(Circle(amp, freq, phase))
        self.circles = _circles

    def on_draw(self):
        self.clear()

        x = self.width / 2
        y = self.height / 2

        arc.start_render()
        for i, circle in enumerate(self.circles):
            is_last = i + 1 == len(self.circles)
            x, y = circle.draw({"x": x, "y": y}, is_last, self.t, self.max_len)
        arc.finish_render()

        self.t += 2 * pi / self.len_fourier
