from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from utils.database import db
from utils.validators import (
    validate_user_data, validate_reflection_data, 
    validate_journey_duration, validate_task_window,
    generate_user_id, format_response
)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Set secret key
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    
    return app

app = create_app()

# Import routes after app creation
from controllers.user_controller import user_bp
from controllers.task_controller import task_bp
from controllers.reflection_controller import reflection_bp

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(task_bp, url_prefix='/api/tasks')
app.register_blueprint(reflection_bp, url_prefix='/api/reflections')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return format_response(True, "ClearNext Backend is running", {
        'version': '1.0.0',
        'database': 'mock' if Config.USE_MOCK_DB else 'mongodb',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return format_response(False, "Endpoint not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return format_response(False, "Internal server error"), 500

if __name__ == '__main__':
    # Check for mock flag
    if '--mock' in sys.argv:
        os.environ['USE_MOCK_DB'] = 'true'
        print("📝 Using mock database")
    
    print("🚀 Starting ClearNext Backend...")
    print(f"📊 Database: {'Mock (In-Memory)' if Config.USE_MOCK_DB else 'MongoDB'}")
    print(f"🌐 Server: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
