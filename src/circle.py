import arcade as arc
from arcade.color import WHITE, YELLOW, GREEN
from numpy import cos, sin


class Circle:
    def __init__(self, angle=0, radius=1, freq=1, phase=0) -> None:
        self.angle = angle
        self.phase = phase
        self.radius = radius
        self._freq = freq
        self.trace = []

    def update(self, unit_angle=0.02):
        self.angle += unit_angle

    def draw(self, center={"x": 0, "y": 0}, is_last=False, angle=1, width=1, height=1):
        x = self.radius * cos(self._freq * self.angle + self.phase) + center.get("x")
        y = self.radius * sin(self._freq * self.angle + self.phase) + center.get("y")

        color = WHITE if is_last else arc.make_transparent_color(WHITE, 50)
        point_size = 5 if is_last else 2

        arc.draw_circle_outline(center.get("x"), center.get("y"), self.radius, color)

        arc.draw_point(x, y, color, point_size)

        arc.draw_line(x, y, center.get("x"), center.get("y"), color)

        if is_last:
            self.trace.append({"x": x, "y": y})

            while len(self.trace) > 300:
                self.trace.pop(0)

            trace = []
            # trace_y = []
            # trace_x = []
            for index, point in enumerate(self.trace[::-1]):
                _x = point.get("x")
                _y = point.get("y")

                translado_y = 600
                translado_x = 300

                # trace_y.append((translado_y, _y))
                # trace_x.append((_x, translado_x))
                trace.append((_x, _y))

            arc.draw_line_strip(trace[::-1], WHITE)
            # arc.draw_line_strip(trace_y[::-1], WHITE)
            # arc.draw_line_strip(trace_x[::-1], WHITE)

            # arc.draw_line(trace_y[0][0], trace_y[0][1], x, y, YELLOW)
            # arc.draw_line(trace_x[0][0], trace_x[0][1], x, y, GREEN)

        return x, y
