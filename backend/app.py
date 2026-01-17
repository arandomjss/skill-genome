import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from app.routes import api

app = Flask(__name__)

# Register the API Blueprint
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def home():
    return "Welcome to the Skill Intelligence Platform!"

if __name__ == '__main__':
    app.run(debug=True)