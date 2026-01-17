from flask import Blueprint

gap_analysis_bp = Blueprint('gap_analysis', __name__)

@gap_analysis_bp.route('/gap-analysis')
def gap_analysis():
    return "Gap Analysis Endpoint"