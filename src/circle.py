import arcade as arc
from arcade.color import WHITE, YELLOW
from numpy import cos, sin


class Circle:
    def __init__(self, angle=0, radius=1) -> None:
        self.angle = angle
        self.radius = radius
        self.trace = []

    def update(self, unit_angle=0.02):
        self.angle += unit_angle

    def draw(self, center={"x": 0, "y": 0}, is_last=False, angle=1):
        x = self.radius * cos(angle * self.angle) + center.get("x")
        y = self.radius * sin(angle * self.angle) + center.get("y")

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
            for index, point in enumerate(self.trace[::-1]):
                trace.append((600 - (self.radius + index), point.get("y")))

            arc.draw_line_strip(trace[::-1], WHITE)

            arc.draw_line(trace[0][0], trace[0][1], x, y, YELLOW)

        return x, y
