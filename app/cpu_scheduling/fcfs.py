from flask import Blueprint, request, jsonify
import scheduler.fcfs as fcfs_module    

fcfs_bp = Blueprint('fcfs', __name__)
@fcfs_bp.route('/simulate/fcfs', methods=['GET', 'POST'])
def fcfs():
    print("FCFS POST request received")
    #return []
    input_processes = request.json["processes"]
    
    processes = [fcfs_module.Process(p["pid"], int(p["at"]), int(p["bt"])) for p in input_processes]
    
    scheduled_processes = fcfs_module.fcfs(processes)
    
    averages = fcfs_module.calculate_averages(scheduled_processes)

    table = [{
        "pid": p.pid,
        "arrival_time": p.arrival_time,
        "burst_time": p.burst_time,
        "starting_time": p.starting_time,
        "completion_time": p.completion_time,
        "waiting_time": p.waiting_time,
        "turnaround_time": p.turnaround_time,
        "response_time": p.response_time
    } for p in scheduled_processes]

    return jsonify({
        "scheduled": [
            {
                "pid": p.pid,
                "starting_time": p.starting_time,
                "completion_time": p.completion_time,
                "duration": p.completion_time - p.starting_time
            }
            for p in scheduled_processes
        ],
        "table": table,
        "average_waiting_time": averages['avg_wt'],
        "average_turnaround_time": averages['avg_tat'],
        "average_response_time": averages['avg_rt']
    })