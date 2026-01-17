from flask import Blueprint, jsonify, request

roadmap_bp = Blueprint('roadmap', __name__)

# Mock data for roadmap generation
roadmap_phases = [
    {"phase": 1, "name": "Learn Python Basics", "duration": "2 weeks"},
    {"phase": 2, "name": "Practice Data Analysis", "duration": "3 weeks"},
    {"phase": 3, "name": "Explore Machine Learning", "duration": "4 weeks"}
]

# Get learning roadmap
@roadmap_bp.route('/', methods=['GET'])
def get_roadmap():
    return jsonify(roadmap_phases)