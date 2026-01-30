class Body:
    def __init__(
        self,
        q: tuple[float, float],
        radius: float,
        mass: float | None = None,
        p: tuple[float, float] = (0.0, 0.0),
    ):
        self.x = q[0]
        self.y = q[1]
        if mass is None:
            mass = radius**3

        self.mass: float = mass
        self.r = radius
        self.vx = p[0]
        self.vy = p[1]

    def update_velocity(self, by: tuple[float, float] = (0.0, 0.0)) -> None:
        self.vx += by[0]
        self.vy += by[1]

    def update_position(self) -> None:
        self.x += self.vx
        self.y += self.vy
