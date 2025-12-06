"""
Aplicación Flask principal para el sistema de Tarot
"""
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from models import db
from auth import init_jwt
import os

# Importar blueprints
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.reading_routes import reading_bp
from routes.subscription_routes import subscription_bp


def create_app(config_class=Config):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__, static_folder='.')
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    init_jwt(app)
    CORS(app, origins=config_class.CORS_ORIGINS, supports_credentials=True)
    
    # Migraciones
    migrate = Migrate(app, db)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(reading_bp)
    app.register_blueprint(subscription_bp)
    
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    
    # Rutas básicas
    @app.route('/')
    def index():
        """Sirve el archivo HTML principal"""
        return send_from_directory('.', 'tarot_web.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        """Sirve archivos estáticos"""
        return send_from_directory('.', path)
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Endpoint de health check"""
        return jsonify({
            'status': 'healthy',
            'service': 'Tarot API',
            'version': '1.0.0'
        }), 200
    
    @app.route('/api/info', methods=['GET'])
    def api_info():
        """Información de la API"""
        return jsonify({
            'name': 'Tarot Místico API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth/*',
                'user': '/api/user/*',
                'readings': '/api/readings/*',
                'subscription': '/api/subscription/*'
            },
            'features': [
                'Autenticación JWT',
                'Sistema Freemium',
                'Persistencia de temas',
                'Gestión de lecturas',
                'Suscripciones'
            ]
        }), 200
    
    # Manejadores de errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Recurso no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Acceso prohibido'}), 403
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'No autorizado'}), 401
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # Configuración para desarrollo
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║          🔮 Tarot Místico API Server 🔮                 ║
    ╠══════════════════════════════════════════════════════════╣
    ║  Servidor corriendo en: http://localhost:{port}         ║
    ║  API Base URL: http://localhost:{port}/api              ║
    ║  Health Check: http://localhost:{port}/api/health       ║
    ║  API Info: http://localhost:{port}/api/info             ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
