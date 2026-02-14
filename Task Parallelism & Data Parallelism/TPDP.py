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


def compute_withholding_tax(salary):
    thread_name = threading.current_thread().name
    tax = salary * 0.10
    print(f"[{thread_name}] Withholding Tax: {tax:.2f}")
    return tax


# PART B TASK 

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