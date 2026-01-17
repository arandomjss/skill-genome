import json
import os
from typing import List, Dict
from app.models.schemas import RoadmapPhase, RoadmapSkill, Course

def _load_courses() -> Dict:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    courses_path = os.path.join(current_dir, "courses.json")
    with open(courses_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def map_courses_to_skills(roadmap_phases: List[RoadmapPhase]) -> List[RoadmapPhase]:
    courses_data = _load_courses()
    
    for phase in roadmap_phases:
        for skill in phase.skills:
            skill_lower = skill.name.lower()
            if skill_lower in courses_data:
                course_list = courses_data[skill_lower]
                skill.courses = [
                    Course(platform=course["platform"], title=course["title"], url=course["url"])
                    for course in course_list
                ]
            else:
                for key, course_list in courses_data.items():
                    if key in skill_lower or skill_lower in key:
                        skill.courses = [
                            Course(platform=course["platform"], title=course["title"], url=course["url"])
                            for course in course_list
                        ]
                        break
    
    return roadmap_phases
