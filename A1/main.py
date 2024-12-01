import numpy as np
import tkinter as tk
from config import Config
from torus import Torus


def visualize_torus(torus):
    """Visualisiert die Torus-Anordnung, zeigt den Synchronisationsgrad an und loggt diesen."""
    root = tk.Tk()
    root.title("Synchronisation der Glühwürmchen")

    # Canvas für die Glühwürmchen
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()

    # Label für den Synchronisationsgrad
    sync_label = tk.Label(root, text="Synchronisationsgrad: 0.0000")
    sync_label.pack()

    size = Config.TORUS_SIZE
    rect_size = 500 // size

    # Rechtecke für die Glühwürmchen erstellen
    rects = []
    for i in range(size):
        row = []
        for j in range(size):
            rect = canvas.create_rectangle(
                j * rect_size, i * rect_size,
                (j + 1) * rect_size, (i + 1) * rect_size,
                fill="black"
            )
            row.append(rect)
        rects.append(row)

    def update_canvas():
        """Aktualisiert die Farben basierend auf den Phasen (Gelb und Schwarz)."""
        phases = torus.get_phases()
        for i, row in enumerate(rects):
            for j, rect in enumerate(row):
                phase = phases[i][j]
                # Gelb, wenn die Phase nahe bei 0 oder dem Limit ist
                limit = Config.PHASE_UPPER_LIMIT / 2
                if 0 <= phase < limit / 2 or 3 * limit / 2 <= phase <= 2 * limit:
                    color = "yellow"
                else:
                    color = "black"
                canvas.itemconfig(rect, fill=color)
        root.after(Config.UI_UPDATE_INTERVAL, update_canvas)

    def update_sync_label():
        """Aktualisiert den Synchronisationsgrad im Label."""
        sync_degree = torus.compute_sync_degree()
        sync_label.config(text=f"Synchronisationsgrad: {sync_degree:.4f}")
        root.after(Config.CONSOLE_LOG_INTERVAL, update_sync_label)

    def log_sync():
        """Loggt den Synchronisationsgrad und den Torus-Zustand in die Konsole."""
        torus.print_torus_and_sync_degree()
        root.after(Config.CONSOLE_LOG_INTERVAL, log_sync)

    # Initiale Updates starten
    root.after(Config.UI_UPDATE_INTERVAL, update_canvas)
    root.after(Config.CONSOLE_LOG_INTERVAL, update_sync_label)
    root.after(Config.CONSOLE_LOG_INTERVAL, log_sync)

    # Hauptloop der GUI starten
    root.mainloop()


def main():
    """Startet die Simulation der synchronisierenden Glühwürmchen."""
    try:
        print("Starte Simulation...")
        torus = Torus()
        torus.start_simulation()
        visualize_torus(torus)
    except KeyboardInterrupt:
        print("Simulation wird gestoppt...")
    finally:
        torus.stop_simulation()
        print("Simulation beendet.")

if __name__ == "__main__":
    main()
