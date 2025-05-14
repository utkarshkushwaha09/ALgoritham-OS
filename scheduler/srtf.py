# scheduler/sjf_preemptive.py

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.starting_time = -1
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0

def srtf(processes):
    n = len(processes)
    current_time = 0
    completed = 0
    is_completed = [False] * n
    schedule = []  # Gantt chart data (process IDs at each time unit)

    while completed != n:
        idx = -1
        min_remaining = float('inf')
        for i in range(n):
            if (processes[i].arrival_time <= current_time and
                not is_completed[i] and
                processes[i].remaining_time < min_remaining):
                min_remaining = processes[i].remaining_time
                idx = i
            elif (processes[i].arrival_time <= current_time and
                  not is_completed[i] and
                  processes[i].remaining_time == min_remaining):
                if processes[i].arrival_time < processes[idx].arrival_time:
                    idx = i

        if idx != -1:
            if processes[idx].starting_time == -1:
                processes[idx].starting_time = current_time

            processes[idx].remaining_time -= 1
            schedule.append(processes[idx].pid)  # record execution
            current_time += 1

            if processes[idx].remaining_time == 0:
                processes[idx].completion_time = current_time
                processes[idx].turnaround_time = processes[idx].completion_time - processes[idx].arrival_time
                processes[idx].waiting_time = processes[idx].turnaround_time - processes[idx].burst_time
                processes[idx].response_time = processes[idx].starting_time - processes[idx].arrival_time
                is_completed[idx] = True
                completed += 1
        else:
            schedule.append('idle')  # system is idle
            current_time += 1

    return processes, schedule


def calculate_averages(processes):
    n = len(processes)
    total_tat = sum(p.turnaround_time for p in processes)
    total_wt = sum(p.waiting_time for p in processes)
    total_rt = sum(p.response_time for p in processes)
    return {
        'avg_tat': round(total_tat / n, 2),
        'avg_wt': round(total_wt / n, 2),
        'avg_rt': round(total_rt / n, 2)
    }