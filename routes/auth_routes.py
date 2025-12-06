"""
Rutas de autenticación
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import User, db
from auth import create_tokens, login_required
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def validate_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Valida que la contraseña sea segura"""
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    return True, "OK"


@auth_bp.route('/register', methods=['POST'])
def register():
    """Registra un nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not email or not username or not password:
            return jsonify({'error': 'Email, username y password son requeridos'}), 400
        
        # Validar email
        if not validate_email(email):
            return jsonify({'error': 'Email inválido'}), 400
        
        # Validar password
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'El email ya está registrado'}), 409
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'El username ya está en uso'}), 409
        
        # Crear nuevo usuario
        user = User(
            email=email,
            username=username,
            subscription_plan='free',
            theme=data.get('theme', 'dark')
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Crear tokens
        tokens = create_tokens(user)
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            **tokens
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al registrar usuario', 'details': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Inicia sesión de usuario"""
    try:
        data = request.get_json()
        
        email_or_username = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email_or_username or not password:
            return jsonify({'error': 'Email/username y password son requeridos'}), 400
        
        # Buscar usuario por email o username
        user = User.query.filter(
            (User.email == email_or_username) | (User.username == email_or_username)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Cuenta desactivada'}), 403
        
        # Crear tokens
        tokens = create_tokens(user)
        
        return jsonify({
            'message': 'Login exitoso',
            **tokens
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al iniciar sesión', 'details': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresca el token de acceso"""
    try:
        from flask_jwt_extended import create_access_token
        
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'Usuario no válido'}), 401
        
        access_token = create_access_token(identity=user)
        
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al refrescar token', 'details': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Obtiene información del usuario actual"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'user': user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener usuario', 'details': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Cierra sesión (en el cliente se debe eliminar el token)"""
    # En una implementación más completa, aquí se podría agregar el token a una blacklist
    return jsonify({'message': 'Logout exitoso'}), 200


@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Cambia la contraseña del usuario"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Contraseña actual y nueva son requeridas'}), 400
        
        # Verificar contraseña actual
        if not user.check_password(current_password):
            return jsonify({'error': 'Contraseña actual incorrecta'}), 401
        
        # Validar nueva contraseña
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Cambiar contraseña
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Contraseña cambiada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al cambiar contraseña', 'details': str(e)}), 500
