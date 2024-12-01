from multiprocessing import Process
import time

import numpy as np
from config import Config
from firefly import Firefly



def start_firefly(id, port, neighbors):
    """Startet ein Glühwürmchen als unabhängigen Prozess."""
    natural_frequency = np.random.normal(Config.NATURAL_FREQUENCY_MEAN, Config.NATURAL_FREQUENCY_STD)
    coupling_strength = Config.COUPLING_STRENGTH
    firefly = Firefly(id=id, port=port, neighbors=neighbors, natural_frequency=natural_frequency, coupling_strength=coupling_strength)
    firefly.run()

def generate_neighbors(id, size):
    """Generiert die Adressen der Nachbarn im Torus."""
    row, col = divmod(id, size)
    neighbors = [
        ((row - 1) % size) * size + col,
        ((row + 1) % size) * size + col,
        row * size + (col - 1) % size,
        row * size + (col + 1) % size
    ]
    return [f"localhost:{Config.BASE_PORT + n}" for n in neighbors]

def main():
    size = Config.TORUS_SIZE
    processes = []
    time.sleep(5)

    for id in range(size * size):
        port = Config.BASE_PORT + id
        neighbors = generate_neighbors(id, size)
        process = Process(target=start_firefly, args=(id, port, neighbors))
        processes.append(process)
        process.start()

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print("Simulation beendet.")

if __name__ == "__main__":
    main()
