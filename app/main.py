# app/main.py
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import json

load_dotenv()
logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

# Import crew and models
try:
    from app.crew import ProjectPlanningCrew
    CREW_AVAILABLE = True
    logger.info("✅ ProjectPlanningCrew imported successfully")
except ImportError as e:
    logger.warning(f"⚠️ Crew not available: {e}")
    CREW_AVAILABLE = False

try:
    from app.models import ProjectPlan
    MODELS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ Models not available: {e}")
    MODELS_AVAILABLE = False

@main_bp.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@main_bp.route('/api/plan', methods=['POST'])
def create_plan():
    """Create a project plan"""
    try:
        data = request.json
        
        # Validate input
        required_fields = ['project_type', 'project_objectives']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'error'
                }), 400
        
        # Prepare project data
        project_data = {
            'project_type': data.get('project_type', 'Website'),
            'project_objectives': data.get('project_objectives', ''),
            'industry': data.get('industry', 'Technology'),
            'team_members': data.get('team_members', ''),
            'project_requirements': data.get('project_requirements', '')
        }
        
        # Create plan using CrewAI
        if not CREW_AVAILABLE:
            return jsonify({
                'error': 'CrewAI not available. Please check installation.',
                'status': 'error'
            }), 500
        
        crew = ProjectPlanningCrew()
        result = crew.create_plan(project_data)
        
        if result['status'] == 'error':
            return jsonify({
                'error': result.get('error', 'Unknown error'),
                'status': 'error'
            }), 500
        
        return jsonify({
            'status': 'success',
            'result': result,
            'message': 'Project plan created successfully!'
        })
        
    except Exception as e:
        logger.error(f"Error creating plan: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@main_bp.route('/api/progress-report', methods=['POST'])
def generate_progress_report():
    """Generate a project progress report"""
    try:
        if not CREW_AVAILABLE:
            return jsonify({
                'error': 'CrewAI not available. Please check installation.',
                'status': 'error'
            }), 500
        
        crew = ProjectPlanningCrew()
        result = crew.generate_progress_report()
        
        if result['status'] == 'error':
            return jsonify({
                'error': result.get('error', 'Unknown error'),
                'status': 'error'
            }), 500
        
        return jsonify({
            'status': 'success',
            'result': result,
            'message': 'Progress report generated successfully!'
        })
        
    except Exception as e:
        logger.error(f"Error generating progress report: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@main_bp.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    try:
        from app.model_manager import model_manager
        results = model_manager.test_providers()
        available = [m for m, v in results.items() if v]
        
        return jsonify({
            'status': 'success',
            'models': {
                'primary': os.getenv('OPENROUTER_PRIMARY_MODEL', 'openai/gpt-4o-mini'),
                'fallbacks': os.getenv('OPENROUTER_FALLBACK_MODELS', '').split(','),
                'available': available,
                'all_tested': results
            }
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@main_bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'crew_available': CREW_AVAILABLE,
        'models_available': MODELS_AVAILABLE,
        'version': '2.0.0',
        'features': ['planning', 'estimation', 'allocation', 'progress-report']
    })