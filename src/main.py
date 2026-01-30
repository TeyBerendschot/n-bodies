from itertools import combinations

import numpy as np
import pygame
from pygame.time import Clock
from pygame.draw import circle

from bodies import Body

# Gravitational constant
G = 1e-4


class NBodySimulation:
    def __init__(
        self,
        bodies: list[Body],
        fps: int = 60,
    ):
        self.bodies = bodies

        # Initialize simulation attributes
        pygame.init()
        self.surface = pygame.display.set_mode((800, 800))
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

        total_momentum = np.sum(
            [b.mass * np.array([b.vx, b.vy]) for b in self.bodies], axis=0
        )

        for b in self.bodies:
            b.x += translate_vector[0]
            b.y += translate_vector[1]

            b.vx -= total_momentum[0] / total_mass
            b.vy -= total_momentum[1] / total_mass

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
            r = np.array([b2.x - b1.x, b2.y - b1.y])

            # The force that is applies to the bodies is proportional to mM/r^2
            v = G * r / np.linalg.norm(r, ord=3)

            b1.update_velocity(by=v * b2.mass)
            b2.update_velocity(by=-v * b1.mass)

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
            body.update_position()

        self.draw_center_of_mass()

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
            radius=10,
            p=(0, -20),
        ),
        Body(
            q=(150, 0),
            radius=30,
            p=(-20, 20),
        ),
        Body(
            q=(150, 200),
            radius=25,
            p=(0, 20),
        ),
    ]
    simulation = NBodySimulation(bodies=bodies, fps=30)

    simulation.run()
