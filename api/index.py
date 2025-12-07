"""
Vercel Serverless Function Entry Point
Optimized for Vercel's 250 MB limit
"""
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# Import only lightweight routes
try:
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.reading_routes import reading_bp
    from routes.subscription_routes import subscription_bp
except ImportError as e:
    print(f"Warning: Could not import routes: {e}")
    auth_bp = user_bp = reading_bp = subscription_bp = None

# Try to import astrology routes (may fail if pyswisseph not available)
try:
    from routes.astrology_routes import astrology_bp
    ASTROLOGY_AVAILABLE = True
except ImportError:
    print("Warning: Astrology features disabled (pyswisseph not available)")
    astrology_bp = None
    ASTROLOGY_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize CORS
CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)

# Initialize database (lightweight - SQLite)
try:
    from models import db
    from auth import init_jwt
    
    db.init_app(app)
    init_jwt(app)
    
    # Create tables if needed
    with app.app_context():
        db.create_all()
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")

# Register blueprints
if auth_bp:
    app.register_blueprint(auth_bp)
if user_bp:
    app.register_blueprint(user_bp)
if reading_bp:
    app.register_blueprint(reading_bp)
if subscription_bp:
    app.register_blueprint(subscription_bp)
if astrology_bp and ASTROLOGY_AVAILABLE:
    app.register_blueprint(astrology_bp)

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
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Acceso prohibido'}), 403

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'No autorizado'}), 401

# Vercel serverless function handler
def handler(request):
    """Vercel serverless function handler"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()

# For local testing
if __name__ == '__main__':
    app.run(debug=True, port=5000)
