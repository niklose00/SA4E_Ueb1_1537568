import numpy as np
import threading
import tkinter as tk
import time

from config import Config

class Firefly(threading.Thread):
    def __init__(self, id, natural_frequency, coupling_strength, neighbors):
        super().__init__()
        self.id = id
        self.phase = np.random.uniform(0, Config.PHASE_UPPER_LIMIT)
        self.natural_frequency = natural_frequency
        self.coupling_strength = coupling_strength
        self.neighbors = neighbors
        self.running = True

    def influence(self):
        """Berechnet den Einfluss der Nachbarn."""
        return sum(np.sin(neighbor.phase - self.phase) for neighbor in self.neighbors)

    def update_phase(self, dt):
        """Aktualisiert die Phase gemäß Kuramoto-Modell."""
        self.phase += self.natural_frequency * dt + self.coupling_strength * self.influence() * dt
        self.phase %= Config.PHASE_UPPER_LIMIT

    def run(self):
        """Thread-Logik."""
        while self.running:
            self.update_phase(Config.TIME_STEP)
            time.sleep(Config.TIME_STEP)
