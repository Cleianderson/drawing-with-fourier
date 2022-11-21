import arcade as arc
from numpy import cos, sin, pi


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
        point_size = 4 if is_last else 2

        arc.draw_circle_outline(center.get("x"), center.get("y"), self.radius, color)

        arc.draw_point(x, y, color, point_size)

        arc.draw_line(x, y, center.get("x"), center.get("y"), color)

        if is_last:
            self.trace.append({"x": x, "y": y})

            while len(self.trace) > max_len:
                self.trace.pop(0)

            trace = []
            for point in self.trace:
                _x = point.get("x")
                _y = point.get("y")

                arc.draw_point(_x, _y, color, point_size)
                # trace.append((_x, _y))

            # arc.draw_line_strip(trace, color)

        return x, y
