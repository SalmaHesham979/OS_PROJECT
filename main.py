import tkinter as tk
from tkinter import ttk, messagebox
# التأكد من الربط بملف البطاقة الشخصية
from model.process import Process

# قائمة لتخزين كل العمليات اللي هندخلها
all_processes = []


def add_process():
    try:
        # 1. سحب البيانات من الخانات
        pid = entry_pid.get()
        arrival_text = entry_arrival.get()
        burst_text = entry_burst.get()
        priority_text = entry_priority.get()

        # 2. الـ Validation (عشان تضمني الـ 10 درجات)
        if not (pid and arrival_text and burst_text and priority_text):
            messagebox.showerror("Error", "Please fill all fields!")
            return

        arrival = int(arrival_text)
        burst = int(burst_text)
        priority = int(priority_text)

        if arrival < 0 or burst <= 0:
            messagebox.showerror("Error", "Arrival/Burst cannot be negative or zero!")
            return

        # 3. حفظ العملية في القائمة (The Model)
        new_p = Process(pid, arrival, burst, priority)
        all_processes.append(new_p)

        # 4. عرض العملية في الجدول قدام عينك (The View)
        tree.insert('', 'end', values=(pid, arrival, burst, priority))

        # تنظيف الخانات عشان ندخل مريض جديد
        entry_pid.delete(0, tk.END)
        entry_arrival.delete(0, tk.END)
        entry_burst.delete(0, tk.END)
        entry_priority.delete(0, tk.END)

        print(f"Added: {pid}, Total processes: {len(all_processes)}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for Arrival, Burst, and Priority!")


# --- إعداد النافذة ---
root = tk.Tk()
root.title("OS Project - Priority vs SRTF")
root.geometry("600x600")

# --- لوحة الإدخال (Input Panel) ---
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

tk.Label(input_frame, text="Process ID:").grid(row=0, column=0, padx=5)
entry_pid = tk.Entry(input_frame, width=10)
entry_pid.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Arrival Time:").grid(row=1, column=0, padx=5)
entry_arrival = tk.Entry(input_frame, width=10)
entry_arrival.grid(row=1, column=1, padx=5)

tk.Label(input_frame, text="Burst Time:").grid(row=2, column=0, padx=5)
entry_burst = tk.Entry(input_frame, width=10)
entry_burst.grid(row=2, column=1, padx=5)

tk.Label(input_frame, text="Priority:").grid(row=3, column=0, padx=5)
entry_priority = tk.Entry(input_frame, width=10)
entry_priority.grid(row=3, column=1, padx=5)

# زرار الإضافة (أخضر شيك)
btn_add = tk.Button(root, text="Add Process", command=add_process, bg="#4CAF50", fg="white", width=15)
btn_add.pack(pady=10)

# --- الجدول (The Table) ---
tk.Label(root, text="Added Processes List:", font=("Arial", 10, "bold")).pack()
columns = ("PID", "Arrival", "Burst", "Priority")
tree = ttk.Treeview(root, columns=columns, show='headings', height=8)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

tree.pack(pady=10, padx=20)

# --- زرار المحاكاة (Run Simulation) ---
# ده اللي هيفجر المعادلات والرسومات في الخطوة الجاية
btn_simulate = tk.Button(root, text="Run Simulation", bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=20)
btn_simulate.pack(pady=20)

root.mainloop()