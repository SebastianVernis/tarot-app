"""
Sistema de autenticación JWT
"""
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import (
    JWTManager, 
    create_access_token, 
    create_refresh_token,
    get_jwt_identity,
    verify_jwt_in_request,
    get_jwt
)
from models import User, db
from datetime import datetime

jwt = JWTManager()


def init_jwt(app):
    """Inicializa JWT con la app"""
    jwt.init_app(app)
    
    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        """Define cómo se serializa la identidad del usuario"""
        return user_id
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Carga el usuario desde el token"""
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).first()


def login_required(fn):
    """Decorador para requerir autenticación"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        # Convertir identity a int si es string
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        return fn(*args, **kwargs)
    return wrapper


def premium_required(fn):
    """Decorador para requerir suscripción premium"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 404
            
            if not user.is_premium():
                return jsonify({
                    'error': 'Se requiere suscripción premium',
                    'upgrade_required': True,
                    'current_plan': user.subscription_plan
                }), 403
            
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Error de autenticación', 'message': str(e)}), 401
    return wrapper


def create_tokens(user):
    """Crea tokens de acceso y refresh para un usuario"""
    # Actualizar último login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(include_email=True)
    }


def get_current_user():
    """Obtiene el usuario actual desde el token JWT"""
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return User.query.get(user_id)
    except:
        return None
