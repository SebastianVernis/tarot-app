"""
Middleware para verificar límites freemium
"""
from flask import jsonify
from models import User, UsageLimit, db
from datetime import date
from config import Config


class FreemiumMiddleware:
    """Middleware para gestionar límites del plan freemium"""
    
    @staticmethod
    def check_reading_limit(user):
        """
        Verifica si el usuario puede realizar una lectura
        Retorna (puede_leer: bool, mensaje: str, lecturas_restantes: int)
        """
        # Usuarios premium no tienen límites
        if user.is_premium():
            return True, "Usuario premium - sin límites", -1
        
        # Obtener o crear registro de uso para hoy
        today = date.today()
        usage = UsageLimit.query.filter_by(
            user_id=user.id,
            date=today
        ).first()
        
        if not usage:
            usage = UsageLimit(user_id=user.id, date=today, readings_count=0)
            db.session.add(usage)
            db.session.commit()
        
        # Verificar límite
        limit = Config.FREE_DAILY_READINGS
        remaining = limit - usage.readings_count
        
        if usage.readings_count >= limit:
            return False, f"Has alcanzado el límite de {limit} lecturas diarias. Actualiza a Premium para lecturas ilimitadas.", 0
        
        return True, f"Lecturas restantes hoy: {remaining}", remaining
    
    @staticmethod
    def check_spread_access(user, spread_type):
        """
        Verifica si el usuario puede acceder a un tipo de tirada
        Retorna (puede_acceder: bool, mensaje: str)
        """
        # Usuarios premium tienen acceso a todo
        if user.is_premium():
            return True, "Acceso completo"
        
        # Usuarios free solo pueden usar tiradas básicas
        allowed_spreads = Config.FREE_ALLOWED_SPREADS
        
        if spread_type not in allowed_spreads:
            return False, f"Esta tirada requiere suscripción Premium. Plan gratuito solo permite: {', '.join(allowed_spreads)}"
        
        return True, "Acceso permitido"
    
    @staticmethod
    def increment_reading_count(user):
        """Incrementa el contador de lecturas del usuario"""
        # No contar para usuarios premium
        if user.is_premium():
            return
        
        today = date.today()
        usage = UsageLimit.query.filter_by(
            user_id=user.id,
            date=today
        ).first()
        
        if not usage:
            usage = UsageLimit(user_id=user.id, date=today, readings_count=1)
            db.session.add(usage)
        else:
            usage.readings_count += 1
        
        db.session.commit()
    
    @staticmethod
    def get_usage_stats(user):
        """Obtiene estadísticas de uso del usuario"""
        today = date.today()
        usage = UsageLimit.query.filter_by(
            user_id=user.id,
            date=today
        ).first()
        
        if user.is_premium():
            return {
                'plan': 'premium',
                'readings_today': usage.readings_count if usage else 0,
                'readings_limit': -1,  # ilimitado
                'readings_remaining': -1,
                'allowed_spreads': 'all',
                'is_premium': True
            }
        
        readings_today = usage.readings_count if usage else 0
        limit = Config.FREE_DAILY_READINGS
        
        return {
            'plan': 'free',
            'readings_today': readings_today,
            'readings_limit': limit,
            'readings_remaining': max(0, limit - readings_today),
            'allowed_spreads': Config.FREE_ALLOWED_SPREADS,
            'is_premium': False
        }


def require_reading_limit(f):
    """Decorador para verificar límite de lecturas"""
    from functools import wraps
    from auth import get_current_user
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'No autenticado'}), 401
        
        can_read, message, remaining = FreemiumMiddleware.check_reading_limit(user)
        
        if not can_read:
            return jsonify({
                'error': message,
                'upgrade_required': True,
                'readings_remaining': remaining,
                'plan': user.subscription_plan
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_spread_access(f):
    """Decorador para verificar acceso a tipo de tirada"""
    from functools import wraps
    from auth import get_current_user
    from flask import request
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'No autenticado'}), 401
        
        # Obtener tipo de tirada del request
        data = request.get_json()
        spread_type = data.get('spread_type') if data else None
        
        if not spread_type:
            return jsonify({'error': 'Tipo de tirada no especificado'}), 400
        
        can_access, message = FreemiumMiddleware.check_spread_access(user, spread_type)
        
        if not can_access:
            return jsonify({
                'error': message,
                'upgrade_required': True,
                'allowed_spreads': Config.FREE_ALLOWED_SPREADS,
                'plan': user.subscription_plan
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
