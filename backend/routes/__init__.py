from flask import Blueprint

# Create a Blueprint for API routes
api = Blueprint('api', __name__)

# Import individual route modules
from .skills import skills_bp
from .gap_analysis import gap_analysis_bp
from .roadmap import roadmap_bp

# Register Blueprints
api.register_blueprint(skills_bp, url_prefix='/skills')
api.register_blueprint(gap_analysis_bp, url_prefix='/gap-analysis')
api.register_blueprint(roadmap_bp, url_prefix='/roadmap')
