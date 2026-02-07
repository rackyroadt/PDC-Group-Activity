import threading
import time
from multiprocessing import Process, Queue

thread_results = []
thread_lock = threading.Lock()

def compute_gwa_thread(subject_name, grade, thread_id):
    time.sleep(0.01)
    with thread_lock:
        thread_results.append({
            'subject': subject_name,
            'grade': grade,
            'id': thread_id
        })
        print(f"[Thread {thread_id}] {subject_name}: {grade}")

def run_multithreading(subjects, grades):
    global thread_results
    thread_results = []
    
    print("\n" + "=" * 70)
    print("PROCESSING WITH MULTITHREADING...")
    print("=" * 70)
    
    start_time = time.time()
    
    threads = []
    for i, (subject, grade) in enumerate(zip(subjects, grades)):
        t = threading.Thread(
            target=compute_gwa_thread,
            args=(subject, grade, i+1)
        )
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    gwa = sum(grades) / len(grades) if grades else 0
    
    return execution_time, gwa, thread_results

def compute_gwa_process(subject_name, grade, process_id, result_queue):
    time.sleep(0.01)
    result_queue.put({
        'subject': subject_name,
        'grade': grade,
        'id': process_id
    })
    print(f"[Process {process_id}] {subject_name}: {grade}")

def run_multiprocessing(subjects, grades):
    result_queue = Queue()
    
    print("\n" + "=" * 70)
    print("PROCESSING WITH MULTIPROCESSING...")
    print("=" * 70)
    
    start_time = time.time()
    
    processes = []
    for i, (subject, grade) in enumerate(zip(subjects, grades)):
        p = Process(
            target=compute_gwa_process,
            args=(subject, grade, i+1, result_queue)
        )
        processes.append(p)
        p.start()
    
    # Collect results from queue before join to avoid potential deadlocks if queue is full
    # though for small data it's usually fine.
    process_results = []
    for _ in range(len(subjects)):
        process_results.append(result_queue.get())
        
    for p in processes:
        p.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    gwa = sum(grades) / len(grades) if grades else 0
    
    return execution_time, gwa, process_results

def main():
    print("=" * 70)
    print(" GRADE COMPUTING SYSTEM")
    print(" Multithreading vs Multiprocessing Comparison")
    print("=" * 70)
    
    while True:
        try:
            num_subjects = int(input("\nEnter number of subjects: "))
            if num_subjects < 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    subjects = []
    grades = []
    
    print("\nEnter subject names and grades:")
    for i in range(num_subjects):
        while True:
            subject = input(f"Subject {i+1} name: ").strip()
            if subject:
                break
            print("Subject name cannot be empty. Please enter a valid name.")
            
        while True:
            try:
                grade = float(input(f"Grade for {subject}: "))
                break
            except ValueError:
                print("Invalid input. Please enter a numerical grade.")
        subjects.append(subject)
        grades.append(grade)
    
    print(f"\n[TEST 1] MULTITHREADING")
    thread_time, thread_gwa, thread_res = run_multithreading(subjects, grades)
    print(f"Completed in {thread_time:.6f} seconds")
    
    print(f"\n[TEST 2] MULTIPROCESSING")
    process_time, process_gwa, process_res = run_multiprocessing(subjects, grades)
    print(f"Completed in {process_time:.6f} seconds")
    
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON TABLE")
    print("=" * 70)
    print(f"{'Method':<20} {'Execution Time':<20} {'GWA':<15} {'Status'}")
    print("-" * 70)
    print(f"{'Multithreading':<20} {f'{thread_time:.6f} seconds':<20} {thread_gwa:<15.2f} {'Complete'}")
    print(f"{'Multiprocessing':<20} {f'{process_time:.6f} seconds':<20} {process_gwa:<15.2f} {'Complete'}")
    print("=" * 70)
    
    print("\nANALYSIS:")
    print("-" * 70)
    
    if thread_time < process_time:
        faster = "Multithreading"
        diff = process_time - thread_time
        percent = ((process_time - thread_time) / process_time) * 100
    else:
        faster = "Multiprocessing"
        diff = thread_time - process_time
        percent = ((thread_time - process_time) / thread_time) * 100
    
    print(f"Faster method: {faster}")
    print(f"Time difference: {diff:.6f} seconds ({percent:.2f}% faster)")
    print(f"Number of subjects processed: {num_subjects}")
    print(f"Both methods calculated GWA: {thread_gwa:.2f}")
    
    print("\nNOTES:")
    print("Execution order may vary between runs due to concurrent execution")
    print("Multiprocessing has overhead from creating separate processes")
    print("For CPU-intensive tasks, multiprocessing utilizes multiple cores")
    print("For I/O-bound or lightweight tasks, multithreading is more efficient")
    print("=" * 70)

if __name__ == "__main__":
    main()
