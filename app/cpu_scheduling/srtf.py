from flask import Blueprint, render_template,request,jsonify
import scheduler.srtf as srtf_module

srtf_bp = Blueprint('srtf', __name__)

@srtf_bp.route('/simulate/srtf', methods=['GET', 'POST'])
def srtf():
    #return []
    input_processes = request.json["processes"]

    processes = [srtf_module.Process(p["pid"], int(p["at"]), int(p["bt"])) for p in input_processes]

    # Run the SJF algorithm and get both updated processes and Gantt chart
    scheduled_processes, gantt_chart = srtf_module.srtf(processes)

    averages = srtf_module.calculate_averages(scheduled_processes)

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

    print("SJF simulation completed")
    print("Gantt chart:", gantt_chart)
    print("Averages:", averages)

    return jsonify({
        "scheduled": gantt_chart,
        "table": table,
        "average_waiting_time": averages['avg_wt'],
        "average_turnaround_time": averages['avg_tat'],
        "average_response_time": averages['avg_rt']
    })
