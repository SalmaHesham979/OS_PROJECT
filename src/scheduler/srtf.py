def run_srtf(processes):
    n = len(processes)
    current_time = 0
    completed = 0
    gantt_chart = []

    for p in processes:
        p.remaining_time = p.burst_time
        p.start_time = -1
        p.completion_time = 0

    while completed != n:

        available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]

        if not available:
            current_time += 1
            continue

        
        current_p = min(available, key=lambda x: (x.remaining_time, x.arrival_time, x.pid))

        if current_p.start_time == -1:
            current_p.start_time = current_time

        if not gantt_chart or gantt_chart[-1][0] != current_p.pid:
            gantt_chart.append([current_p.pid, current_time, current_time + 1])
        else:
            gantt_chart[-1][2] = current_time + 1

        current_p.remaining_time -= 1
        current_time += 1

        if current_p.remaining_time == 0:
            completed += 1
            current_p.completion_time = current_time
            current_p.turnaround_time = current_p.completion_time - current_p.arrival_time
            current_p.waiting_time = current_p.turnaround_time - current_p.burst_time
            current_p.response_time = current_p.start_time - current_p.arrival_time

    return gantt_chart