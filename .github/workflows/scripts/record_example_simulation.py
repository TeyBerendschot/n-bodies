from bodies import Body
from simulation import NBodySimulation
from record import PygameRecord

FPS = 60
N_FRAMES = 90

with PygameRecord("./.github/gifs/output.gif", FPS, n_frames=90) as recorder:
    bodies = [
        Body(
            q=(0, 0),
            radius=20,
            p=(0, -45),
        ),
        Body(
            q=(300, 0),
            radius=30,
            p=(-10, -10),
        ),
        Body(
            q=(300, 400),
            radius=25,
            p=(10, 0),
        ),
    ]

    simulation = NBodySimulation(bodies=bodies, fps=FPS, recorder=recorder)
    simulation.run()
