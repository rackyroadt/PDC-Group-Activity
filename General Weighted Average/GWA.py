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
def main():
    print("=" * 50)
    print("      Grade Weighted Average - CLI Edition      ")
    print("         Centralized Computing System           ")
    print("=" * 50)

    # Get number of subjects
    while True:
        try:
            num_input = input("\nEnter number of subjects: ").strip()
            n = int(num_input)
            if n <= 0:
                print("Error: Please enter a valid positive number of subjects.")
                continue
            if n > 8:
                print("Warning: A maximum of 8 subjects is allowed for this layout.")
                n = 8
            break
        except ValueError:
            print("Error: Please enter a valid positive number.")

    grades = []
    units = []