import time
from contextlib import contextmanager

@contextmanager
def timing(label="Execution"):
    start = time.time()
    yield
    end = time.time()
    print(f"[{label}] took {end - start:.3f} seconds")