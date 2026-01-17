from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

# ========================================
# USER MANAGEMENT
# ========================================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    current_role = db.Column(db.String(100))
    target_sector = db.Column(db.String(50))  # Healthcare, Agriculture, Urban
    target_role_id = db.Column(db.Integer, db.ForeignKey('predefined_roles.id'))
    resume_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('UserSkill', back_populates='user', cascade='all, delete-orphan')
    courses = db.relationship('UserCourse', back_populates='user', cascade='all, delete-orphan')
    projects = db.relationship('UserProject', back_populates='user', cascade='all, delete-orphan')
    achievements = db.relationship('UserAchievement', back_populates='user', cascade='all, delete-orphan')
    gap_analyses = db.relationship('SkillGap', back_populates='user', cascade='all, delete-orphan')
    roadmaps = db.relationship('LearningRoadmap', back_populates='user', cascade='all, delete-orphan')
    target_role = db.relationship('PredefinedRole', foreign_keys=[target_role_id])
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'current_role': self.current_role,
            'target_sector': self.target_sector,
            'target_role': self.target_role.role_title if self.target_role else None,
            'created_at': self.created_at.isoformat()
        }


# ========================================
# USER PROFILE DATA
# ========================================

class UserSkill(db.Model):
    __tablename__ = 'user_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # Technical, Soft, Domain
    proficiency_percentage = db.Column(db.Integer, default=0)  # 0-100 (manual update by user)
    confidence_score = db.Column(db.Float)  # 0.0 to 1.0 (from resume extraction)
    source = db.Column(db.String(50))  # Manual, Resume, GitHub
    sector_context = db.Column(db.String(50))  # Healthcare, Agriculture, Urban, General
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='skills')
    
    def to_dict(self):
        return {
            'name': self.skill_name,
            'confidence': self.confidence_score,
            'proficiency_percentage': self.proficiency_percentage,
            'category': self.category,
            'sector_context': self.sector_context,
            'source': self.source
        }


class UserCourse(db.Model):
    __tablename__ = 'user_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_title = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(50))
    completion_status = db.Column(db.String(20))  # Completed, In-Progress, Planned
    completion_date = db.Column(db.Date)
    certificate_url = db.Column(db.String(255))
    skills_gained = db.Column(db.Text)  # JSON array
    course_url = db.Column(db.String(255))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='courses')
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_title': self.course_title,
            'platform': self.platform,
            'completion_status': self.completion_status,
            'skills_gained': json.loads(self.skills_gained) if self.skills_gained else []
        }


class UserProject(db.Model):
    __tablename__ = 'user_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technologies_used = db.Column(db.Text)  # JSON array
    project_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    sector_relevance = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    is_ongoing = db.Column(db.Boolean, default=False)
    skills_demonstrated = db.Column(db.Text)  # JSON array
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='projects')
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_title': self.project_title,
            'description': self.description,
            'technologies_used': json.loads(self.technologies_used) if self.technologies_used else [],
            'github_url': self.github_url,
            'sector_relevance': self.sector_relevance
        }


class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_title = db.Column(db.String(200), nullable=False)
    achievement_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    issuing_organization = db.Column(db.String(100))
    achievement_date = db.Column(db.Date)
    verification_url = db.Column(db.String(255))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='achievements')


# ========================================
# PREDEFINED ROLES (DROPDOWN)
# ========================================

class PredefinedRole(db.Model):
    __tablename__ = 'predefined_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    sector = db.Column(db.String(50), nullable=False, index=True)
    role_title = db.Column(db.String(100), nullable=False)
    experience_level = db.Column(db.String(20))  # Entry, Mid, Senior
    required_skills = db.Column(db.Text, nullable=False)  # JSON array
    
    def to_dict(self):
        return {
            'id': self.id,
            'sector': self.sector,
            'role_title': self.role_title,
            'experience_level': self.experience_level,
            'required_skills': json.loads(self.required_skills) if self.required_skills else []
        }


# ========================================
# RECOMMENDATION ENGINE DATA
# ========================================

class RecommendedCourse(db.Model):
    __tablename__ = 'recommended_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(200), nullable=False, index=True)
    platform = db.Column(db.String(50), nullable=False)
    course_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    duration_hours = db.Column(db.Integer)
    difficulty_level = db.Column(db.String(20))
    target_skills = db.Column(db.Text, nullable=False)  # JSON array
    sector = db.Column(db.String(50), index=True)
    is_free = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float)
    thumbnail_url = db.Column(db.String(255))
    instructor = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'platform': self.platform,
            'title': self.course_title,
            'url': self.course_url,
            'description': self.description,
            'duration_hours': self.duration_hours,
            'difficulty': self.difficulty_level,
            'target_skills': json.loads(self.target_skills) if self.target_skills else [],
            'is_free': self.is_free,
            'rating': self.rating
        }


class RecommendedProject(db.Model):
    __tablename__ = 'recommended_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    project_title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    difficulty_level = db.Column(db.String(20))
    estimated_duration_days = db.Column(db.Integer)
    target_skills = db.Column(db.Text, nullable=False)  # JSON array
    sector = db.Column(db.String(50), index=True)
    project_type = db.Column(db.String(50))
    resources = db.Column(db.Text)  # JSON array
    dataset_links = db.Column(db.Text)  # JSON array
    github_example = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ========================================
# ROADMAP PHASES
# ========================================

class RoadmapPhase(db.Model):
    __tablename__ = 'roadmap_phases'
    
    id = db.Column(db.Integer, primary_key=True)
    phase_name = db.Column(db.String(50), nullable=False, unique=True)
    sequence_order = db.Column(db.Integer, nullable=False)
    duration_weeks = db.Column(db.Integer)
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'phase': self.phase_name.lower(),
            'sequence': self.sequence_order,
            'duration_weeks': self.duration_weeks,
            'description': self.description
        }


# ========================================
# SKILL INTELLIGENCE
# ========================================

class SkillGap(db.Model):
    __tablename__ = 'skill_gaps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_role_id = db.Column(db.Integer, db.ForeignKey('predefined_roles.id'))
    missing_skills = db.Column(db.Text)  # JSON array
    weak_skills = db.Column(db.Text)  # JSON array
    readiness_percentage = db.Column(db.Float)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='gap_analyses')
    target_role = db.relationship('PredefinedRole')
    
    def to_dict(self):
        return {
            'missing_skills': json.loads(self.missing_skills) if self.missing_skills else [],
            'weak_skills': json.loads(self.weak_skills) if self.weak_skills else [],
            'readiness_percentage': self.readiness_percentage,
            'analysis_date': self.analysis_date.isoformat()
        }


class LearningRoadmap(db.Model):
    __tablename__ = 'learning_roadmaps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    gap_analysis_id = db.Column(db.Integer, db.ForeignKey('skill_gaps.id'))
    roadmap_items = db.Column(db.Text, nullable=False)  # JSON array matching output format
    estimated_completion_months = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active')
    
    user = db.relationship('User', back_populates='roadmaps')
    gap_analysis = db.relationship('SkillGap')
    
    def to_dict(self):
        return {
            'roadmap': json.loads(self.roadmap_items) if self.roadmap_items else [],
            'estimated_months': self.estimated_completion_months,
            'status': self.status
        }
