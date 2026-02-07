import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class GWACalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GWA Calculator - Performance Edition")
        self.root.geometry("650x750")
        self.root.configure(bg="#f8f9fa")
        
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure("TFrame", background="#f8f9fa")
        self.style.configure("TLabel", background="#f8f9fa", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#212529")
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"))
        
        self.style.configure("Calculate.TButton", foreground="white", background="#0d6efd")
        self.style.map("Calculate.TButton", background=[('active', '#0b5ed7')])
        
        self.style.configure("Row.TEntry", fieldbackground="white")

        self.subjects_data = []
        self.setup_ui()

    def setup_ui(self):
        # Main wrapper to help with centering everything
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=40)

        # Header
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(pady=(30, 20), fill="x")
        ttk.Label(header_frame, text="Grade Weighted Average", style="Header.TLabel", anchor="center").pack(fill="x")
        ttk.Label(header_frame, text="Centralized Computing System", font=("Segoe UI", 9), foreground="#6c757d", anchor="center").pack(fill="x")

        # Input for number of subjects - Centralized
        input_outer_frame = ttk.Frame(self.main_frame)
        input_outer_frame.pack(pady=10, fill="x")
        
        input_inner_frame = ttk.Frame(input_outer_frame)
        input_inner_frame.pack(anchor="center") # Centering the input group
        
        ttk.Label(input_inner_frame, text="Number of Subjects:").grid(row=0, column=0, padx=5)
        self.num_subjects_var = tk.StringVar(value="3")
        self.num_entry = ttk.Entry(input_inner_frame, textvariable=self.num_subjects_var, width=8, justify="center")
        self.num_entry.grid(row=0, column=1, padx=5)
        
        self.generate_btn = ttk.Button(input_inner_frame, text="Generate Rows", command=self.generate_rows)
        self.generate_btn.grid(row=0, column=2, padx=10)

        # Scrollable area for subjects
        self.container = ttk.Frame(self.main_frame)
        self.container.pack(pady=10, fill="both", expand=True)

        self.canvas = tk.Canvas(self.container, bg="#ffffff", highlightthickness=1, highlightbackground="#dee2e6")
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        
        # This frame will hold the rows
        self.scrollable_frame = ttk.Frame(self.canvas, style="TFrame")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window in canvas and center it
        self.canvas_window = self.canvas.create_window((325, 0), window=self.scrollable_frame, anchor="n")
        
        def on_canvas_configure(e):
            # Keep the scrollable frame centered when canvas resizing
            self.canvas.itemconfig(self.canvas_window, width=e.width)

        self.canvas.bind("<Configure>", on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Footer / Calculate Button
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(pady=30, fill="x")
        
        self.calc_btn = ttk.Button(footer_frame, text="Calculate GWA", style="Calculate.TButton", command=self.calculate_gwa)
        self.calc_btn.pack(ipady=8, ipadx=20)

        self.result_label = ttk.Label(footer_frame, text="", font=("Segoe UI", 14, "bold"), anchor="center")
        self.result_label.pack(pady=(15, 5), fill="x")
        
        self.time_label = ttk.Label(footer_frame, text="", font=("Segoe UI", 9), foreground="#6c757d", anchor="center")
        self.time_label.pack(fill="x")

        # Initial rows
        self.generate_rows()

    def generate_rows(self):
        # Clear existing rows
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.subjects_data = []

        try:
            n = int(self.num_subjects_var.get())
            if n <= 0: raise ValueError
            if n > 8: # Limit to 8 rows
                messagebox.showwarning("Limit Reached", "A maximum of 8 subjects is allowed for this layout.")
                n = 8
                self.num_subjects_var.set("8")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number of subjects.")
            return

        # Table Header with centering
        header_row = ttk.Frame(self.scrollable_frame)
        header_row.pack(fill="x", pady=10)
        header_row.columnconfigure((0,1,2), weight=1)

        ttk.Label(header_row, text="Subject Name", font=("Segoe UI", 9, "bold")).grid(row=0, column=0)
        ttk.Label(header_row, text="Grade (1.0-5.0)", font=("Segoe UI", 9, "bold")).grid(row=0, column=1)
        ttk.Label(header_row, text="Units", font=("Segoe UI", 9, "bold")).grid(row=0, column=2)

        for i in range(n):
            row_frame = ttk.Frame(self.scrollable_frame)
            row_frame.pack(fill="x", pady=2)
            row_frame.columnconfigure((0,1,2), weight=1)

            name_var = tk.StringVar(value=f"Subject {i+1}")
            grade_var = tk.StringVar()
            unit_var = tk.StringVar()

            e1 = ttk.Entry(row_frame, textvariable=name_var, justify="center")
            e2 = ttk.Entry(row_frame, textvariable=grade_var, justify="center", width=10)
            e3 = ttk.Entry(row_frame, textvariable=unit_var, justify="center", width=10)

            e1.grid(row=0, column=0, padx=10, sticky="ew")
            e2.grid(row=0, column=1, padx=10)
            e3.grid(row=0, column=2, padx=10)

            self.subjects_data.append((name_var, grade_var, unit_var))


    def calculate_gwa(self):
        grades = []
        units = []
        
        try:
            for name_var, grade_var, unit_var in self.subjects_data:
                name = name_var.get().strip()
                g_str = grade_var.get().strip()
                u_str = unit_var.get().strip()
                
                if not g_str or not u_str:
                    messagebox.showwarning("Incomplete", f"Please fill in grades and units for '{name}'.")
                    return
                
                grade = float(g_str)
                # Grade range validation (1.0 to 5.0)
                if not (1.0 <= grade <= 5.0):
                    messagebox.showerror("Invalid Grade", f"Grade for '{name}' must be between 1.0 and 5.0.")
                    return
                
                unit = int(u_str)
                # Unit range validation (1 to 3)
                if not (1 <= unit <= 4):
                    messagebox.showerror("Invalid Units", f"Units for '{name}' must be between 1 and 4.")
                    return
                
                grades.append(grade)
                units.append(unit)
        except ValueError:
            messagebox.showerror("Invalid Input", "Make sure grades are numbers and units are integers.")
            return

        # Multithreading Logic (from GWA1.py)
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

        task = GWATask(grades, units)
        start = time.perf_counter()

        with ThreadPoolExecutor() as executor:
            for i in range(len(grades)):
                executor.submit(task.compute, i)

        if task.total_units == 0:
            messagebox.showerror("Error", "Total units cannot be zero.")
            return

        gwa = task.weighted_sum / task.total_units
        end = time.perf_counter()

        self.result_label.config(text=f"Final GWA: {gwa:.3f}", foreground="#27ae60")
        self.time_label.config(text=f"Computed in {end - start:.6f} seconds (Multithreaded)")

if __name__ == "__main__":
    root = tk.Tk()
    app = GWACalculatorGUI(root)
    root.mainloop()

#if cloned into a pc so u can run with gui
