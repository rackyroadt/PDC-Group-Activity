import threading
import time
from concurrent.futures import ThreadPoolExecutor

class GWATask:
    def __init__(self, g, u):
        self.grades = g
        self.units = u
        self.weighted_sum = 0
        self.total_units = 0
        self.lock = threading.Lock()

    def compute(self, index):
        product = self.grades[index] * self.units[index]
        with self.lock:
            self.weighted_sum += product
            self.total_units += self.units[index]
