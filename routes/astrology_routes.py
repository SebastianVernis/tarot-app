"""
Rutas para cálculos astrológicos y cartas natales
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from models import BirthChart, AspectRecord, User, db
from auth import login_required
from astrology_calculator import (
    AstrologyCalculator,
    HouseSystem,
    calculate_houses_and_aspects
)
from gemini_service import GeminiAstrologyService
from datetime import datetime
import pytz

astrology_bp = Blueprint('astrology', __name__, url_prefix='/api/astrology')


@astrology_bp.route('/birth-chart', methods=['POST'])
@login_required
def create_birth_chart():
    """
    Calcula una carta natal completa
    
    Body JSON:
    {
        "birth_datetime": "1990-05-15T14:30:00",
        "timezone": "America/Mexico_City",
        "latitude": 19.4326,
        "longitude": -99.1332,
        "location_name": "Ciudad de México",
        "house_system": "P",  // Opcional: P=Placidus, K=Koch, E=Equal
        "include_interpretations": true,  // Opcional
        "name": "Mi Carta Natal"  // Opcional
    }
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['birth_datetime', 'timezone', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        # Parsear fecha de nacimiento
        try:
            birth_dt = datetime.fromisoformat(data['birth_datetime'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Use ISO 8601'}), 400
        
        # Validar coordenadas
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        
        if not (-90 <= latitude <= 90):
            return jsonify({'error': 'Latitud debe estar entre -90 y 90'}), 400
        
        if not (-180 <= longitude <= 180):
            return jsonify({'error': 'Longitud debe estar entre -180 y 180'}), 400
        
        # Validar zona horaria
        timezone_str = data['timezone']
        try:
            pytz.timezone(timezone_str)
        except pytz.exceptions.UnknownTimeZoneError:
            return jsonify({'error': f'Zona horaria inválida: {timezone_str}'}), 400
        
        # Sistema de casas
        house_system = data.get('house_system', HouseSystem.PLACIDUS)
        if house_system not in ['P', 'K', 'E', 'W', 'C', 'R']:
            return jsonify({'error': 'Sistema de casas inválido'}), 400
        
        # Calcular carta natal
        calculator = AstrologyCalculator()
        chart_data = calculator.calculate_birth_chart(
            birth_dt,
            latitude,
            longitude,
            timezone_str,
            house_system,
            include_minor_aspects=True
        )
        
        # Crear registro en base de datos
        birth_chart = BirthChart(
            user_id=user.id,
            birth_datetime=birth_dt,
            timezone=timezone_str,
            latitude=latitude,
            longitude=longitude,
            location_name=data.get('location_name'),
            house_system=house_system,
            name=data.get('name')
        )
        
        # Guardar datos calculados
        birth_chart.set_planetary_positions(chart_data['planetary_positions'])
        birth_chart.set_houses_data(chart_data['houses'])
        birth_chart.set_aspects_data(chart_data['aspects'])
        birth_chart.set_chart_summary(chart_data['chart_summary'])
        
        # Generar interpretaciones con Gemini si se solicita
        if data.get('include_interpretations', False):
            try:
                gemini_service = GeminiAstrologyService()
                interpretations = gemini_service.generate_personalized_reading(
                    chart_data,
                    question=data.get('question')
                )
                birth_chart.set_interpretations(interpretations)
            except Exception as e:
                # Si falla Gemini, continuar sin interpretaciones
                print(f"Error generando interpretaciones: {e}")
        
        db.session.add(birth_chart)
        db.session.commit()
        
        return jsonify({
            'message': 'Carta natal calculada exitosamente',
            'birth_chart': birth_chart.to_dict(include_full_data=True)
        }), 201
        
    except ValueError as e:
        return jsonify({'error': f'Error en los datos: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al calcular carta natal', 'details': str(e)}), 500


@astrology_bp.route('/birth-chart/<int:chart_id>', methods=['GET'])
@login_required
def get_birth_chart(chart_id):
    """Obtiene una carta natal específica"""
    try:
        user_id = get_jwt_identity()
        
        birth_chart = BirthChart.query.filter_by(id=chart_id, user_id=user_id).first()
        
        if not birth_chart:
            return jsonify({'error': 'Carta natal no encontrada'}), 404
        
        return jsonify({
            'birth_chart': birth_chart.to_dict(include_full_data=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener carta natal', 'details': str(e)}), 500


@astrology_bp.route('/birth-charts', methods=['GET'])
@login_required
def get_birth_charts():
    """Obtiene todas las cartas natales del usuario"""
    try:
        user_id = get_jwt_identity()
        
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Query
        query = BirthChart.query.filter_by(user_id=user_id).order_by(BirthChart.created_at.desc())
        
        # Paginación
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # No incluir datos completos en la lista
        charts = [chart.to_dict(include_full_data=False) for chart in pagination.items]
        
        return jsonify({
            'birth_charts': charts,
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
        return jsonify({'error': 'Error al obtener cartas natales', 'details': str(e)}), 500


@astrology_bp.route('/birth-chart/<int:chart_id>', methods=['PUT'])
@login_required
def update_birth_chart(chart_id):
    """Actualiza una carta natal (nombre, notas, favorito)"""
    try:
        user_id = get_jwt_identity()
        
        birth_chart = BirthChart.query.filter_by(id=chart_id, user_id=user_id).first()
        
        if not birth_chart:
            return jsonify({'error': 'Carta natal no encontrada'}), 404
        
        data = request.get_json()
        
        # Actualizar campos permitidos
        if 'name' in data:
            birth_chart.name = data['name']
        
        if 'notes' in data:
            birth_chart.notes = data['notes']
        
        if 'is_favorite' in data:
            birth_chart.is_favorite = bool(data['is_favorite'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Carta natal actualizada',
            'birth_chart': birth_chart.to_dict(include_full_data=False)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar carta natal', 'details': str(e)}), 500


@astrology_bp.route('/birth-chart/<int:chart_id>', methods=['DELETE'])
@login_required
def delete_birth_chart(chart_id):
    """Elimina una carta natal"""
    try:
        user_id = get_jwt_identity()
        
        birth_chart = BirthChart.query.filter_by(id=chart_id, user_id=user_id).first()
        
        if not birth_chart:
            return jsonify({'error': 'Carta natal no encontrada'}), 404
        
        db.session.delete(birth_chart)
        db.session.commit()
        
        return jsonify({
            'message': 'Carta natal eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al eliminar carta natal', 'details': str(e)}), 500


@astrology_bp.route('/aspects', methods=['POST'])
@login_required
def calculate_aspects():
    """
    Calcula aspectos entre posiciones planetarias
    
    Body JSON:
    {
        "planetary_positions": {
            "0": {"longitude": 45.5, "name": "Sol"},
            "1": {"longitude": 135.2, "name": "Luna"}
        },
        "include_minor": true
    }
    """
    try:
        data = request.get_json()
        
        if 'planetary_positions' not in data:
            return jsonify({'error': 'Campo requerido: planetary_positions'}), 400
        
        planetary_positions = data['planetary_positions']
        include_minor = data.get('include_minor', True)
        
        # Convertir claves a enteros si vienen como strings
        positions_dict = {}
        for key, value in planetary_positions.items():
            positions_dict[int(key)] = value
        
        # Calcular aspectos
        calculator = AstrologyCalculator()
        aspects = calculator.calculate_aspects(positions_dict, include_minor)
        
        return jsonify({
            'aspects': aspects,
            'total_aspects': len(aspects)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al calcular aspectos', 'details': str(e)}), 500


@astrology_bp.route('/interpret', methods=['POST'])
@login_required
def interpret_placement():
    """
    Genera interpretación de una posición planetaria o aspecto usando Gemini
    
    Body JSON:
    {
        "type": "house_placement" | "aspect" | "ascendant" | "midheaven",
        "data": {
            // Para house_placement:
            "planet_name": "Sol",
            "house_number": 10,
            "sign": "Capricornio",
            "degree": 15.5
            
            // Para aspect:
            "planet1_name": "Sol",
            "planet2_name": "Luna",
            "aspect_name": "Trígono",
            "aspect_angle": 120,
            "orb": 2.5,
            "nature": "harmonious"
            
            // Para ascendant/midheaven:
            "sign": "Aries",
            "degree": 10.2
        }
    }
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        if 'type' not in data or 'data' not in data:
            return jsonify({'error': 'Campos requeridos: type, data'}), 400
        
        interpretation_type = data['type']
        interpretation_data = data['data']
        
        # Inicializar servicio Gemini
        try:
            gemini_service = GeminiAstrologyService()
        except ValueError as e:
            return jsonify({'error': str(e)}), 500
        
        # Generar interpretación según el tipo
        interpretation = ""
        
        if interpretation_type == 'house_placement':
            interpretation = gemini_service.interpret_house_placement(
                interpretation_data['planet_name'],
                interpretation_data['house_number'],
                interpretation_data['sign'],
                interpretation_data['degree']
            )
        
        elif interpretation_type == 'aspect':
            interpretation = gemini_service.interpret_aspect(
                interpretation_data['planet1_name'],
                interpretation_data['planet2_name'],
                interpretation_data['aspect_name'],
                interpretation_data['aspect_angle'],
                interpretation_data['orb'],
                interpretation_data['nature']
            )
        
        elif interpretation_type == 'ascendant':
            interpretation = gemini_service.interpret_ascendant(
                interpretation_data['sign'],
                interpretation_data['degree']
            )
        
        elif interpretation_type == 'midheaven':
            interpretation = gemini_service.interpret_midheaven(
                interpretation_data['sign'],
                interpretation_data['degree']
            )
        
        else:
            return jsonify({'error': f'Tipo de interpretación inválido: {interpretation_type}'}), 400
        
        return jsonify({
            'interpretation': interpretation,
            'type': interpretation_type
        }), 200
        
    except KeyError as e:
        return jsonify({'error': f'Campo faltante en data: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': 'Error al generar interpretación', 'details': str(e)}), 500


@astrology_bp.route('/birth-chart/<int:chart_id>/interpret', methods=['POST'])
@login_required
def interpret_birth_chart(chart_id):
    """
    Genera o actualiza interpretaciones completas de una carta natal
    
    Body JSON (opcional):
    {
        "question": "¿Cuál es mi propósito de vida?"
    }
    """
    try:
        user_id = get_jwt_identity()
        
        birth_chart = BirthChart.query.filter_by(id=chart_id, user_id=user_id).first()
        
        if not birth_chart:
            return jsonify({'error': 'Carta natal no encontrada'}), 404
        
        data = request.get_json() or {}
        question = data.get('question')
        
        # Reconstruir chart_data
        chart_data = {
            'planetary_positions': birth_chart.get_planetary_positions(),
            'houses': birth_chart.get_houses_data(),
            'aspects': birth_chart.get_aspects_data(),
            'chart_summary': birth_chart.get_chart_summary()
        }
        
        # Generar interpretaciones
        try:
            gemini_service = GeminiAstrologyService()
            interpretations = gemini_service.generate_personalized_reading(
                chart_data,
                question=question
            )
            
            # Actualizar en base de datos
            birth_chart.set_interpretations(interpretations)
            db.session.commit()
            
            return jsonify({
                'message': 'Interpretaciones generadas exitosamente',
                'interpretations': interpretations
            }), 200
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 500
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al generar interpretaciones', 'details': str(e)}), 500


@astrology_bp.route('/house-systems', methods=['GET'])
def get_house_systems():
    """Obtiene información sobre los sistemas de casas disponibles"""
    systems = {
        'P': {
            'name': 'Placidus',
            'description': 'Sistema más popular, basado en divisiones temporales',
            'best_for': 'Análisis psicológico y predictivo'
        },
        'K': {
            'name': 'Koch',
            'description': 'Sistema del lugar de nacimiento',
            'best_for': 'Análisis de eventos y timing'
        },
        'E': {
            'name': 'Equal House (Casas Iguales)',
            'description': 'Divisiones de 30° desde el Ascendente',
            'best_for': 'Simplicidad y claridad'
        },
        'W': {
            'name': 'Whole Sign (Signos Completos)',
            'description': 'Cada signo completo es una casa',
            'best_for': 'Astrología tradicional'
        },
        'C': {
            'name': 'Campanus',
            'description': 'Basado en el círculo vertical',
            'best_for': 'Análisis espacial'
        },
        'R': {
            'name': 'Regiomontanus',
            'description': 'Sistema medieval clásico',
            'best_for': 'Astrología horaria'
        }
    }
    
    return jsonify({
        'house_systems': systems,
        'default': 'P'
    }), 200


@astrology_bp.route('/timezones', methods=['GET'])
def get_common_timezones():
    """Obtiene lista de zonas horarias comunes"""
    common_timezones = {
        'America': [
            'America/New_York',
            'America/Chicago',
            'America/Denver',
            'America/Los_Angeles',
            'America/Mexico_City',
            'America/Bogota',
            'America/Lima',
            'America/Santiago',
            'America/Buenos_Aires',
            'America/Sao_Paulo'
        ],
        'Europe': [
            'Europe/London',
            'Europe/Paris',
            'Europe/Madrid',
            'Europe/Berlin',
            'Europe/Rome',
            'Europe/Moscow'
        ],
        'Asia': [
            'Asia/Tokyo',
            'Asia/Shanghai',
            'Asia/Hong_Kong',
            'Asia/Singapore',
            'Asia/Dubai',
            'Asia/Kolkata'
        ],
        'Pacific': [
            'Pacific/Auckland',
            'Australia/Sydney',
            'Pacific/Honolulu'
        ],
        'UTC': ['UTC']
    }
    
    return jsonify({
        'timezones': common_timezones,
        'all_timezones': pytz.all_timezones
    }), 200


@astrology_bp.route('/validate-location', methods=['POST'])
def validate_location():
    """
    Valida coordenadas y zona horaria
    
    Body JSON:
    {
        "latitude": 19.4326,
        "longitude": -99.1332,
        "timezone": "America/Mexico_City"
    }
    """
    try:
        data = request.get_json()
        
        latitude = float(data.get('latitude', 0))
        longitude = float(data.get('longitude', 0))
        timezone_str = data.get('timezone', 'UTC')
        
        errors = []
        
        # Validar latitud
        if not (-90 <= latitude <= 90):
            errors.append('Latitud debe estar entre -90 y 90')
        
        # Validar longitud
        if not (-180 <= longitude <= 180):
            errors.append('Longitud debe estar entre -180 y 180')
        
        # Validar zona horaria
        try:
            tz = pytz.timezone(timezone_str)
            tz_valid = True
        except pytz.exceptions.UnknownTimeZoneError:
            errors.append(f'Zona horaria inválida: {timezone_str}')
            tz_valid = False
        
        if errors:
            return jsonify({
                'valid': False,
                'errors': errors
            }), 400
        
        return jsonify({
            'valid': True,
            'message': 'Ubicación válida',
            'timezone_info': {
                'name': timezone_str,
                'utc_offset': str(tz.utcoffset(datetime.now())) if tz_valid else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al validar ubicación', 'details': str(e)}), 500
