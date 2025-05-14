from flask import Blueprint, request, render_template

simulate_bp = Blueprint('simulate', __name__)

@simulate_bp.route('/simulate', methods=['POST'])
def simulate():
    algorithm = request.form.get('algorithm')
    if algorithm == "fcfs":
        return render_template("fcfs.html", algorithm=algorithm)
    elif algorithm == "srtf":
        return render_template("srtf.html", algorithm=algorithm)
    return f"Algorithm {algorithm.upper()} is not yet supported.", 404
