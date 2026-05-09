import tkinter as tk
from tkinter import ttk, messagebox
import copy

# استيراد الموديلات والمنطق
from model.process import Process
from scheduler.priority import run_priority_preemptive
from scheduler.srtf import run_srtf
from metrics.calculator import calculate_averages
from util.validators import validate_process_input


def start_app():
    all_processes = []

    # --- باليتة الألوان (الأسود والبينك) ---
    color_bg = "#121212"  # خلفية سوداء مطفية
    color_card = "#1E1E1E"  # رمادي داكن للفريمات
    color_pink = "#FF69B4"  # Hot Pink للزراير واللمسات
    color_white = "#FFFFFF"  # أبيض للكلام
    color_input = "#2D2D2D"  # خلفية خانات الإدخال
    gantt_pinks = ["#FF69B4", "#FF1493", "#C71585", "#DB7093", "#FF82AB", "#FFB6C1"]

    # --- 1. الوظائف (Functions) ---
    def clear_data():
        all_processes.clear()
        for item in tree.get_children(): tree.delete(item)
        canvas_p.delete("all");
        canvas_s.delete("all")
        for t in [tree_res_p, tree_res_s]:
            for item in t.get_children(): t.delete(item)
        lbl_avg_p.config(text="Avg -> WT: 0, TAT: 0, RT: 0")
        lbl_avg_s.config(text="Avg -> WT: 0, TAT: 0, RT: 0")
        text_summary.config(state="normal");
        text_summary.delete("1.0", tk.END);
        text_summary.config(state="disabled")

    def add_process():
        pid = entry_pid.get().strip()
        arrival = entry_arrival.get().strip()
        burst = entry_burst.get().strip()
        priority = entry_priority.get().strip()

        is_valid, errors, parsed_values = validate_process_input(
            pid, arrival, burst, priority, all_processes
        )

        if not is_valid:
            if errors == ["All fields must be filled!"]:
                messagebox.showerror("Error", "All fields must be filled!")
            else:
                full_error_msg = "Please fix the following issues:\n\n" + "\n".join(errors)
                messagebox.showerror("Validation Error", full_error_msg)
            return

        at_val, bt_val, pr_val = parsed_values

        all_processes.append(Process(pid, at_val, bt_val, pr_val))
        tree.insert('', 'end', values=(pid, at_val, bt_val, pr_val))
        for e in [entry_pid, entry_arrival, entry_burst, entry_priority]: e.delete(0, tk.END)
        entry_pid.focus()

    def load_test_case(case_type):
        for e in [entry_pid, entry_arrival, entry_burst, entry_priority]: e.delete(0, tk.END)
        clear_data()
        cases = {
            "Normal": [("P1", 0, 8, 3), ("P2", 2, 4, 1), ("P3", 4, 6, 2)],
            "Conflict": [("P1", 0, 10, 1), ("P2", 1, 2, 5), ("P3", 2, 1, 5)],
            "Starvation": [("P1", 0, 20, 10), ("P2", 1, 3, 1), ("P3", 3, 3, 1), ("P4", 5, 3, 1), ("P5", 7, 3, 1)],
            "Invalid": [("P_Error", -3, 0, 1)]
        }
        if case_type == "Invalid":
            p = cases["Invalid"][0]
            for i, val in enumerate(p): [entry_pid, entry_arrival, entry_burst, entry_priority][i].insert(0, val)
        elif case_type in cases:
            for p in cases[case_type]:
                all_processes.append(Process(p[0], p[1], p[2], p[3]));
                tree.insert('', 'end', values=p)

    def draw_gantt(canvas, data):
        canvas.delete("all")
        x, y, h, scale = 50, 15, 35, 25
        for i, (pid, start, end) in enumerate(data):
            w = (end - start) * scale
            canvas.create_rectangle(x, y, x + w, y + h, fill=gantt_pinks[i % 6], outline=color_white)
            canvas.create_text(x + w / 2, y + h / 2, text=pid, fill=color_white, font=("Arial", 9, "bold"))
            canvas.create_text(x, y + h + 10, text=str(start), fill=color_pink, font=("Arial", 8))
            x += w
        if data: canvas.create_text(x, y + h + 10, text=str(data[-1][2]), fill=color_pink, font=("Arial", 8))

    def run_simulation():
        if not all_processes: return
        p_data, s_data = copy.deepcopy(all_processes), copy.deepcopy(all_processes)
        # تشغيل الخوارزميات مع الـ Tie-breaking المحدث (PID)
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
        
        avg_wt, avg_tat, avg_rt = calculate_averages(data)
        
        l.config(text=f"Avg -> WT: {avg_wt:.2f}, TAT: {avg_tat:.2f}, RT: {avg_rt:.2f}")
        return avg_wt, avg_tat, avg_rt

    def generate_summary(pm, sm):
        text_summary.config(state="normal");
        text_summary.delete("1.0", tk.END)

        wt_winner = "SRTF" if sm[0] < pm[0] else ("Priority" if pm[0] < sm[0] else "TIE")
        tat_winner = "SRTF" if sm[1] < pm[1] else ("Priority" if pm[1] < sm[1] else "TIE")
        rt_winner = "SRTF" if sm[2] < pm[2] else ("Priority" if pm[2] < sm[2] else "TIE")
        overall = "SRTF" if sm[0] < pm[0] else "Priority"

        summary = f"""═══════════════════════════════════════════════
         SIMULATION CONCLUSION & COMPARISON
═══════════════════════════════════════════════

► Priority Rule: Smaller number = Higher priority (Preemptive)
► Tie-breaking: 1) Priority/Remaining → 2) Arrival Time → 3) Process ID

───────────── METRIC COMPARISON ─────────────

  Q1: Which algorithm produced the lower average Waiting Time?
      • Priority Avg WT : {pm[0]:.2f} ms
      • SRTF Avg WT     : {sm[0]:.2f} ms
      ✓ Answer: {wt_winner}

  Q2: Which algorithm produced the lower average Response Time?
      • Priority Avg RT : {pm[2]:.2f} ms
      • SRTF Avg RT     : {sm[2]:.2f} ms
      ✓ Answer: {rt_winner}

  Q3: Did priority values improve treatment of urgent processes?
      ✓ YES — Priority Scheduling guarantees that processes with
        higher priority (lower number) are served first, regardless
        of burst time. This benefits urgent/critical tasks.

  Q4: Did SRTF favor short jobs more aggressively?
      ✓ YES — SRTF always preempts the running process when a
        shorter remaining job arrives, aggressively favoring short
        burst times over any other criterion.

  Q5: Which algorithm would you recommend?
      ✓ Overall winner: {overall} (based on lower Avg WT)
      • For time-sensitive urgent tasks → use Priority
      • For maximum CPU efficiency     → use SRTF

───────────── TRADE-OFF ANALYSIS ─────────────

  • FAIRNESS: Priority may starve low-priority processes
    indefinitely if high-priority jobs keep arriving.
  • STARVATION: SRTF may starve LONG jobs regardless of
    their importance or priority level.
  • KEY DIFFERENCE: Priority = policy-based service (by urgency)
                    SRTF = burst-time-based service (by efficiency)

═══════════════════════════════════════════════
"""
        text_summary.insert(tk.END, summary)
        
        # Calculate exactly how many lines are in the summary
        num_lines = summary.count('\n')
        # Update the height of the text box to fit the text perfectly without scrolling
        text_summary.config(height=num_lines, state="disabled")

    # --- 2. بناء الواجهة (UI) ---
    root = tk.Tk();
    root.title("CPU Scheduling Simulator - Black & Pink Premium");
    root.geometry("1150x900");
    root.configure(bg=color_bg)

    style = ttk.Style();
    style.theme_use('clam')
    style.configure("TNotebook", background=color_bg, borderwidth=0)
    style.configure("TNotebook.Tab", background=color_card, foreground=color_white, padding=[20, 8],
                    font=("Arial", 10, "bold"))
    style.map("TNotebook.Tab", background=[("selected", color_pink)], foreground=[("selected", "black")])
    style.configure("Treeview", background=color_card, foreground=color_white, fieldbackground=color_card, rowheight=25)
    style.configure("Treeview.Heading", background=color_pink, foreground="black", font=("Arial", 10, "bold"))

    notebook = ttk.Notebook(root)
    tab1, tab2 = tk.Frame(notebook, bg=color_bg), tk.Frame(notebook, bg=color_bg)
    notebook.add(tab1, text=" 1. CONFIGURATION ");
    notebook.add(tab2, text=" 2. ANALYSIS & RESULTS ")
    notebook.pack(expand=True, fill="both")

    # Tab 1
    input_f = tk.LabelFrame(tab1, text=" Add New Process ", bg=color_bg, fg=color_pink, font=("Arial", 11, "bold"),
                            padx=15, pady=15)
    input_f.pack(fill="x", padx=25, pady=20)
    lbls = ["Process ID:", "Arrival Time:", "Burst Time:", "Priority:"]
    vars = ["entry_pid", "entry_arrival", "entry_burst", "entry_priority"]
    for i, txt in enumerate(lbls):
        tk.Label(input_f, text=txt, bg=color_bg, fg=color_white, font=("Arial", 10)).grid(row=0, column=i * 2, padx=10)
        globals()[vars[i]] = tk.Entry(input_f, width=12, bg=color_input, fg=color_white, insertbackground=color_white,
                                      relief="flat", highlightthickness=1, highlightbackground=color_pink)
        globals()[vars[i]].grid(row=0, column=i * 2 + 1)
    tk.Button(input_f, text="+ Add Process", command=add_process, bg=color_pink, fg="black", font=("Arial", 10, "bold"),
              relief="flat", padx=15).grid(row=0, column=8, padx=25)
    tk.Label(input_f, text="★ Priority Rule: Lower Number = Higher Priority  |  Range: 0–10  |  Preemptive Mode",
             bg=color_bg, fg=color_pink, font=("Arial", 9, "italic")).grid(row=1, column=0, columnspan=9, pady=(8, 0))

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

    # أسماء الأعمدة كاملة
    tree_cols = ("Process ID", "Arrival Time", "Burst Time", "Priority")
    tree = ttk.Treeview(tab1, columns=tree_cols, show='headings', height=15)
    for c in tree_cols: tree.heading(c, text=c); tree.column(c, anchor="center")
    tree.pack(fill="both", expand=True, padx=25, pady=20)

    # Tab 2 - Scrollable Setup
    tab2_canvas = tk.Canvas(tab2, bg=color_bg, highlightthickness=0)
    tab2_scrollbar = ttk.Scrollbar(tab2, orient="vertical", command=tab2_canvas.yview)
    tab2_scrollable_frame = tk.Frame(tab2_canvas, bg=color_bg)

    tab2_scrollable_frame.bind("<Configure>", lambda e: tab2_canvas.configure(scrollregion=tab2_canvas.bbox("all")))
    tab2_canvas.create_window((0, 0), window=tab2_scrollable_frame, anchor="nw", tags="frame")
    tab2_canvas.bind("<Configure>", lambda e: tab2_canvas.itemconfig("frame", width=e.width))

    tab2_canvas.pack(side="left", fill="both", expand=True)
    tab2_scrollbar.pack(side="right", fill="y")
    tab2_canvas.configure(yscrollcommand=tab2_scrollbar.set)

    def _on_mousewheel(event):
        # Allow scrolling with mouse wheel when mouse is over tab 2
        try:
            tab2_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass
    tab2_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    gf = tk.LabelFrame(tab2_scrollable_frame, text=" Gantt Charts ", bg=color_bg, fg=color_pink, font=("Arial", 11, "bold"), padx=15,
                       pady=10)
    gf.pack(fill="x", padx=25, pady=10)
    for n, v in [("Priority Preemptive", "canvas_p"), ("SRTF Scheduling", "canvas_s")]:
        tk.Label(gf, text=n, bg=color_bg, fg=color_white, font=("Arial", 9, "italic")).pack(anchor="w", padx=15)
        globals()[v] = tk.Canvas(gf, height=85, bg="#181818", highlightthickness=1, highlightbackground=color_card);
        globals()[v].pack(fill="x", padx=15, pady=8)

    res_f = tk.Frame(tab2_scrollable_frame, bg=color_bg);
    res_f.pack(fill="x", padx=20)
    for name, tv, lb in [("Priority", "tree_res_p", "lbl_avg_p"), ("SRTF", "tree_res_s", "lbl_avg_s")]:
        f = tk.LabelFrame(res_f, text=f" {name} Metrics ", bg=color_bg, fg=color_pink, font=("Arial", 10, "bold"),
                          padx=10, pady=10);
        f.pack(side="left", expand=True, fill="both", padx=10)
        t = ttk.Treeview(f, columns=("ID", "WT", "TAT", "RT"), show='headings', height=6)
        for c in ("ID", "WT", "TAT", "RT"): t.heading(c, text=c); t.column(c, width=65, anchor="center")
        t.pack(fill="both");
        l = tk.Label(f, text="Avg -> WT: 0, TAT: 0, RT: 0", bg=color_bg, fg=color_pink, font=("Arial", 10, "bold"));
        l.pack(pady=8)
        if name == "Priority":
            tree_res_p, lbl_avg_p = t, l
        else:
            tree_res_s, lbl_avg_s = t, l

    summary_f = tk.LabelFrame(tab2_scrollable_frame, text=" Conclusion & Tie-break Summary ", bg=color_bg, fg=color_pink,
                              font=("Arial", 11, "bold"), padx=15, pady=10)
    summary_f.pack(fill="both", expand=True, padx=25, pady=15)
    text_summary = tk.Text(summary_f, height=8, bg="#181818", fg=color_white, relief="flat", font=("Courier New", 10),
                           padx=15, pady=15)
    text_summary.pack(fill="both", expand=True);
    text_summary.config(state="disabled")

    root.mainloop()