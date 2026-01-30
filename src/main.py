from itertools import combinations

import numpy as np
import pygame
from pygame.time import Clock
from pygame.draw import circle

from bodies import Body


class NBodySimulation:
    def __init__(
        self,
        bodies: list[Body],
        fps: int = 60,
    ):
        self.bodies = bodies

        # Initialize simulation attributes
        pygame.init()
        self.surface = pygame.display.set_mode((600, 600))
        self.fps = fps
        self.clock = Clock()

        # Place the center of mass of the system in the middle of the canvas
        self.move_center_of_mass_to_display_center()

    def draw_center_of_mass(self):
        total_mass = sum(b.mass for b in self.bodies)
        center_of_mass = (
            np.sum([b.mass * np.array([b.x, b.y]) for b in self.bodies], axis=0)
            / total_mass
        )
        circle(
            surface=self.surface,
            color=(255, 255, 0),
            center=tuple(center_of_mass),
            radius=10,
        )

    def move_center_of_mass_to_display_center(self) -> None:
        """Calculate the center of mass and put it in the center of the display surface.

        Also calculates the velocity relative to the surface and subtracts this from each body"""
        total_mass = sum(b.mass for b in self.bodies)
        center_of_mass = (
            np.sum([b.mass * np.array([b.x, b.y]) for b in self.bodies], axis=0)
            / total_mass
        )
        surface_center = np.array(self.surface.get_size()) / 2

        translate_vector = surface_center - center_of_mass

        total_momentum = np.sum([np.array([b.vx, b.vy]) for b in self.bodies], axis=0)

        for b in self.bodies:
            b.x += translate_vector[0]
            b.y += translate_vector[1]

            b.vx -= total_momentum[0] / len(self.bodies)
            b.vy -= total_momentum[1] / len(self.bodies)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def draw_body(self, body: Body):
        circle(
            surface=self.surface,
            color=(0, 0, 0),
            center=(body.x, body.y),
            radius=body.r,
        )

    def update_velocities(self) -> None:
        # Calculate forces that act on the bodies
        for b1, b2 in combinations(self.bodies, 2):
            v = np.array([b2.x - b1.x, b2.y - b1.y])

            # The force that is applies to the bodies is proportional to mM/r^2
            v = b1.mass * b2.mass * v / np.linalg.norm(v)

            b1.update_velocity(by=v)
            b2.update_velocity(by=-v)

    def update(self):
        # Handle any events
        self.handle_events()

        # Start with a fresh canvas each frame
        self.surface.fill((255, 255, 255))

        # Update the velocities of the bodies
        self.update_velocities()

        # Draw circles
        for body in self.bodies:
            self.draw_body(body=body)
            self.draw_center_of_mass()
            body.update_position()

        pygame.display.update()
        self.clock.tick(self.fps)

    def run(self):
        """Run the simulation"""
        while True:
            self.update()


if __name__ == "__main__":
    bodies = [
        Body(
            q=(0, 0),
            radius=20,
            p=(0, 4),
        ),
        Body(
            q=(300, 0),
            radius=30,
            p=(0, -4),
        ),
        Body(
            q=(300, 400),
            radius=25,
            p=(0, -4),
        ),
    ]
    simulation = NBodySimulation(bodies=bodies, fps=40)

    simulation.run()
