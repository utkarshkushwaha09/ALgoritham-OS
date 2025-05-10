# scheduler/fcfs.py

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.starting_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0

def fcfs(processes):
    current_time = 0
    print("Processes before sorting:", processes)
    processes.sort(key=lambda p: p.arrival_time)

    for process in processes:
        print(f"Processing {process.pid}: Arrival Time: {process.arrival_time}, Burst Time: {process.burst_time}")
        if process.arrival_time > current_time:
            current_time = process.arrival_time

        process.starting_time = current_time
        current_time += process.burst_time
        process.completion_time = current_time

        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        process.response_time = process.starting_time - process.arrival_time

    return processes

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
