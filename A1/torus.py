from config import Config
import numpy as np
import cmath

from firefly import Firefly

class Torus:
    def __init__(self):
        self.size = Config.TORUS_SIZE
        self.coupling_strength = Config.COUPLING_STRENGTH
        self.fireflies = []
        self.initialize_torus()

    def initialize_torus(self):
        """Erstellt Glühwürmchen und weist Nachbarn zu."""
        for i in range(self.size):
            row = []
            for j in range(self.size):
                natural_frequency = np.random.normal(
                    Config.NATURAL_FREQUENCY_MEAN, Config.NATURAL_FREQUENCY_STD
                )
                firefly = Firefly(
                    id=f"{i}-{j}",
                    natural_frequency=natural_frequency,
                    coupling_strength=self.coupling_strength,
                    neighbors=[]
                )
                row.append(firefly)
            self.fireflies.append(row)

        # Nachbarn zuweisen (Torus-Topologie)
        for i in range(self.size):
            for j in range(self.size):
                neighbors = [
                    self.fireflies[(i-1) % self.size][j],
                    self.fireflies[(i+1) % self.size][j],
                    self.fireflies[i][(j-1) % self.size],
                    self.fireflies[i][(j+1) % self.size],
                ]
                self.fireflies[i][j].neighbors = neighbors

    def start_simulation(self):
        """Startet die Simulation."""
        for row in self.fireflies:
            for firefly in row:
                firefly.start()

    def stop_simulation(self):
        """Stoppt die Simulation."""
        for row in self.fireflies:
            for firefly in row:
                firefly.running = False
                firefly.join()

    def get_phases(self):
        """Erfasst die aktuellen Phasen aller Glühwürmchen."""
        return [[firefly.phase for firefly in row] for row in self.fireflies]

    def compute_sync_degree(self):
        """Berechnet den Synchronisationsgrad r."""
        phases = [firefly.phase for row in self.fireflies for firefly in row]
        N = len(phases)
        complex_order = sum(cmath.exp(1j * phase) for phase in phases) / N
        return abs(complex_order)

    def print_torus_and_sync_degree(self):
        """Druckt die Torus-Anordnung und den Synchronisationsgrad."""
        phases = self.get_phases()
        sync_degree = self.compute_sync_degree()
        print("\nTorus-Zustand:")
        for row in phases:
            print(["{:.2f}".format(phase) for phase in row])
        print(f"Synchronisationsgrad: {sync_degree:.4f}")
