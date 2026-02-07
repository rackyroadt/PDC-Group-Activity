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

# Subject Data

n = int(input("How many subjects do you have? "))
print("\nPlease enter details for each subject:")
for i in range(n):
        print(f"\n--- Subject {i+1} ---")
        name = input(f"Subject Name (default 'Subject {i+1}'): ").strip()
        if not name:
            name = f"Subject {i+1}"

        while True:
            try:
                g_str = input(f"Grade (1.0-5.0) for '{name}': ").strip()
                grade = float(g_str)
                if 1.0 <= grade <= 5.0:
                    grade.append(grade)
                    break
                else:
                    print(f"Error: Grade for '{name}' must be between 1.0 and 5.0.")
            except ValueError:
                print("Error: Make sure grades are numbers.")

        while True:
            try:
                u_str = input(f"Units (1-4) for '{name}': ").strip()
                unit = int(u_str)
                if 1 <= unit <= 4:
                    unit.append(unit)
                    break
                else:
                    print(f"Error: Units for '{name}' must be between 1 and 4.")
            except ValueError:
                print("Error: Make sure units are integers.")

        task = GWATask(grades, units)
    start = time.perf_counter()

    with ThreadPoolExecutor() as executor:
        for i in range(len(grades)):
            executor.submit(task.compute, i)

    if task.total_units == 0:
        print("\nError: Total units cannot be zero.")
        return

    gwa = task.weighted_sum / task.total_units
    end = time.perf_counter()

    # Results display
    print("\n" + "=" * 50)
    print(f"Final GWA: {gwa:.3f}")
    print(f"Computed in {end - start:.6f} seconds (Multithreaded)")
    print("=" * 50)

if name == "main":
    main()
