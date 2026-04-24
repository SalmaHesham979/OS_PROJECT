def run_priority_preemptive(processes):
    # 1. تجهيز البيانات
    n = len(processes)
    current_time = 0
    completed = 0
    gantt_chart = []  # هنسجل فيه (الاسم، وقت البداية، وقت النهاية)

    # تصفير المواعيد عشان لو هنعمل Run كذا مرة
    for p in processes:
        p.remaining_time = p.burst_time
        p.start_time = -1
        p.completion_time = 0

    while completed != n:
        # 2. هات العمليات اللي وصلت دلوقتي ولسه مخلصتش
        available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]

        if not available:
            current_time += 1
            continue

        # 3. اختار صاحب أعلى أولوية (أقل رقم)
        # ولو تساووا، اختار اللي وصل الأول (Tie-breaking)
        current_p = min(available, key=lambda x: (x.priority, x.arrival_time, x.pid))

        # 4. سجل أول مرة دخل فيها الـ CPU عشان الـ Response Time
        if current_p.start_time == -1:
            current_p.start_time = current_time

        # 5. شغل العملية لمدة ثانية واحدة
        # سجل في الـ Gantt Chart
        if not gantt_chart or gantt_chart[-1][0] != current_p.pid:
            gantt_chart.append([current_p.pid, current_time, current_time + 1])
        else:
            gantt_chart[-1][2] = current_time + 1  # طول المدة لو نفس العملية لسه شغالة

        current_p.remaining_time -= 1
        current_time += 1

        # 6. لو خلصت، احسب النتايج
        if current_p.remaining_time == 0:
            completed += 1
            current_p.completion_time = current_time
            # المعادلات اللي في ورقتك:
            current_p.turnaround_time = current_p.completion_time - current_p.arrival_time
            current_p.waiting_time = current_p.turnaround_time - current_p.burst_time
            current_p.response_time = current_p.start_time - current_p.arrival_time

    return gantt_chart