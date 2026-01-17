from flask import Blueprint, request, jsonify
from typing import Optional, List
import json
from app.models.schemas import Skill
from app.services.resume_analysis.extractor import extract_text
from app.services.resume_analysis.normalizer import normalize_text
from app.services.resume_analysis.skill_extractor import extract_skills
from app.services.resume_analysis.scorer import score_skills
from app.services.resume_analysis.roadmap import generate_roadmap
from app.services.resume_analysis.course_mapper import map_courses_to_skills

bp = Blueprint("resume", __name__)

@bp.route("/extract", methods=["POST"])
def extract_skills_only():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "No file provided"}), 400
    
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        return jsonify({"error": "File must be PDF or DOCX"}), 400
    
    content = file.read()
    
    raw_text = extract_text(content, file.filename)
    normalized_text = normalize_text(raw_text)
    skills_list = extract_skills(normalized_text, raw_text)
    
    return jsonify({
        "extracted_skills": skills_list
    })

@bp.route("/analyze", methods=["POST"])
def analyze_resume():
    target_role = request.form.get("target_role")
    if not target_role:
        return jsonify({"error": "target_role is required"}), 400
    
    skills_with_scores = request.form.get("skills_with_scores")
    if not skills_with_scores:
        return jsonify({"error": "skills_with_scores is required. Please provide skills with confidence scores."}), 400
    
    try:
        skills_data = json.loads(skills_with_scores)
        if not isinstance(skills_data, list):
            return jsonify({"error": "skills_with_scores must be a JSON array"}), 400
        
        final_skills = []
        for item in skills_data:
            if isinstance(item, dict) and "name" in item and "confidence" in item:
                skill_name = item["name"].strip()
                confidence = float(item["confidence"])
                if 0.0 <= confidence <= 1.0:
                    final_skills.append({
                        "name": skill_name,
                        "confidence": confidence
                    })
        
        if not final_skills:
            return jsonify({"error": "No valid skills provided"}), 400
        
        final_skills.sort(key=lambda x: x["confidence"], reverse=True)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in skills_with_scores"}), 400
    except Exception as e:
        return jsonify({"error": f"Error processing skills: {str(e)}"}), 400
    
    roadmap_phases = generate_roadmap(
        [Skill(name=s["name"], confidence=s["confidence"]) for s in final_skills],
        target_role
    )
    roadmap_with_courses = map_courses_to_skills(roadmap_phases)
    
    roadmap_response = []
    for phase in roadmap_with_courses:
        roadmap_response.append({
            "phase": phase.phase,
            "skills": [
                {
                    "name": skill.name,
                    "courses": [
                        {
                            "platform": course.platform,
                            "title": course.title,
                            "url": course.url
                        }
                        for course in skill.courses
                    ]
                }
                for skill in phase.skills
            ]
        })
    
    return jsonify({
        "skills": final_skills,
        "roadmap": roadmap_response
    })
