import threading
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# ==============================
# PART A — TASK PARALLELISM
# ==============================



# --- Individual Deduction Functions ---

def compute_sss(salary):
    thread_name = threading.current_thread().name
    sss = salary * 0.05
    print(f"[{thread_name}] SSS Deduction: {sss:.2f}")
    return sss


def compute_philhealth(salary):
    thread_name = threading.current_thread().name
    philhealth = salary * 0.04
    print(f"[{thread_name}] PhilHealth Deduction: {philhealth:.2f}")
    return philhealth


def compute_pagibig(salary):
    thread_name = threading.current_thread().name
    pagibig = salary * 0.02
    print(f"[{thread_name}] Pag-IBIG Deduction: {pagibig:.2f}")
    return pagibig

def task_parallelism_example(salary):
    print("\n===== PART A: Task Parallelism (ThreadPoolExecutor) =====")

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_sss = executor.submit(compute_sss, salary)
        future_philhealth = executor.submit(compute_philhealth, salary)
        future_pagibig = executor.submit(compute_pagibig, salary)
        future_tax = executor.submit(compute_withholding_tax, salary)

        sss = future_sss.result()
        philhealth = future_philhealth.result()
        pagibig = future_pagibig.result()
        tax = future_tax.result()

    total_deduction = sss + philhealth + pagibig + tax

    print(f"\nTotal Deduction: {total_deduction:.2f}")
    print("===============================================") 

def compute_withholding_tax(salary):
    thread_name = threading.current_thread().name
    tax = salary * 0.10
    print(f"[{thread_name}] Withholding Tax: {tax:.2f}")
    return tax

# PART B
def compute_payroll(employee):
    """
    Computes complete payroll for one employee.
    This function will run in separate processes.
    """
    name, salary = employee

    sss = salary * 0.05
    philhealth = salary * 0.04
    pagibig = salary * 0.02
    tax = salary * 0.10

    total_deduction = sss + philhealth + pagibig + tax
    net_salary = salary - total_deduction

    return {
        "name": name,
        "gross_salary": salary,
        "total_deduction": total_deduction,
        "net_salary": net_salary,
        "process_id": os.getpid()
    } 

def data_parallelism_example(employees):
    print("\n===== PART B: Data Parallelism (ProcessPoolExecutor) =====")

    with ProcessPoolExecutor() as executor:
        results = executor.map(compute_payroll, employees)

        for result in results:
            print(f"\nEmployee: {result['name']}")
            print(f"Process ID: {result['process_id']}")
            print(f"Gross Salary: {result['gross_salary']:.2f}")
            print(f"Total Deduction: {result['total_deduction']:.2f}")
            print(f"Net Salary: {result['net_salary']:.2f}")

    print("===============================================")

if __name__ == "__main__":

    # Part A: Single employee salary
    employee_salary = 50000
    task_parallelism_example(employee_salary)

    # Part B: Multiple employees
    employee_list = [
        ("Alice", 50000),
        ("Bob", 45000),
        ("Charlie", 60000),
        ("Diana", 55000),
        ("Edward", 48000),
    ]

    data_parallelism_example(employee_list)