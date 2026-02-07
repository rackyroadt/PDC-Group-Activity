import threading
import time
from multiprocessing import Process, Queue

thread_results = []
thread_lock = threading.Lock()

def compute_gwa_thread(subject_name, grade, thread_id):
    time.sleep(0.01)
    with thread_lock:
        thread_results.append({'subject': subject_name, 'grade': grade})
        print("[Thread {}] {}: {}".format(thread_id, subject_name, grade))

def compute_gwa_process(subject_name, grade, process_id, result_queue):
    time.sleep(0.01)
    result_queue.put({'subject': subject_name, 'grade': grade})
    print("[Process {}] {}: {}".format(process_id, subject_name, grade))

def run_multithreading(subjects, grades):
    global thread_results
    thread_results = []
    start_time = time.time()
    threads = []
    for i, (subject, grade) in enumerate(zip(subjects, grades)):
        t = threading.Thread(target=compute_gwa_thread, args=(subject, grade, i+1))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return time.time() - start_time, sum(grades) / len(grades)

def run_multiprocessing(subjects, grades):
    result_queue = Queue()
    start_time = time.time()
    processes = []
    for i, (subject, grade) in enumerate(zip(subjects, grades)):
        p = Process(target=compute_gwa_process, args=(subject, grade, i+1, result_queue))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    return time.time() - start_time, sum(grades) / len(grades)

def main():
    print("COMPARISON VERSION")
    num_subjects = int(input("Enter number of subjects: "))
    subjects = []
    grades = []
    for i in range(num_subjects):
        subject = input("Subject {} name: ".format(i+1))
        grade = float(input("Grade for {}: ".format(subject)))
        subjects.append(subject)
        grades.append(grade)
    
    print("\nTesting Multithreading...")
    thread_time, thread_gwa = run_multithreading(subjects, grades)
    
    print("\nTesting Multiprocessing...")
    process_time, process_gwa = run_multiprocessing(subjects, grades)
    
    print("\n" + "="*50)
    print("RESULTS")
    print("="*50)
    print("Multithreading: {:.6f} seconds | GWA: {:.2f}".format(thread_time, thread_gwa))
    print("Multiprocessing: {:.6f} seconds | GWA: {:.2f}".format(process_time, process_gwa))

if _name_ == "_main_":
    main()