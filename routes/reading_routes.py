"""
Rutas para lecturas de tarot
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from src.models import Reading, User, db
from src.auth import login_required
from src.middleware import require_reading_limit, require_spread_access, FreemiumMiddleware
from config import Config

reading_bp = Blueprint('reading', __name__, url_prefix='/api/readings')


@reading_bp.route('/', methods=['POST'])
@login_required
@require_spread_access
@require_reading_limit
def create_reading():
    """Crea una nueva lectura de tarot"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Validar datos requeridos
        spread_type = data.get('spread_type')
        cards = data.get('cards', [])
        
        if not spread_type:
            return jsonify({'error': 'Tipo de tirada requerido'}), 400
        
        if not cards:
            return jsonify({'error': 'Cartas requeridas'}), 400
        
        # Crear lectura
        reading = Reading(
            user_id=user.id,
            spread_type=spread_type,
            question=data.get('question', ''),
            interpretation=data.get('interpretation', '')
        )
        reading.set_cards(cards)
        
        db.session.add(reading)
        
        # Incrementar contador de uso
        FreemiumMiddleware.increment_reading_count(user)
        
        db.session.commit()
        
        # Obtener estadísticas actualizadas
        usage_stats = FreemiumMiddleware.get_usage_stats(user)
        
        return jsonify({
            'message': 'Lectura creada exitosamente',
            'reading': reading.to_dict(),
            'usage': usage_stats
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al crear lectura', 'details': str(e)}), 500


@reading_bp.route('/', methods=['GET'])
@login_required
def get_readings():
    """Obtiene todas las lecturas del usuario con paginación"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', Config.READINGS_PER_PAGE, type=int)
        
        # Filtros
        spread_type = request.args.get('spread_type')
        is_favorite = request.args.get('is_favorite', type=bool)
        
        # Query base
        query = Reading.query.filter_by(user_id=user.id)
        
        # Aplicar filtros
        if spread_type:
            query = query.filter_by(spread_type=spread_type)
        
        if is_favorite is not None:
            query = query.filter_by(is_favorite=is_favorite)
        
        # Ordenar por fecha descendente
        query = query.order_by(Reading.created_at.desc())
        
        # Paginación
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        readings = [reading.to_dict() for reading in pagination.items]
        
        return jsonify({
            'readings': readings,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener lecturas', 'details': str(e)}), 500


@reading_bp.route('/<int:reading_id>', methods=['GET'])
@login_required
def get_reading(reading_id):
    """Obtiene una lectura específica"""
    try:
        user_id = get_jwt_identity()
        
        reading = Reading.query.filter_by(id=reading_id, user_id=user_id).first()
        
        if not reading:
            return jsonify({'error': 'Lectura no encontrada'}), 404
        
        return jsonify({
            'reading': reading.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener lectura', 'details': str(e)}), 500


@reading_bp.route('/<int:reading_id>', methods=['PUT'])
@login_required
def update_reading(reading_id):
    """Actualiza una lectura (notas, favorito)"""
    try:
        user_id = get_jwt_identity()
        
        reading = Reading.query.filter_by(id=reading_id, user_id=user_id).first()
        
        if not reading:
            return jsonify({'error': 'Lectura no encontrada'}), 404
        
        data = request.get_json()
        
        # Actualizar campos permitidos
        if 'notes' in data:
            reading.notes = data['notes']
        
        if 'is_favorite' in data:
            reading.is_favorite = bool(data['is_favorite'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Lectura actualizada',
            'reading': reading.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar lectura', 'details': str(e)}), 500


@reading_bp.route('/<int:reading_id>', methods=['DELETE'])
@login_required
def delete_reading(reading_id):
    """Elimina una lectura"""
    try:
        user_id = get_jwt_identity()
        
        reading = Reading.query.filter_by(id=reading_id, user_id=user_id).first()
        
        if not reading:
            return jsonify({'error': 'Lectura no encontrada'}), 404
        
        db.session.delete(reading)
        db.session.commit()
        
        return jsonify({
            'message': 'Lectura eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al eliminar lectura', 'details': str(e)}), 500


@reading_bp.route('/<int:reading_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(reading_id):
    """Marca/desmarca una lectura como favorita"""
    try:
        user_id = get_jwt_identity()
        
        reading = Reading.query.filter_by(id=reading_id, user_id=user_id).first()
        
        if not reading:
            return jsonify({'error': 'Lectura no encontrada'}), 404
        
        reading.is_favorite = not reading.is_favorite
        db.session.commit()
        
        return jsonify({
            'message': 'Favorito actualizado',
            'is_favorite': reading.is_favorite,
            'reading': reading.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar favorito', 'details': str(e)}), 500


@reading_bp.route('/check-access', methods=['POST'])
@login_required
def check_access():
    """Verifica si el usuario puede realizar una lectura"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        spread_type = data.get('spread_type')
        
        if not spread_type:
            return jsonify({'error': 'Tipo de tirada requerido'}), 400
        
        # Verificar acceso a la tirada
        can_access_spread, spread_message = FreemiumMiddleware.check_spread_access(user, spread_type)
        
        # Verificar límite de lecturas
        can_read, limit_message, remaining = FreemiumMiddleware.check_reading_limit(user)
        
        # Obtener estadísticas de uso
        usage_stats = FreemiumMiddleware.get_usage_stats(user)
        
        return jsonify({
            'can_access': can_access_spread and can_read,
            'spread_access': {
                'allowed': can_access_spread,
                'message': spread_message
            },
            'reading_limit': {
                'allowed': can_read,
                'message': limit_message,
                'remaining': remaining
            },
            'usage': usage_stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al verificar acceso', 'details': str(e)}), 500
