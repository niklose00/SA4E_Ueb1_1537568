import grpc
import tkinter as tk
import cmath
from concurrent.futures import ThreadPoolExecutor
from firefly_pb2 import PhaseRequest
from firefly_pb2_grpc import FireflyServiceStub
from config import Config


class Observer:
    def __init__(self, size, addresses):
        self.size = size 
        self.addresses = addresses  
        self.phases = [[0 for _ in range(size)] for _ in range(size)] 
        self.root = tk.Tk()
        self.root.title("Observer - Glühwürmchen-Zustände")

        # Canvas für die Torus-Darstellung
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        # Label für den Synchronisationsgrad
        self.sync_label = tk.Label(self.root, text="Synchronisationsgrad: 0.0000")
        self.sync_label.pack()

        # Rechtecke für die Visualisierung erstellen
        self.rects = self.create_rects()

    def create_rects(self):
        """Erstellt Rechtecke für die Visualisierung."""
        rects = []
        rect_size = 500 // self.size
        for i in range(self.size):
            row = []
            for j in range(self.size):
                rect = self.canvas.create_rectangle(
                    j * rect_size, i * rect_size,
                    (j + 1) * rect_size, (i + 1) * rect_size,
                    fill="black"
                )
                row.append(rect)
            rects.append(row)
        return rects

    def update_phases(self):
        """Kommuniziert mit allen Glühwürmchen und aktualisiert die Phasen."""
        with ThreadPoolExecutor(max_workers=len(self.addresses)) as executor:
            futures = [
                executor.submit(self.get_phase, i, j, address)
                for i, row in enumerate(self.addresses)
                for j, address in enumerate(row)
            ]
            for future in futures:
                future.result()  

        self.update_canvas()  
        self.update_sync_label()  
        self.root.after(Config.UI_UPDATE_INTERVAL, self.update_phases) 

    def get_phase(self, i, j, address):
        """Ruft die Phase eines Glühwürmchens ab."""
        with grpc.insecure_channel(address) as channel:
            stub = FireflyServiceStub(channel)
            try:
                response = stub.GetPhase(PhaseRequest(id=i * self.size + j))
                self.phases[i][j] = response.phase
            except grpc.RpcError:
                print(f"Observer: Failed to connect to Firefly at {address}")

    def update_canvas(self):
        """Aktualisiert die GUI-Darstellung basierend auf den Phasen."""
        for i, row in enumerate(self.rects):
            for j, rect in enumerate(row):
                phase = self.phases[i][j]
                # Gelb, wenn die Phase nahe bei 0 oder dem Limit ist
                limit = Config.PHASE_UPPER_LIMIT / 2
                if 0 <= phase < limit / 2 or 3 * limit / 2 <= phase <= 2 * limit:
                    color = "yellow"
                else:
                    color = "black"
                self.canvas.itemconfig(rect, fill=color)

    def compute_sync_degree(self):
        """Berechnet den Synchronisationsgrad."""
        flat_phases = [phase for row in self.phases for phase in row]
        N = len(flat_phases)
        complex_order = sum(cmath.exp(1j * phase) for phase in flat_phases) / N
        return abs(complex_order)

    def update_sync_label(self):
        """Aktualisiert den Synchronisationsgrad im Fenster."""
        sync_degree = self.compute_sync_degree()
        self.sync_label.config(text=f"Synchronisationsgrad: {sync_degree:.4f}")

    def run(self):
        """Startet die GUI."""
        self.update_phases() 
        self.root.mainloop()
