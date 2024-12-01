import grpc
import threading
import time
import random
from concurrent import futures
from config import Config

import numpy as np
from config import Config
from firefly_pb2 import PhaseResponse, PhaseRequest, PhaseUpdate, Empty
from firefly_pb2_grpc import FireflyServiceServicer, FireflyServiceStub, add_FireflyServiceServicer_to_server

class Firefly(FireflyServiceServicer):
    def __init__(self, id, port, neighbors, natural_frequency, coupling_strength):
        self.id = id
        self.port = port
        self.neighbors = neighbors
        self.phase = random.uniform(0, Config.PHASE_UPPER_LIMIT) 
        self.natural_frequency = natural_frequency
        self.coupling_strength = coupling_strength
        self.running = True
        self.lock = threading.Lock() 

    def GetPhase(self, request, context):
        """gRPC-Methode: Phase abrufen."""
        with self.lock:
            return PhaseResponse(phase=self.phase)

    def UpdatePhase(self, request, context):
        """gRPC-Methode: Phase aktualisieren."""
        with self.lock:
            previous_phase = self.phase
            self.phase += self.coupling_strength * (request.newPhase - self.phase)
            self.phase %= Config.PHASE_UPPER_LIMIT
            print(f"[Firefly {self.id}] Updated Phase: {previous_phase:.4f} -> {self.phase:.4f}")
        return Empty()

    def run_server(self):
        """Startet den gRPC-Server."""
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_FireflyServiceServicer_to_server(self, server)
        server.add_insecure_port(f'[::]:{self.port}')
        server.start()
        print(f"[Firefly {self.id}] Running on port {self.port}")
        server.wait_for_termination()

    def communicate_with_neighbors(self):
        """Kommuniziert regelmäßig mit den Nachbarn."""
        while self.running:
            neighbor_phases = [] 
            
            # Phasen von Nachbarn abrufen
            for neighbor in self.neighbors:
                with grpc.insecure_channel(neighbor) as channel:
                    stub = FireflyServiceStub(channel)
                    try:
                        response = stub.GetPhase(PhaseRequest(id=self.id))
                        neighbor_phases.append(response.phase) 
                        print(f"[Firefly {self.id}] Neighbor {neighbor} Phase: {response.phase:.4f}")
                    except grpc.RpcError:
                        print(f"[Firefly {self.id}] Connection failed to neighbor {neighbor}")

            # Nach Kuramoto-Modell Phase berechnen
            with self.lock:
                previous_phase = self.phase
                total_influence = sum(
                    self.coupling_strength * (np.sin(neighbor_phase - self.phase))
                    for neighbor_phase in neighbor_phases
                )
                self.phase += self.natural_frequency * Config.TIME_STEP + total_influence * Config.TIME_STEP
                self.phase %= Config.PHASE_UPPER_LIMIT
                print(f"[Firefly {self.id}] Updated Phase: {previous_phase:.4f} -> {self.phase:.4f}")

            time.sleep(Config.TIME_STEP)

    def run(self):
        """Startet den Server und die Nachbarskommunikation."""
        threading.Thread(target=self.communicate_with_neighbors, daemon=True).start()
        self.run_server()
