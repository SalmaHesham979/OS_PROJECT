import tkinter as tk
from tkinter import ttk, messagebox
import copy

# استيراد الموديل والمنطق (Logic) من الفولدرات التانية
from model.process import Process
from scheduler.priority import run_priority_preemptive
from scheduler.srtf import run_srtf


def start_app():
    all_processes = []

    # --- وظائف التحكم (Functions) ---
    def clear_data():
        all_processes.clear()
        for item in tree.get_children():
            tree.delete(item)

    def load_test_case(case_type):
        clear_data()
        # الـ 4 حالات اللي في المرجع
        test_cases = {
            "Normal": [("P1", 0, 8, 3), ("P2", 2, 4, 1), ("P3", 4, 6, 2)],
            "Conflict": [("P1", 0, 5, 2), ("P2", 0, 3, 2), ("P3", 5, 2, 1)],
            "Starvation": [("P1", 0, 15, 10), ("P2", 1, 2, 1), ("P3", 2, 2, 1), ("P4", 3, 2, 1)],
            "Invalid": [("P_Error", -5, 0, 1)]
        }

        if case_type in test_cases:
            if case_type == "Invalid":
                # بنملأ الخانات بس عشان نختبر الـ Validation
                p = test_cases["Invalid"][0]
                entry_pid.insert(0, p[0]);
                entry_arrival.insert(0, p[1])
                entry_burst.insert(0, p[2]);
                entry_priority.insert(0, p[3])
                messagebox.showinfo("Test Case", "Invalid data loaded! Click 'Add Process' to test error handling.")
            else:
                for p in test_cases[case_type]:
                    new_p = Process(p[0], p[1], p[2], p[3])
                    all_processes.append(new_p)
                    tree.insert('', 'end', values=p)

    def add_process():
        try:
            pid = entry_pid.get().strip()
            at = int(entry_arrival.get().strip())
            bt = int(entry_burst.get().strip())
            pr = int(entry_priority.get().strip())

            if any(p.pid == pid for p in all_processes):
                messagebox.showerror("Error", "Process ID already exists!")
                return

            new_p = Process(pid, at, bt, pr)
            all_processes.append(new_p)
            tree.insert('', 'end', values=(pid, at, bt, pr))

            # تنظيف الخانات
            for e in [entry_pid, entry_arrival, entry_burst, entry_priority]: e.delete(0, tk.END)
            entry_pid.focus()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")

    def run_simulation():
        if not all_processes:
            messagebox.showwarning("Warning", "Please add processes first!")
            return

        selected_algo = combo_algo.get()
        test_data = copy.deepcopy(all_processes)

        # تشغيل الخوارزمية المختارة
        if selected_algo == "Priority Preemptive":
            gantt = run_priority_preemptive(test_data)
        else:
            gantt = run_srtf(test_data)

        # حساب المتوسطات
        n = len(test_data)
        avg_wt = sum(p.waiting_time for p in test_data) / n
        avg_tat = sum(p.turnaround_time for p in test_data) / n

        messagebox.showinfo("Simulation Results",
                            f"Algorithm: {selected_algo}\nAvg WT: {avg_wt:.2f}\nAvg TAT: {avg_tat:.2f}")
        notebook.select(tab2)  # الانتقال لتبويب النتائج أوتوماتيك

    # --- إعداد النافذة (UI Setup) ---
    root = tk.Tk()
    root.title("CPU Scheduling Simulator (Priority Preemptive vs SRTF)")
    root.geometry("1100x650")

    # نظام التبويبات (Tabs)
    notebook = ttk.Notebook(root)
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    notebook.add(tab1, text=" 1. Process Configuration ")
    notebook.add(tab2, text=" 2. Simulation Results (Gantt & Metrics) ")
    notebook.pack(expand=True, fill="both")

    # --- Tab 1: Configuration ---
    # 1. Input Panel (بالعرض زي المرجع)
    input_panel = tk.LabelFrame(tab1, text=" Input Panel ", padx=10, pady=10)
    input_panel.pack(fill="x", padx=15, pady=10)

    tk.Label(input_panel, text="Process ID:").grid(row=0, column=0, padx=2)
    entry_pid = tk.Entry(input_panel, width=10);
    entry_pid.grid(row=0, column=1, padx=5)

    tk.Label(input_panel, text="Arrival Time:").grid(row=0, column=2, padx=2)
    entry_arrival = tk.Entry(input_panel, width=10);
    entry_arrival.grid(row=0, column=3, padx=5)

    tk.Label(input_panel, text="Burst Time:").grid(row=0, column=4, padx=2)
    entry_burst = tk.Entry(input_panel, width=10);
    entry_burst.grid(row=0, column=5, padx=5)

    tk.Label(input_panel, text="Priority (0 is highest):").grid(row=0, column=6, padx=2)
    entry_priority = tk.Entry(input_panel, width=10);
    entry_priority.grid(row=0, column=7, padx=5)

    tk.Button(input_panel, text="Add Process", command=add_process).grid(row=0, column=8, padx=10)

    # 2. Action Frame (زراير الـ Load والـ Run)
    action_frame = tk.Frame(tab1)
    action_frame.pack(fill="x", padx=15, pady=5)

    # زراير الحالات الـ 4 (يسار)
    tk.Button(action_frame, text="Load Normal Case", command=lambda: load_test_case("Normal")).pack(side="left", padx=2)
    tk.Button(action_frame, text="Load Conflict Case", command=lambda: load_test_case("Conflict")).pack(side="left",
                                                                                                        padx=2)
    tk.Button(action_frame, text="Load Starvation Case", command=lambda: load_test_case("Starvation")).pack(side="left",
                                                                                                            padx=2)
    tk.Button(action_frame, text="Load Invalid Case", command=lambda: load_test_case("Invalid")).pack(side="left",
                                                                                                      padx=2)

    # اختيار الخوارزمية وزرار التشغيل (يمين)
    tk.Button(action_frame, text="Clear Data", command=clear_data, bg="#ffcccc").pack(side="right", padx=5)
    tk.Button(action_frame, text="Run Simulation", command=run_simulation, bg="#2196F3", fg="white",
              font=("Arial", 10, "bold")).pack(side="right", padx=5)

    combo_algo = ttk.Combobox(action_frame, values=["Priority Preemptive", "SRTF"], state="readonly", width=20)
    combo_algo.set("Priority Preemptive")
    combo_algo.pack(side="right", padx=10)

    # 3. Process Table
    tree_frame = tk.LabelFrame(tab1, text=" Process Table ", padx=10, pady=10)
    tree_frame.pack(expand=True, fill="both", padx=15, pady=10)

    columns = ("PID", "Arrival", "Burst", "Priority")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    tree.pack(side="left", expand=True, fill="both")
    scrollbar.pack(side="right", fill="y")

    # --- Tab 2: Results ---
    tk.Label(tab2, text="Gantt Chart and Performance Metrics will be displayed here.",
             font=("Arial", 12, "italic")).pack(pady=100)

    root.mainloop()