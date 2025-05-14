from flask import Flask
from app import register_blueprints  # importing from routes/__init__.py

app = Flask(__name__)
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)