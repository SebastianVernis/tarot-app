"""
Rutas para cálculos astrológicos y lecturas de carta natal
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models import AstrologyReading, User, db
from auth import login_required
from astrology_calculator import AstrologyCalculator
from gemini_service import GeminiService
from datetime import datetime
import pytz
from config import Config

astrology_bp = Blueprint('astrology', __name__, url_prefix='/api/astrology')

# Inicializar servicios
astrology_calc = AstrologyCalculator()


def get_gemini_service():
    """Obtiene instancia del servicio Gemini"""
    try:
        return GeminiService()
    except ValueError:
        return None


@astrology_bp.route('/calculate', methods=['POST'])
@login_required
def calculate_positions():
    """
    Calcula posiciones planetarias para una fecha y ubicación específicas
    
    Body JSON:
    {
        "date": "2000-01-01T00:00:00",
        "latitude": 19.4326,
        "longitude": -99.1332,
        "timezone": "America/Mexico_City" (opcional)
    }
    """
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        if isinstance(user_id, str):
            user_id = int(user_id)
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('date'):
            return jsonify({'error': 'Fecha requerida'}), 400
        
        if data.get('latitude') is None or data.get('longitude') is None:
            return jsonify({'error': 'Latitud y longitud requeridas'}), 400
        
        # Parsear fecha
        try:
            date_str = data['date']
            if 'T' in date_str:
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError as e:
            return jsonify({'error': f'Formato de fecha inválido: {str(e)}'}), 400
        
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        timezone_str = data.get('timezone')
        
        # Calcular posiciones
        positions = astrology_calc.calculate_planetary_positions(
            date, latitude, longitude
        )
        
        return jsonify({
            'success': True,
            'positions': positions
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error calculando posiciones planetarias',
            'details': str(e)
        }), 500


@astrology_bp.route('/birth-chart', methods=['POST'])
@login_required
def create_birth_chart():
    """
    Genera carta natal completa con interpretación
    
    Body JSON:
    {
        "birth_date": "1990-05-15T14:30:00",
        "latitude": 19.4326,
        "longitude": -99.1332,
        "timezone": "America/Mexico_City" (opcional),
        "location_name": "Ciudad de México" (opcional),
        "generate_interpretation": true (opcional, default: true)
    }
    """
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('birth_date'):
            return jsonify({'error': 'Fecha de nacimiento requerida'}), 400
        
        if data.get('latitude') is None or data.get('longitude') is None:
            return jsonify({'error': 'Latitud y longitud requeridas'}), 400
        
        # Parsear fecha de nacimiento
        try:
            birth_date_str = data['birth_date']
            if 'T' in birth_date_str:
                birth_date = datetime.fromisoformat(birth_date_str.replace('Z', '+00:00'))
            else:
                birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
        except ValueError as e:
            return jsonify({'error': f'Formato de fecha inválido: {str(e)}'}), 400
        
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        timezone_str = data.get('timezone')
        location_name = data.get('location_name', '')
        generate_interpretation = data.get('generate_interpretation', True)
        
        # Calcular carta natal
        chart_data = astrology_calc.calculate_birth_chart(
            birth_date, latitude, longitude, timezone_str
        )
        
        # Generar interpretación con Gemini si se solicita
        interpretation = None
        if generate_interpretation:
            gemini_service = get_gemini_service()
            if gemini_service:
                try:
                    interpretation = gemini_service.generate_birth_chart_interpretation(chart_data)
                except Exception as e:
                    print(f"Error generando interpretación: {str(e)}")
                    interpretation = "Interpretación no disponible en este momento."
            else:
                interpretation = "Servicio de interpretación no configurado. Configure GEMINI_API_KEY."
        
        # Crear registro en base de datos
        astrology_reading = AstrologyReading(
            user_id=user.id,
            birth_date=birth_date,
            birth_latitude=latitude,
            birth_longitude=longitude,
            birth_timezone=chart_data['birth_data']['timezone'],
            birth_location_name=location_name,
            reading_type='birth_chart',
            interpretation=interpretation,
            sun_sign=chart_data['summary']['sun_sign'],
            moon_sign=chart_data['summary']['moon_sign'],
            rising_sign=chart_data['summary']['rising_sign']
        )
        
        astrology_reading.set_chart_data(chart_data)
        
        db.session.add(astrology_reading)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Carta natal generada exitosamente',
            'reading': astrology_reading.to_dict(include_full_chart=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error generando carta natal',
            'details': str(e)
        }), 500


@astrology_bp.route('/readings', methods=['GET'])
@login_required
def get_readings():
    """Obtiene todas las lecturas astrológicas del usuario"""
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Filtros
        reading_type = request.args.get('reading_type')
        is_favorite = request.args.get('is_favorite', type=bool)
        
        # Query base
        query = AstrologyReading.query.filter_by(user_id=user.id)
        
        # Aplicar filtros
        if reading_type:
            query = query.filter_by(reading_type=reading_type)
        
        if is_favorite is not None:
            query = query.filter_by(is_favorite=is_favorite)
        
        # Ordenar por fecha descendente
        query = query.order_by(AstrologyReading.created_at.desc())
        
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
        return jsonify({
            'error': 'Error obteniendo lecturas',
            'details': str(e)
        }), 500


@astrology_bp.route('/readings/<int:reading_id>', methods=['GET'])
@login_required
def get_reading(reading_id):
    """Obtiene una lectura astrológica específica"""
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        reading = AstrologyReading.query.filter_by(
            id=reading_id,
            user_id=user_id
        ).first()
        
        if not reading:
            return jsonify({'error': 'Lectura no encontrada'}), 404
        
        return jsonify({
            'reading': reading.to_dict(include_full_chart=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error obteniendo lectura',
            'details': str(e)
        }), 500


@astrology_bp.route('/readings/<int:reading_id>', methods=['PUT'])
@login_required
def update_reading(reading_id):
    """Actualiza una lectura astrológica (notas, favorito)"""
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        reading = AstrologyReading.query.filter_by(
            id=reading_id,
            user_id=user_id
        ).first()
        
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
        return jsonify({
            'error': 'Error actualizando lectura',
            'details': str(e)
        }), 500


@astrology_bp.route('/readings/<int:reading_id>', methods=['DELETE'])
@login_required
def delete_reading(reading_id):
    """Elimina una lectura astrológica"""
    try:
        user_id = get_jwt_identity()
        if isinstance(user_id, str):
            user_id = int(user_id)
        
        reading = AstrologyReading.query.filter_by(
            id=reading_id,
            user_id=user_id
        ).first()
        
        if not reading:
            return jsonify({'error': 'Lectura no encontrada'}), 404
        
        db.session.delete(reading)
        db.session.commit()
        
        return jsonify({
            'message': 'Lectura eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error eliminando lectura',
            'details': str(e)
        }), 500


@astrology_bp.route('/daily-horoscope', methods=['POST'])
@login_required
def get_daily_horoscope():
    """
    Genera horóscopo diario para un signo
    
    Body JSON:
    {
        "sun_sign": "Aries",
        "date": "2024-01-01" (opcional, default: hoy)
    }
    """
    try:
        data = request.get_json()
        
        sun_sign = data.get('sun_sign')
        if not sun_sign:
            return jsonify({'error': 'Signo solar requerido'}), 400
        
        date_str = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        # Generar horóscopo con Gemini
        gemini_service = get_gemini_service()
        if not gemini_service:
            return jsonify({
                'error': 'Servicio de horóscopo no configurado',
                'details': 'Configure GEMINI_API_KEY'
            }), 503
        
        horoscope = gemini_service.generate_daily_horoscope(sun_sign, date_str)
        
        return jsonify({
            'success': True,
            'sun_sign': sun_sign,
            'date': date_str,
            'horoscope': horoscope
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error generando horóscopo',
            'details': str(e)
        }), 500


@astrology_bp.route('/compatibility', methods=['POST'])
@login_required
def calculate_compatibility():
    """
    Calcula compatibilidad entre dos personas
    
    Body JSON:
    {
        "person1": {
            "sun_sign": "Aries",
            "moon_sign": "Leo",
            "rising_sign": "Sagitario"
        },
        "person2": {
            "sun_sign": "Libra",
            "moon_sign": "Acuario",
            "rising_sign": "Géminis"
        }
    }
    """
    try:
        data = request.get_json()
        
        person1 = data.get('person1')
        person2 = data.get('person2')
        
        if not person1 or not person2:
            return jsonify({'error': 'Datos de ambas personas requeridos'}), 400
        
        # Generar análisis de compatibilidad con Gemini
        gemini_service = get_gemini_service()
        if not gemini_service:
            return jsonify({
                'error': 'Servicio de compatibilidad no configurado',
                'details': 'Configure GEMINI_API_KEY'
            }), 503
        
        compatibility = gemini_service.generate_compatibility_reading(person1, person2)
        
        return jsonify({
            'success': True,
            'person1': person1,
            'person2': person2,
            'compatibility_analysis': compatibility
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error calculando compatibilidad',
            'details': str(e)
        }), 500


@astrology_bp.route('/info', methods=['GET'])
def get_astrology_info():
    """Información sobre el servicio de astrología"""
    return jsonify({
        'service': 'Astrología y Carta Natal',
        'version': '1.0.0',
        'features': [
            'Cálculo preciso de posiciones planetarias',
            'Carta natal completa con casas astrológicas',
            'Interpretaciones personalizadas con IA',
            'Horóscopo diario',
            'Análisis de compatibilidad',
            'Cálculo de aspectos planetarios'
        ],
        'planets': [
            'Sol', 'Luna', 'Mercurio', 'Venus', 'Marte',
            'Júpiter', 'Saturno', 'Urano', 'Neptuno', 'Plutón'
        ],
        'zodiac_signs': [
            'Aries', 'Tauro', 'Géminis', 'Cáncer', 'Leo', 'Virgo',
            'Libra', 'Escorpio', 'Sagitario', 'Capricornio', 'Acuario', 'Piscis'
        ],
        'endpoints': {
            'calculate': 'POST /api/astrology/calculate - Calcular posiciones planetarias',
            'birth_chart': 'POST /api/astrology/birth-chart - Generar carta natal completa',
            'readings': 'GET /api/astrology/readings - Obtener lecturas guardadas',
            'daily_horoscope': 'POST /api/astrology/daily-horoscope - Horóscopo diario',
            'compatibility': 'POST /api/astrology/compatibility - Análisis de compatibilidad'
        }
    }), 200
