import tkinter as tk
from tkinter import ttk, messagebox
import copy

# استيراد الموديلات والمنطق
from model.process import Process
from scheduler.priority import run_priority_preemptive
from scheduler.srtf import run_srtf


def start_app():
    all_processes = []

    # --- باليتة الألوان (الأسود والبينك) ---
    color_bg = "#121212"  # خلفية سوداء مطفية
    color_card = "#1E1E1E"  # رمادي داكن للفريمات
    color_pink = "#FF69B4"  # Hot Pink للزراير واللمسات
    color_white = "#FFFFFF"  # أبيض للكلام
    color_input = "#2D2D2D"  # خلفية خانات الإدخال

    gantt_colors = ["#FF69B4", "#FF1493", "#C71585", "#DB7093", "#FF82AB", "#FFB6C1"]

    # --- 1. الوظائف (Functions) ---
    def clear_data():
        all_processes.clear()
        for item in tree.get_children(): tree.delete(item)
        canvas_p.delete("all");
        canvas_s.delete("all")
        for t in [tree_res_p, tree_res_s]:
            for item in t.get_children(): t.delete(item)
        lbl_avg_p.config(text="Avg WT: 0, TAT: 0");
        lbl_avg_s.config(text="Avg WT: 0, TAT: 0")
        text_summary.config(state="normal");
        text_summary.delete("1.0", tk.END);
        text_summary.config(state="disabled")

    def add_process():
        try:
            pid = entry_pid.get().strip()
            at, bt, pr = int(entry_arrival.get()), int(entry_burst.get()), int(entry_priority.get())
            if any(p.pid == pid for p in all_processes):
                messagebox.showerror("Error", "Process ID already exists!")
                return
            all_processes.append(Process(pid, at, bt, pr))
            tree.insert('', 'end', values=(pid, at, bt, pr))
            for e in [entry_pid, entry_arrival, entry_burst, entry_priority]: e.delete(0, tk.END)
            entry_pid.focus()
        except:
            messagebox.showerror("Error", "Invalid Input!")

    def load_test_case(case_type):
        clear_data()
        cases = {
            "Normal": [("P1", 0, 8, 3), ("P2", 2, 4, 1), ("P3", 4, 6, 2)],
            "Conflict": [("P1", 0, 5, 2), ("P2", 0, 3, 2), ("P3", 5, 2, 1)],
            "Starvation": [("P1", 0, 15, 10), ("P2", 1, 2, 1), ("P3", 2, 2, 1), ("P4", 3, 2, 1)],
            "Invalid": [("P_Err", -1, 0, 1)]
        }
        if case_type == "Invalid":
            p = cases["Invalid"][0]
            entry_pid.insert(0, p[0]);
            entry_arrival.insert(0, p[1])
            entry_burst.insert(0, p[2]);
            entry_priority.insert(0, p[3])
        elif case_type in cases:
            for p in cases[case_type]:
                all_processes.append(Process(p[0], p[1], p[2], p[3]))
                tree.insert('', 'end', values=p)

    def draw_gantt(canvas, data):
        canvas.delete("all")
        x, y, h, scale = 50, 15, 35, 25
        for i, (pid, start, end) in enumerate(data):
            w = (end - start) * scale
            canvas.create_rectangle(x, y, x + w, y + h, fill=gantt_colors[i % 6], outline=color_white)
            canvas.create_text(x + w / 2, y + h / 2, text=pid, fill=color_white, font=("Arial", 9, "bold"))
            canvas.create_text(x, y + h + 10, text=str(start), fill=color_pink, font=("Arial", 8))
            x += w
        if data: canvas.create_text(x, y + h + 10, text=str(data[-1][2]), fill=color_pink, font=("Arial", 8))

    def run_simulation():
        if not all_processes: return
        p_data, s_data = copy.deepcopy(all_processes), copy.deepcopy(all_processes)
        g_p, g_s = run_priority_preemptive(p_data), run_srtf(s_data)
        draw_gantt(canvas_p, g_p);
        draw_gantt(canvas_s, g_s)
        pm = fill_res(tree_res_p, p_data, lbl_avg_p)
        sm = fill_res(tree_res_s, s_data, lbl_avg_s)
        generate_summary(pm, sm)
        notebook.select(tab2)

    def fill_res(t, data, l):
        for i in t.get_children(): t.delete(i)
        for p in data: t.insert('', 'end', values=(p.pid, p.waiting_time, p.turnaround_time, p.response_time))
        n = len(data)
        avg_wt, avg_tat = sum(p.waiting_time for p in data) / n, sum(p.turnaround_time for p in data) / n
        l.config(text=f"Averages -> WT: {avg_wt:.2f}, TAT: {avg_tat:.2f}")
        return avg_wt, avg_tat

    def generate_summary(pm, sm):
        text_summary.config(state="normal");
        text_summary.delete("1.0", tk.END)
        winner = "SRTF" if sm[0] < pm[0] else "Priority"
        summary = f"--- SIMULATION CONCLUSION & SUMMARY ---\n\n"
        summary += f"- Efficiency Winner: {winner} (Min WT: {min(sm[0], pm[0]):.2f})\n"
        summary += f"- Priority Stats: Avg WT = {pm[0]:.2f}, Avg TAT = {pm[1]:.2f}\n"
        summary += f"- SRTF Stats: Avg WT = {sm[0]:.2f}, Avg TAT = {sm[1]:.2f}\n\n"
        summary += "--- STARVATION ANALYSIS ---\n"
        summary += "In the Priority case, low-priority tasks may suffer from starvation.\n"
        summary += "SRTF is optimal for average wait time but requires knowing burst times."
        text_summary.insert(tk.END, summary);
        text_summary.config(state="disabled")

    # --- 2. بناء الواجهة (UI) ---
    root = tk.Tk()
    root.title("CPU Scheduling Simulator - Black & Pink Edition")
    root.geometry("1100x880");
    root.configure(bg=color_bg)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TNotebook", background=color_bg, borderwidth=0)
    style.configure("TNotebook.Tab", background=color_card, foreground=color_white, padding=[20, 8],
                    font=("Arial", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", color_pink)], foreground=[("selected", "black")])
    style.configure("Treeview", background=color_card, foreground=color_white, fieldbackground=color_card, rowheight=25)
    style.configure("Treeview.Heading", background=color_pink, foreground="black", font=("Arial", 10, "bold"))

    notebook = ttk.Notebook(root)
    tab1 = tk.Frame(notebook, bg=color_bg);
    tab2 = tk.Frame(notebook, bg=color_bg)
    notebook.add(tab1, text=" 1. CONFIGURATION ");
    notebook.add(tab2, text=" 2. ANALYSIS & RESULTS ")
    notebook.pack(expand=True, fill="both")

    # Tab 1
    input_f = tk.LabelFrame(tab1, text=" Add New Process ", bg=color_bg, fg=color_pink, font=("Arial", 11, "bold"),
                            padx=15, pady=15)
    input_f.pack(fill="x", padx=25, pady=20)

    lbls_names = ["Process ID:", "Arrival Time:", "Burst Time:", "Priority:"]
    vars_names = ["entry_pid", "entry_arrival", "entry_burst", "entry_priority"]
    for i, txt in enumerate(lbls_names):
        tk.Label(input_f, text=txt, bg=color_bg, fg=color_white, font=("Arial", 10)).grid(row=0, column=i * 2, padx=10)
        globals()[vars_names[i]] = tk.Entry(input_f, width=12, bg=color_input, fg=color_white,
                                            insertbackground=color_white, relief="flat", highlightthickness=1,
                                            highlightbackground=color_pink)
        globals()[vars_names[i]].grid(row=0, column=i * 2 + 1)

    tk.Button(input_f, text="+ Add Process", command=add_process, bg=color_pink, fg="black", font=("Arial", 10, "bold"),
              relief="flat", padx=15).grid(row=0, column=8, padx=25)

    btn_f = tk.Frame(tab1, bg=color_bg);
    btn_f.pack(fill="x", padx=25)
    for c in ["Normal", "Conflict", "Starvation", "Invalid"]:
        tk.Button(btn_f, text=f"Load {c}", command=lambda case=c: load_test_case(case), bg=color_bg, fg=color_pink,
                  highlightthickness=1, highlightbackground=color_pink, relief="flat", padx=12, pady=5).pack(
            side="left", padx=5)

    tk.Button(btn_f, text="RUN SIMULATION 🚀", command=run_simulation, bg=color_pink, fg="black",
              font=("Arial", 10, "bold"), padx=25, pady=8).pack(side="right", padx=5)
    tk.Button(btn_f, text="Clear", command=clear_data, bg=color_card, fg=color_white, relief="flat", padx=15).pack(
        side="right", padx=15)

    # تعديل أسماء الأعمدة هنا
    tree_columns = ("Process ID", "Arrival Time", "Burst Time", "Priority")
    tree = ttk.Treeview(tab1, columns=tree_columns, show='headings', height=15)
    for c in tree_columns:
        tree.heading(c, text=c)
        tree.column(c, anchor="center")
    tree.pack(fill="both", expand=True, padx=25, pady=20)

    # Tab 2
    gf = tk.LabelFrame(tab2, text=" Gantt Charts ", bg=color_bg, fg=color_pink, font=("Arial", 11, "bold"), padx=15,
                       pady=10)
    gf.pack(fill="x", padx=25, pady=10)
    for n, v in [("Priority Scheduling", "canvas_p"), ("SRTF Scheduling", "canvas_s")]:
        tk.Label(gf, text=n, bg=color_bg, fg=color_white, font=("Arial", 9, "italic")).pack(anchor="w", padx=15)
        globals()[v] = tk.Canvas(gf, height=85, bg="#181818", highlightthickness=1, highlightbackground=color_card)
        globals()[v].pack(fill="x", padx=15, pady=8)

    rf = tk.Frame(tab2, bg=color_bg);
    rf.pack(fill="x", padx=20)
    for name, tv_var, lb_var in [("Priority", "tree_res_p", "lbl_avg_p"), ("SRTF", "tree_res_s", "lbl_avg_s")]:
        f = tk.LabelFrame(rf, text=f" {name} Metrics ", bg=color_bg, fg=color_pink, font=("Arial", 10, "bold"), padx=10,
                          pady=10)
        f.pack(side="left", expand=True, fill="both", padx=10)
        t = ttk.Treeview(f, columns=("ID", "WT", "TAT", "RT"), show='headings', height=6)
        for c in ("ID", "WT", "TAT", "RT"): t.heading(c, text=c); t.column(c, width=65, anchor="center")
        t.pack(fill="both");
        l = tk.Label(f, text="Avg WT: 0, TAT: 0", bg=color_bg, fg=color_pink, font=("Arial", 10, "bold"))
        l.pack(pady=8)
        if name == "Priority":
            tree_res_p, lbl_avg_p = t, l
        else:
            tree_res_s, lbl_avg_s = t, l

    summary_f = tk.LabelFrame(tab2, text=" Conclusion Summary ", bg=color_bg, fg=color_pink, font=("Arial", 11, "bold"),
                              padx=15, pady=10)
    summary_f.pack(fill="both", expand=True, padx=25, pady=15)
    text_summary = tk.Text(summary_f, height=8, bg="#181818", fg=color_white, relief="flat", font=("Courier New", 10),
                           padx=15, pady=15)
    text_summary.pack(fill="both", expand=True);
    text_summary.config(state="disabled")

    root.mainloop()