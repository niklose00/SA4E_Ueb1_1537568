import numpy as np


class Config:
    """Zentrale Konfiguration für die Simulation."""
    TORUS_SIZE = 8  # Größe des Torus
    COUPLING_STRENGTH = 1  # Kopplungsstärke
    NATURAL_FREQUENCY_MEAN = 1  # Mittelwert der natürlichen Frequenz
    NATURAL_FREQUENCY_STD = 0.1  # Standardabweichung der natürlichen Frequenz
    TIME_STEP = 0.1  # Zeitschritt für die Simulation
    UI_UPDATE_INTERVAL = 100  # Intervall für UI-Aktualisierung in Millisekunden
    CONSOLE_LOG_INTERVAL = 1000  # Intervall für Konsolen-Log in Millisekunden
    BASE_PORT = 5000 # Basisport für gRPC-Kommunikation; individuelle Ports der Glühwürmchen werden darauf aufbauend generiert
    PHASE_UPPER_LIMIT = 2 * np.pi # Maximaler Wert einer Phase Delta