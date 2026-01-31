from bodies import Body
from simulation import NBodySimulation
from record import PygameRecord

FPS = 40
N_FRAMES = 1000

with PygameRecord("./.github/gifs/output.gif", FPS, n_frames=N_FRAMES) as recorder:
    bodies = [
        Body(q=(0, 0), radius=20, p=(0, -45), color=(149, 219, 50)),
        Body(q=(300, 0), radius=30, p=(-10, -10), color=(219, 56, 1)),
        Body(q=(300, 400), radius=25, p=(10, 0), color=(50, 142, 86)),
    ]

    simulation = NBodySimulation(bodies=bodies, fps=FPS, recorder=recorder)
    simulation.run()
