import time
import threading
import queue

# ---------------- SEQUENTIAL ----------------

def consultation():
    time.sleep(2)

def washing():
    time.sleep(3)

def cutting_and_styling():
    time.sleep(10)

def checkout():
    time.sleep(2)

def serve_customer_sequential(customer_id):
    consultation()
    washing()
    cutting_and_styling()
    checkout()

def sequential_barbershop(num_customers):
    start = time.time()
    for i in range(num_customers):
        serve_customer_sequential(i)
    return time.time() - start

# ---------------- PARALLEL (PIPELINE) ----------------

def consultation_worker(input_q, output_q):
    while True:
        customer = input_q.get()
        if customer is None:
            break
        time.sleep(2)
        output_q.put(customer)
        input_q.task_done()

def washing_worker(input_q, output_q):
    while True:
        customer = input_q.get()
        if customer is None:
            break
        time.sleep(3)
        output_q.put(customer)
        input_q.task_done()

def cutting_worker(input_q, output_q):
    while True:
        customer = input_q.get()
        if customer is None:
            break
        time.sleep(10)
        output_q.put(customer)
        input_q.task_done()

def checkout_worker(input_q):
    while True:
        customer = input_q.get()
        if customer is None:
            break
        time.sleep(2)
        input_q.task_done()

def parallel_barbershop(num_customers):
    q1 = queue.Queue()
    q2 = queue.Queue()
    q3 = queue.Queue()
    q4 = queue.Queue()

    threads = [
        threading.Thread(target=consultation_worker, args=(q1, q2)),
        threading.Thread(target=washing_worker, args=(q2, q3)),
        threading.Thread(target=cutting_worker, args=(q3, q4)),
        threading.Thread(target=checkout_worker, args=(q4,))
    ]

    start = time.time()

    for t in threads:
        t.start()

    for i in range(num_customers):
        q1.put(i)

    q1.join()
    q2.join()
    q3.join()
    q4.join()

    for q in (q1, q2, q3, q4):
        q.put(None)

    for t in threads:
        t.join()

    return time.time() - start

# ---------------- BENCHMARK ----------------

if __name__ == "__main__":
    customers = 5

    seq_time = sequential_barbershop(customers)
    par_time = parallel_barbershop(customers)
    speedup = seq_time / par_time

    print("\n--- Benchmark Results ---")
    print(f"Sequential Time: {seq_time:.2f} seconds")
    print(f"Parallel Time:   {par_time:.2f} seconds")
    print(f"Speedup:         {speedup:.2f}x")