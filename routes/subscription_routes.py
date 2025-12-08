"""
Rutas para gestión de suscripciones
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from src.models import User, Subscription, db
from src.auth import login_required
from datetime import datetime, timedelta

subscription_bp = Blueprint('subscription', __name__, url_prefix='/api/subscription')


@subscription_bp.route('/plans', methods=['GET'])
def get_plans():
    """Obtiene los planes disponibles"""
    plans = {
        'free': {
            'name': 'Plan Gratuito',
            'price': 0,
            'currency': 'USD',
            'features': [
                '3 lecturas diarias',
                'Tiradas básicas (1 carta, 3 cartas)',
                'Historial limitado (últimas 10 lecturas)',
                'Interpretaciones básicas'
            ],
            'limitations': [
                'Sin acceso a tiradas avanzadas',
                'Sin historial completo',
                'Anuncios ocasionales'
            ]
        },
        'premium': {
            'name': 'Plan Premium',
            'price': 9.99,
            'currency': 'USD',
            'billing': 'monthly',
            'features': [
                'Lecturas ilimitadas',
                'Todas las tiradas disponibles',
                'Historial completo de lecturas',
                'Interpretaciones detalladas',
                'Sin anuncios',
                'Exportar lecturas en PDF',
                'Soporte prioritario',
                'Nuevas funciones primero'
            ],
            'popular': True
        }
    }
    
    return jsonify({'plans': plans}), 200


@subscription_bp.route('/current', methods=['GET'])
@login_required
def get_current_subscription():
    """Obtiene la suscripción actual del usuario"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Obtener suscripción activa
        active_subscription = Subscription.query.filter_by(
            user_id=user.id,
            status='active'
        ).order_by(Subscription.created_at.desc()).first()
        
        subscription_data = {
            'plan': user.subscription_plan,
            'is_premium': user.is_premium(),
            'start_date': user.subscription_start.isoformat() if user.subscription_start else None,
            'end_date': user.subscription_end.isoformat() if user.subscription_end else None,
            'active_subscription': active_subscription.to_dict() if active_subscription else None
        }
        
        return jsonify(subscription_data), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener suscripción', 'details': str(e)}), 500


@subscription_bp.route('/upgrade', methods=['POST'])
@login_required
def upgrade_to_premium():
    """
    Actualiza a plan premium
    En producción, aquí se integraría con Stripe/PayPal
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if user.is_premium():
            return jsonify({'error': 'Ya tienes una suscripción premium activa'}), 400
        
        data = request.get_json()
        payment_method = data.get('payment_method', 'demo')  # En producción: stripe, paypal, etc.
        
        # Simular procesamiento de pago
        # En producción, aquí iría la integración con el procesador de pagos
        
        # Actualizar usuario a premium
        user.subscription_plan = 'premium'
        user.subscription_start = datetime.utcnow()
        user.subscription_end = datetime.utcnow() + timedelta(days=30)  # 1 mes
        
        # Crear registro de suscripción
        subscription = Subscription(
            user_id=user.id,
            plan='premium',
            status='active',
            start_date=user.subscription_start,
            end_date=user.subscription_end,
            payment_method=payment_method,
            amount=9.99,
            currency='USD'
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        return jsonify({
            'message': 'Actualización a Premium exitosa',
            'subscription': subscription.to_dict(),
            'user': user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar suscripción', 'details': str(e)}), 500


@subscription_bp.route('/cancel', methods=['POST'])
@login_required
def cancel_subscription():
    """Cancela la suscripción premium"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if not user.is_premium():
            return jsonify({'error': 'No tienes una suscripción premium activa'}), 400
        
        # Obtener suscripción activa
        active_subscription = Subscription.query.filter_by(
            user_id=user.id,
            status='active'
        ).order_by(Subscription.created_at.desc()).first()
        
        if active_subscription:
            active_subscription.status = 'cancelled'
        
        # El usuario mantiene acceso hasta la fecha de fin
        # No cambiamos subscription_plan ni subscription_end
        # Solo marcamos como cancelada para que no se renueve
        
        db.session.commit()
        
        return jsonify({
            'message': 'Suscripción cancelada. Mantendrás acceso premium hasta el final del período actual.',
            'access_until': user.subscription_end.isoformat() if user.subscription_end else None
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al cancelar suscripción', 'details': str(e)}), 500


@subscription_bp.route('/history', methods=['GET'])
@login_required
def get_subscription_history():
    """Obtiene el historial de suscripciones del usuario"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        subscriptions = Subscription.query.filter_by(
            user_id=user.id
        ).order_by(Subscription.created_at.desc()).all()
        
        history = [sub.to_dict() for sub in subscriptions]
        
        return jsonify({
            'history': history,
            'total': len(history)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener historial', 'details': str(e)}), 500


@subscription_bp.route('/demo-upgrade', methods=['POST'])
@login_required
def demo_upgrade():
    """
    Endpoint de demostración para actualizar a premium sin pago
    SOLO PARA DESARROLLO - Eliminar en producción
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Actualizar a premium por 30 días
        user.subscription_plan = 'premium'
        user.subscription_start = datetime.utcnow()
        user.subscription_end = datetime.utcnow() + timedelta(days=30)
        
        # Crear registro
        subscription = Subscription(
            user_id=user.id,
            plan='premium',
            status='active',
            start_date=user.subscription_start,
            end_date=user.subscription_end,
            payment_method='demo',
            amount=0,
            currency='USD'
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        return jsonify({
            'message': '¡Actualizado a Premium (DEMO)!',
            'subscription': subscription.to_dict(),
            'user': user.to_dict(include_email=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error en demo upgrade', 'details': str(e)}), 500
