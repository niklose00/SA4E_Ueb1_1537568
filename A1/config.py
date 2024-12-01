import numpy as np


class Config:
    """Zentrale Konfiguration für die Simulation."""
    TORUS_SIZE = 10  # Größe des Torus
    COUPLING_STRENGTH = 1  # Kopplungsstärke K
    NATURAL_FREQUENCY_MEAN = 1  # Mittelwert der natürlichen Frequenz wi
    NATURAL_FREQUENCY_STD = 0.2  # Standardabweichung der natürlichen Frequenz wi
    TIME_STEP = 0.2  # Zeitschritt für die Simulation
    UI_UPDATE_INTERVAL = 100  # Intervall für UI-Aktualisierung in Millisekunden
    CONSOLE_LOG_INTERVAL = 1000  # Intervall für Konsolen-Log in Millisekunden
    PHASE_UPPER_LIMIT = 2 * np.pi # Maximaler Wert einer Phase Delta