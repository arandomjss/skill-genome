from flask import Blueprint, jsonify, request

gap_analysis_bp = Blueprint('gap_analysis', __name__)

# Mock data for user skills and required skills
user_skills = ["Python", "Data Analysis"]
required_skills = ["Python", "Machine Learning", "Data Visualization"]

# Analyze skill gaps
@gap_analysis_bp.route('/', methods=['GET'])
def analyze_gaps():
    gaps = [skill for skill in required_skills if skill not in user_skills]
    return jsonify({"gaps": gaps})