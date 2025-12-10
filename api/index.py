"""
Vercel Serverless Function Entry Point
Optimized for Vercel's 250 MB limit
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import only lightweight routes
try:
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.reading_routes import reading_bp
    from routes.subscription_routes import subscription_bp
    logger.info("Successfully imported core routes")
except ImportError as e:
    logger.error(f"Could not import routes: {e}")
    auth_bp = user_bp = reading_bp = subscription_bp = None

# Try to import astrology routes (may fail if pyswisseph not available)
try:
    from routes.astrology_routes import astrology_bp
    ASTROLOGY_AVAILABLE = True
    logger.info("Astrology features enabled")
except ImportError as e:
    logger.warning(f"Astrology features disabled: {e}")
    astrology_bp = None
    ASTROLOGY_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__, static_folder=parent_dir, static_url_path='')
app.config.from_object(Config)

# Initialize CORS with proper configuration
CORS(app, 
     origins=Config.CORS_ORIGINS, 
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Initialize database (lightweight - SQLite or PostgreSQL)
try:
    from src.models import db
    from src.auth import init_jwt
    
    db.init_app(app)
    init_jwt(app)
    
    # Create tables if needed (only on first request)
    @app.before_request
    def initialize_database():
        if not hasattr(app, '_database_initialized'):
            try:
                with app.app_context():
                    db.create_all()
                    app._database_initialized = True
                    logger.info("Database initialized successfully")
            except Exception as e:
                logger.error(f"Database initialization error: {e}")
                app._database_initialized = False
    
    logger.info("Database configuration loaded")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")

# Register blueprints
if auth_bp:
    app.register_blueprint(auth_bp)
    logger.info("Registered auth blueprint")
if user_bp:
    app.register_blueprint(user_bp)
    logger.info("Registered user blueprint")
if reading_bp:
    app.register_blueprint(reading_bp)
    logger.info("Registered reading blueprint")
if subscription_bp:
    app.register_blueprint(subscription_bp)
    logger.info("Registered subscription blueprint")
if astrology_bp and ASTROLOGY_AVAILABLE:
    app.register_blueprint(astrology_bp)
    logger.info("Registered astrology blueprint")

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Tarot API',
        'version': '1.0.0',
        'platform': 'Vercel',
        'features': {
            'auth': auth_bp is not None,
            'readings': reading_bp is not None,
            'subscriptions': subscription_bp is not None,
            'astrology': ASTROLOGY_AVAILABLE
        }
    }), 200

@app.route('/api/info', methods=['GET'])
def api_info():
    """Información de la API"""
    endpoints = {
        'auth': '/api/auth/*',
        'user': '/api/user/*',
        'readings': '/api/readings/*',
        'subscription': '/api/subscription/*'
    }
    
    features = [
        'Autenticación JWT',
        'Sistema Freemium',
        'Persistencia de temas',
        'Gestión de lecturas',
        'Suscripciones'
    ]
    
    if ASTROLOGY_AVAILABLE:
        endpoints['astrology'] = '/api/astrology/*'
        features.extend([
            'Cálculos astrológicos precisos',
            'Cartas Natales Astrológicas',
            'Sistemas de Casas',
            'Aspectos Planetarios',
            'Interpretaciones con IA (Gemini)'
        ])
    else:
        features.append('Astrology: Disabled (heavy dependencies removed for Vercel)')
    
    return jsonify({
        'name': 'Tarot Místico API',
        'version': '1.0.0',
        'platform': 'Vercel Serverless',
        'endpoints': endpoints,
        'features': features
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    try:
        db.session.rollback()
    except:
        pass
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Acceso prohibido'}), 403

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'No autorizado'}), 401

# Request logging middleware
@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path} - {request.remote_addr}")

@app.after_request
def log_response(response):
    logger.info(f"{request.method} {request.path} - {response.status_code}")
    return response

# Vercel serverless function handler - CRITICAL: This must be named 'app' for Vercel
# The Flask app instance is automatically used by Vercel's Python runtime

# For local testing
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting development server on port {port}")
    app.run(debug=True, host='0.0.0.0', port=port)
