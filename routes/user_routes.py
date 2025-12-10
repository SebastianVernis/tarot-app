"""
Rutas de usuario y configuraciones
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from src.models import User, Reading, db
from src.auth import login_required
from src.middleware import FreemiumMiddleware

user_bp = Blueprint('user', __name__, url_prefix='/api/user')


@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Obtiene el perfil completo del usuario"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Obtener estadísticas
        total_readings = Reading.query.filter_by(user_id=user.id).count()
        favorite_readings = Reading.query.filter_by(user_id=user.id, is_favorite=True).count()
        
        # Obtener uso actual
        usage_stats = FreemiumMiddleware.get_usage_stats(user)
        
        return jsonify({
            'user': user.to_dict(include_email=True),
            'stats': {
                'total_readings': total_readings,
                'favorite_readings': favorite_readings
            },
            'usage': usage_stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener perfil', 'details': str(e)}), 500


@user_bp.route('/settings', methods=['PUT'])
@login_required
def update_settings():
    """Actualiza configuraciones del usuario"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Actualizar tema
        if 'theme' in data:
            theme = data['theme']
            if theme in ['light', 'dark']:
                user.theme = theme
            else:
                return jsonify({'error': 'Tema inválido. Debe ser "light" o "dark"'}), 400
        
        # Actualizar idioma
        if 'language' in data:
            user.language = data['language']
        
        # Actualizar username
        if 'username' in data:
            new_username = data['username'].strip()
            if new_username != user.username:
                # Verificar que no esté en uso
                existing = User.query.filter_by(username=new_username).first()
                if existing:
                    return jsonify({'error': 'Username ya está en uso'}), 409
                user.username = new_username
        
        db.session.commit()
        
        return jsonify({
            'message': 'Configuraciones actualizadas',
            'user': user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar configuraciones', 'details': str(e)}), 500


@user_bp.route('/theme', methods=['PUT'])
@login_required
def update_theme():
    """Actualiza solo el tema del usuario"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        theme = data.get('theme')
        
        if not theme or theme not in ['light', 'dark']:
            return jsonify({'error': 'Tema inválido. Debe ser "light" o "dark"'}), 400
        
        user.theme = theme
        db.session.commit()
        
        return jsonify({
            'message': 'Tema actualizado',
            'theme': user.theme
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar tema', 'details': str(e)}), 500


@user_bp.route('/usage', methods=['GET'])
@login_required
def get_usage():
    """Obtiene estadísticas de uso del usuario"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        usage_stats = FreemiumMiddleware.get_usage_stats(user)
        
        return jsonify(usage_stats), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener uso', 'details': str(e)}), 500


@user_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Obtiene estadísticas detalladas del usuario"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Estadísticas de lecturas
        total_readings = Reading.query.filter_by(user_id=user.id).count()
        favorite_readings = Reading.query.filter_by(user_id=user.id, is_favorite=True).count()
        
        # Lecturas por tipo de tirada
        from sqlalchemy import func
        spread_stats = db.session.query(
            Reading.spread_type,
            func.count(Reading.id).label('count')
        ).filter_by(user_id=user.id).group_by(Reading.spread_type).all()
        
        spread_distribution = {spread: count for spread, count in spread_stats}
        
        # Lecturas recientes (últimos 7 días)
        from datetime import datetime, timedelta
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_readings = Reading.query.filter(
            Reading.user_id == user.id,
            Reading.created_at >= seven_days_ago
        ).count()
        
        return jsonify({
            'total_readings': total_readings,
            'favorite_readings': favorite_readings,
            'recent_readings_7d': recent_readings,
            'spread_distribution': spread_distribution,
            'member_since': user.created_at.isoformat(),
            'is_premium': user.is_premium()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener estadísticas', 'details': str(e)}), 500
