"""
Tarot Místico - Vercel Serverless API
Clean, scalable, production-ready implementation
"""
import sys
import os
from pathlib import Path

# Add parent directory to Python path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder=parent_dir, static_url_path='')
app.config.from_object(Config)

# Configure CORS
CORS(app, 
     origins=Config.CORS_ORIGINS, 
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Import and initialize database
try:
    from src.models import db
    from src.auth import init_jwt
    
    db.init_app(app)
    init_jwt(app)
    
    @app.before_request
    def initialize_database():
        """Initialize database on first request"""
        if not hasattr(app, '_db_initialized'):
            try:
                with app.app_context():
                    db.create_all()
                    app._db_initialized = True
                    logger.info("✅ Database initialized")
            except Exception as e:
                logger.error(f"❌ Database initialization failed: {e}")
                app._db_initialized = False
    
    logger.info("✅ Database configuration loaded")
except Exception as e:
    logger.error(f"❌ Database setup failed: {e}")

# Import routes
ROUTES_LOADED = {}

try:
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    ROUTES_LOADED['auth'] = True
    logger.info("✅ Auth routes loaded")
except ImportError as e:
    ROUTES_LOADED['auth'] = False
    logger.warning(f"⚠️  Auth routes not loaded: {e}")

try:
    from routes.user_routes import user_bp
    app.register_blueprint(user_bp)
    ROUTES_LOADED['user'] = True
    logger.info("✅ User routes loaded")
except ImportError as e:
    ROUTES_LOADED['user'] = False
    logger.warning(f"⚠️  User routes not loaded: {e}")

try:
    from routes.reading_routes import reading_bp
    app.register_blueprint(reading_bp)
    ROUTES_LOADED['reading'] = True
    logger.info("✅ Reading routes loaded")
except ImportError as e:
    ROUTES_LOADED['reading'] = False
    logger.warning(f"⚠️  Reading routes not loaded: {e}")

try:
    from routes.subscription_routes import subscription_bp
    app.register_blueprint(subscription_bp)
    ROUTES_LOADED['subscription'] = True
    logger.info("✅ Subscription routes loaded")
except ImportError as e:
    ROUTES_LOADED['subscription'] = False
    logger.warning(f"⚠️  Subscription routes not loaded: {e}")

try:
    from routes.astrology_routes import astrology_bp
    app.register_blueprint(astrology_bp)
    ROUTES_LOADED['astrology'] = True
    logger.info("✅ Astrology routes loaded")
except ImportError as e:
    ROUTES_LOADED['astrology'] = False
    logger.warning(f"⚠️  Astrology routes not loaded (optional): {e}")

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Tarot Místico API',
        'version': '2.0.0',
        'platform': 'Vercel Serverless',
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'routes': ROUTES_LOADED
    }), 200

@app.route('/api/info', methods=['GET'])
def api_info():
    """API information endpoint"""
    endpoints = {}
    features = []
    
    if ROUTES_LOADED.get('auth'):
        endpoints['auth'] = '/api/auth/*'
        features.append('JWT Authentication')
    
    if ROUTES_LOADED.get('user'):
        endpoints['user'] = '/api/user/*'
        features.append('User Management')
    
    if ROUTES_LOADED.get('reading'):
        endpoints['readings'] = '/api/readings/*'
        features.extend([
            'Tarot Card Readings',
            'Multiple Spread Types',
            'Reading History',
            'AI Interpretations (Gemini)'
        ])
    
    if ROUTES_LOADED.get('subscription'):
        endpoints['subscription'] = '/api/subscription/*'
        features.extend([
            'Freemium System',
            'Subscription Management',
            'Usage Tracking'
        ])
    
    if ROUTES_LOADED.get('astrology'):
        endpoints['astrology'] = '/api/astrology/*'
        features.extend([
            'Birth Chart Calculations',
            'Planetary Positions',
            'House Systems',
            'Astrological Aspects'
        ])
    
    return jsonify({
        'name': 'Tarot Místico API',
        'version': '2.0.0',
        'platform': 'Vercel Serverless',
        'endpoints': endpoints,
        'features': features,
        'documentation': 'https://github.com/yourusername/tarot-mistico'
    }), 200

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle bad request errors"""
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(401)
def unauthorized(error):
    """Handle unauthorized errors"""
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@app.errorhandler(403)
def forbidden(error):
    """Handle forbidden errors"""
    return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403

@app.errorhandler(404)
def not_found(error):
    """Handle not found errors"""
    return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {error}")
    try:
        db.session.rollback()
    except:
        pass
    return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500

# Request/Response logging middleware
@app.before_request
def log_request():
    """Log incoming requests"""
    logger.info(f"→ {request.method} {request.path} from {request.remote_addr}")

@app.after_request
def log_response(response):
    """Log outgoing responses"""
    logger.info(f"← {request.method} {request.path} → {response.status_code}")
    return response

# CORS preflight handler
@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    """Handle CORS preflight requests"""
    return '', 204

# Root redirect
@app.route('/')
def index():
    """Redirect to frontend"""
    return app.send_static_file('public/tarot_web.html')

# Vercel serverless handler
# The Flask app instance is automatically used by Vercel's Python runtime
# No additional handler needed - Vercel uses the 'app' variable directly

# Local development server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Starting development server on port {port}")
    app.run(debug=True, host='0.0.0.0', port=port)
