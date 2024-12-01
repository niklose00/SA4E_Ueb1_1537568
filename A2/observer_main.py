from config import Config
from obverser import Observer


if __name__ == "__main__":
    size = Config.TORUS_SIZE
    addresses = [[f"localhost:{Config.BASE_PORT + i * size + j}" for j in range(size)] for i in range(size)]

    observer = Observer(size=size, addresses=addresses)
    observer.run()
