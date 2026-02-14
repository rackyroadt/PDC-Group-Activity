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