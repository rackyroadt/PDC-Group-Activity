import threading
import queue
import time
import random

NUM_CUSTOMERS = 12
RANDOM_SEED   = 42
random.seed(RANDOM_SEED)

STAGE_DURATIONS = {
    "Consultation" : 0.10,
    "Washing"      : 0.25,
    "Cutting"      : 0.75,
    "Styling"      : 0.10,
    "Checkout"     : 0.05,
}

barber_chair_lock = threading.Lock()
done_count        = 0
done_lock         = threading.Lock()
print_lock        = threading.Lock()

def log(msg):
    with print_lock:
        print(msg)

def do_stage(stage_name):
    base   = STAGE_DURATIONS[stage_name]
    jitter = random.uniform(0.85, 1.15)
    time.sleep(base * jitter)

SENTINEL = None