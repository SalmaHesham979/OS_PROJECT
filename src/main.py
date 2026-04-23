import tkinter as tk
from tkinter import ttk, messagebox
# استيراد الموديل من الفولدر اللي عملناه
from src.model.process import Process

# قائمة تخزين العمليات
all_processes = []


def add_process():
    try:
        # 1. سحب البيانات
        pid = entry_pid.get().strip()
        arrival_text = entry_arrival.get().strip()
        burst_text = entry_burst.get().strip()
        priority_text = entry_priority.get().strip()

        # 2. الـ Validation (عشان درجات الـ Input Handling)
        if not (pid and arrival_text and burst_text and priority_text):
            messagebox.showerror("Error", "Please fill all fields!")
            return

        arrival = int(arrival_text)
        burst = int(burst_text)
        priority = int(priority_text)

        if arrival < 0 or burst <= 0:
            messagebox.showerror("Error", "Arrival/Burst cannot be negative or zero!")
            return

        # التأكد من عدم تكرار الـ ID
        for p in all_processes:
            if p.pid == pid:
                messagebox.showerror("Error", "Process ID already exists!")
                return

        # 3. إنشاء العملية وحفظها
        new_p = Process(pid, arrival, burst, priority)
        all_processes.append(new_p)

        # 4. تحديث الجدول
        tree.insert('', 'end', values=(pid, arrival, burst, priority))

        # تنظيف الخانات
        entry_pid.delete(0, tk.END)
        entry_arrival.delete(0, tk.END)
        entry_burst.delete(0, tk.END)
        entry_priority.delete(0, tk.END)
        entry_pid.focus()  # يخلي الماوس يرجع لأول خانة لوحده

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values!")


# --- إعداد النافذة الرئيسية ---
root = tk.Tk()
root.title("OS Project - Priority vs SRTF")
root.geometry("850x600")
root.minsize(700, 500)

# جعل النافذة مرنة عند التكبير
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

# --- 1. لوحة الإدخال (الخانات جنب بعض) ---
input_frame = tk.LabelFrame(root, text=" 📝 Add New Process ", padx=15, pady=15)
input_frame.pack(side="top", fill="x", padx=20, pady=15)

# توزيع الـ Grid داخل الفريم ليكونوا جنب بعض
for i in range(8):
    input_frame.columnconfigure(i, weight=1)

# الخانات
tk.Label(input_frame, text="PID:").grid(row=0, column=0, sticky="e")
entry_pid = tk.Entry(input_frame, width=10)
entry_pid.grid(row=0, column=1, padx=5, sticky="w")

tk.Label(input_frame, text="Arrival:").grid(row=0, column=2, sticky="e")
entry_arrival = tk.Entry(input_frame, width=10)
entry_arrival.grid(row=0, column=3, padx=5, sticky="w")

tk.Label(input_frame, text="Burst:").grid(row=0, column=4, sticky="e")
entry_burst = tk.Entry(input_frame, width=10)
entry_burst.grid(row=0, column=5, padx=5, sticky="w")

tk.Label(input_frame, text="Priority:").grid(row=0, column=6, sticky="e")
entry_priority = tk.Entry(input_frame, width=10)
entry_priority.grid(row=0, column=7, padx=5, sticky="w")

# --- 2. زرار الإضافة ---
btn_add = tk.Button(root, text="+ Add Process to Table", command=add_process,
                    bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), pady=5)
btn_add.pack(side="top", fill="x", padx=150, pady=5)

# --- 3. الجدول (Responsive Table) ---
table_frame = tk.Frame(root)
table_frame.pack(side="top", fill="both", expand=True, padx=20, pady=15)

columns = ("PID", "Arrival", "Burst", "Priority")
tree = ttk.Treeview(table_frame, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=100)

# إضافة Scrollbar للجدول
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- 4. زرار المحاكاة (Run Simulation) ---
btn_simulate = tk.Button(root, text="🚀 Run Simulation", bg="#2196F3", fg="white",
                         font=("Arial", 12, "bold"), pady=10)
btn_simulate.pack(side="bottom", fill="x", padx=100, pady=20)

root.mainloop()