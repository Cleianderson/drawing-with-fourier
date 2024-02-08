import arcade as arc
from numpy import cos, sin, pi, sqrt


class Circle:
    def __init__(self, radius=1, freq=1, phase=0) -> None:
        self.phase = phase
        self.radius = radius
        self._freq = freq
        self.trace = []

    def draw(
        self,
        center={"x": 0, "y": 0},
        is_last=False,
        t=1,
        max_len=300,
        colors=[175, 120],
    ):
        phi = self._freq * t + self.phase - pi / 2

        x = self.radius * cos(phi) + center.get("x")
        y = self.radius * sin(phi) + center.get("y")

        color = [colors[1]] * 3 if is_last else [colors[0]] * 3
        point_size = 4 if is_last else 3

        arc.draw_circle_outline(center.get("x"), center.get("y"), self.radius, arc.color.WHITE_SMOKE)

        arc.draw_point(x, y, color, point_size)

        arc.draw_line(x, y, center.get("x"), center.get("y"), arc.color.LIGHT_GRAY, line_width=1.5)

        if is_last:
            self.trace.append({"x": x, "y": y})

            while len(self.trace) > max_len:
                self.trace.pop(0)

            trace = []
            for i in range(len(self.trace) - 1):
                x0 = self.trace[i].get("x")
                y0 = self.trace[i].get("y")
                x1 = self.trace[i + 1].get("x")
                y1 = self.trace[i + 1].get("y")

                if sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2) <= 50:
                # arc.draw_point(_x, _y, color, point_size)
                    arc.draw_line(x0, y0, x1, y1, color, line_width=3)
                # trace.append((_x, _y))

            # arc.draw_line_strip(trace, color, line_width=3)

        return x, y
