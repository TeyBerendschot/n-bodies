from itertools import combinations

import numpy as np
import pygame
from pygame.time import Clock
from pygame.draw import circle

from bodies import Body
from record import PygameRecord

# Gravitational constant
G = 1e-4

# Window size
WIDTH = 1000
HEIGHT = 1000


class NBodySimulation:
    def __init__(
        self,
        bodies: list[Body],
        fps: int = 60,
        title: str = "0-body simulation",
        width: int = WIDTH,
        height: int = HEIGHT,
        recorder: PygameRecord | None = None,
    ):
        self.bodies = bodies
        self.recorder = recorder

        # Initialize simulation attributes
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.fps = fps
        self.clock = Clock()

        # Place the center of mass of the system in the middle of the canvas
        if self.bodies:
            self._normalize_system()

        # Used to check for mouse drag
        self.mouse_click_start = None
        self.line = None

    def _render_explanation(self):
        my_font = pygame.font.SysFont("Comic Sans MS", 30)
        text_surface_drag = my_font.render(
            "Drag mouse to add bodies to the problem.", False, (0, 0, 0)
        )
        text_surface_normalize = my_font.render(
            "Press space bar to put the center of mass at the center of window.",
            False,
            (0, 0, 0),
        )

        self.surface.blit(text_surface_drag, (4, 4))
        self.surface.blit(text_surface_normalize, (4, 30))

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

    def _normalize_system(self) -> None:
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

            if event.type == pygame.KEYDOWN:
                # Normalize the system when pressing the space bar
                if event.key == 32:
                    self._normalize_system()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_click_start = event.pos
                self.line = [event.pos, event.pos]

            if self.mouse_click_start and event.type == pygame.MOUSEMOTION:
                self.line[1] = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                self._add_body()
                self.mouse_click_start = None
                self.line = None

    def _get_radius_from_line(self):
        return np.sqrt(np.linalg.norm(np.array(self.line[1]) - np.array(self.line[0])))

    def _add_body(self):
        """Add a new body to the system based on user input."""
        body = Body(
            q=self.line[0],
            radius=self._get_radius_from_line(),
            p=tuple((np.array(self.line[1]) - np.array(self.line[0])) / 20),
        )

        self.bodies.append(body)

        pygame.display.set_caption(f"{len(self.bodies)}-body simulation")

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

    def _draw_line(self):
        pygame.draw.line(self.surface, (0, 255, 0), self.line[0], self.line[1], width=4)

        # Draw a circle of which the size is proportional to the length of the line
        circle(
            self.surface,
            (100, 100, 100),
            center=self.line[0],
            radius=self._get_radius_from_line(),
        )

    def update(self):
        # Start with a fresh canvas each frame
        self.surface.fill((255, 255, 255))

        # Handle any events
        self.handle_events()

        # Update the velocities of the bodies
        self.update_velocities()

        # Draw circles
        for body in self.bodies:
            self.draw_body(body=body)
            body.update_position()

        # Draw line if mouse is down
        if self.line:
            self._draw_line()

        # Render the explanation
        self._render_explanation()

        pygame.display.update()
        self.clock.tick(self.fps)

    def run(self):
        """Run the simulation"""
        while True:
            # Record the frame
            if self.recorder:
                self.recorder.add_frame()
                self.recorder.n_frames -= 1
                print(self.recorder.n_frames)
                if self.recorder.n_frames == 0:
                    self.recorder.save()
                    pygame.quit()
                    return

            self.update()
