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
        print("[Thread {}] {}: {}".format(thread_id, subject_name, grade))

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
    print("[Process {}] {}: {}".format(process_id, subject_name, grade))

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
    
    for p in processes:
        p.join()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    process_results = []
    while not result_queue.empty():
        process_results.append(result_queue.get())
    
    gwa = sum(grades) / len(grades) if grades else 0
    
    return execution_time, gwa, process_results

def main():
    print("=" * 70)
    print(" GRADE COMPUTING SYSTEM")
    print(" Multithreading vs Multiprocessing Comparison")
    print("=" * 70)
    
    num_subjects = int(input("\nEnter number of subjects: "))
    
    subjects = []
    grades = []
    
    print("\nEnter subject names and grades:")
    for i in range(num_subjects):
        subject = input("Subject {} name: ".format(i+1))
        grade = float(input("Grade for {}: ".format(subject)))
        subjects.append(subject)
        grades.append(grade)
    
    print("\n[TEST 1] MULTITHREADING")
    thread_time, thread_gwa, thread_res = run_multithreading(subjects, grades)
    print("Completed in {:.6f} seconds".format(thread_time))
    
    print("\n[TEST 2] MULTIPROCESSING")
    process_time, process_gwa, process_res = run_multiprocessing(subjects, grades)
    print("Completed in {:.6f} seconds".format(process_time))
    
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON TABLE")
    print("=" * 70)
    print("{:<20} {:<20} {:<15} {}".format('Method', 'Execution Time', 'GWA', 'Status'))
    print("-" * 70)
    print("{:<20} {:<20} {:<15.2f} {}".format('Multithreading', '{:.6f} seconds'.format(thread_time), thread_gwa, 'Complete'))
    print("{:<20} {:<20} {:<15.2f} {}".format('Multiprocessing', '{:.6f} seconds'.format(process_time), process_gwa, 'Complete'))
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
    
    print("Faster method: {}".format(faster))
    print("Time difference: {:.6f} seconds ({:.2f}% faster)".format(diff, percent))
    print("Number of subjects processed: {}".format(num_subjects))
    print("Both methods calculated GWA: {:.2f}".format(thread_gwa))
    
    print("\nNOTES:")
    print("Execution order may vary between runs due to concurrent execution")
    print("Multiprocessing has overhead from creating separate processes")
    print("For CPU-intensive tasks, multiprocessing utilizes multiple cores")
    print("For I/O-bound or lightweight tasks, multithreading is more efficient")
    print("=" * 70)

if _name_ == "_main_":
    main()
