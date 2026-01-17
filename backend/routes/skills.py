from flask import Blueprint, jsonify, request

skills_bp = Blueprint('skills', __name__)

# Mock data for skills
skills = [
    {"id": 1, "name": "Python", "importance": 5},
    {"id": 2, "name": "Data Analysis", "importance": 4}
]

# Get all skills
@skills_bp.route('/', methods=['GET'])
def get_skills():
    return jsonify(skills)

# Add a new skill
@skills_bp.route('/', methods=['POST'])
def add_skill():
    new_skill = request.json
    new_skill['id'] = len(skills) + 1
    skills.append(new_skill)
    return jsonify(new_skill), 201

# Update a skill
@skills_bp.route('/<int:skill_id>', methods=['PUT'])
def update_skill(skill_id):
    skill = next((s for s in skills if s['id'] == skill_id), None)
    if not skill:
        return jsonify({"error": "Skill not found"}), 404
    skill.update(request.json)
    return jsonify(skill)

# Delete a skill
@skills_bp.route('/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    global skills
    skills = [s for s in skills if s['id'] != skill_id]
    return '', 204