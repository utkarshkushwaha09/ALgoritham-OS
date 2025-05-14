from app.home.home import home_bp
from app.cpu_scheduling.fcfs import fcfs_bp
from app.cpu_scheduling.srtf import srtf_bp
from app.simulate.simulate import simulate_bp
#from app.simulate.simulate_page import simulate_page_bp

def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(simulate_bp)
    #app.register_blueprint(simulate_page_bp)
    app.register_blueprint(fcfs_bp)
    app.register_blueprint(srtf_bp)
