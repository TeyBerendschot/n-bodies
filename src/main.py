from simulation import NBodySimulation


def main():
    # Start with an empty simulation
    simulation = NBodySimulation(bodies=[], fps=50)

    simulation.run()


if __name__ == "__main__":
    main()
