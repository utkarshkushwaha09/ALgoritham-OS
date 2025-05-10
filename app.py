from flask import Flask, render_template, request, jsonify,redirect, url_for
from scheduler.fcfs import Process, fcfs, calculate_averages

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/simulate', methods=['POST'])
def simulate():
    selected_algo = request.form['algorithm']
    return redirect(url_for('simulation_page', algorithm=selected_algo))


@app.route("/simulate/<algorithm>")
def simulation_page(algorithm):

    if algorithm == "fcfs":
        return render_template("fcfs.html", algorithm=algorithm)
    return f"Algorithm {algorithm.upper()} is not yet supported.", 404
    
@app.route("/simulate/fcfs", methods=["POST"])
def run_simulate():

    input_processes = request.json["processes"]
    
    processes = [Process(p["pid"], int(p["at"]), int(p["bt"])) for p in input_processes]
    
    scheduled_processes = fcfs(processes)
    
    averages = calculate_averages(scheduled_processes)

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

if __name__ == "__main__":
    app.run(debug=True)
