import threading
import time

grades = [1.25, 1.50, 2.00, 1.75, 1.25]
units  = [3, 3, 4, 3, 2]

weighted_sum = 0
total_units = 0
lock = threading.Lock()

def compute(index):
    global weighted_sum, total_units
    with lock:
        weighted_sum += grades[index] * units[index]
        total_units += units[index]

start = time.time()

threads = []
for i in range(len(grades)):
    t = threading.Thread(target=compute, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

gwa = weighted_sum / total_units
end = time.time()

print("Multithreading GWA:", gwa)
print("Execution Time:", end - start)