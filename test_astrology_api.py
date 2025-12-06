"""
Script de prueba para endpoints de API de astrología
"""
import json


def test_api_endpoints():
    """Muestra ejemplos de uso de los endpoints de API"""
    
    print("\n" + "="*70)
    print("EJEMPLOS DE USO - API DE ASTROLOGÍA")
    print("="*70)
    
    print("\n1. CALCULAR CARTA NATAL")
    print("-" * 70)
    print("POST /api/astrology/birth-chart")
    print("\nHeaders:")
    print("  Authorization: Bearer <token>")
    print("  Content-Type: application/json")
    print("\nBody:")
    birth_chart_request = {
        "birth_datetime": "1990-05-15T14:30:00",
        "timezone": "America/Mexico_City",
        "latitude": 19.4326,
        "longitude": -99.1332,
        "location_name": "Ciudad de México",
        "house_system": "P",
        "include_interpretations": True,
        "name": "Mi Carta Natal"
    }
    print(json.dumps(birth_chart_request, indent=2))
    
    print("\n\n2. OBTENER CARTA NATAL")
    print("-" * 70)
    print("GET /api/astrology/birth-chart/<chart_id>")
    print("\nHeaders:")
    print("  Authorization: Bearer <token>")
    
    print("\n\n3. LISTAR CARTAS NATALES")
    print("-" * 70)
    print("GET /api/astrology/birth-charts?page=1&per_page=20")
    print("\nHeaders:")
    print("  Authorization: Bearer <token>")
    
    print("\n\n4. CALCULAR ASPECTOS")
    print("-" * 70)
    print("POST /api/astrology/aspects")
    print("\nHeaders:")
    print("  Authorization: Bearer <token>")
    print("  Content-Type: application/json")
    print("\nBody:")
    aspects_request = {
        "planetary_positions": {
            "0": {"longitude": 54.5, "name": "Sol"},
            "1": {"longitude": 298.45, "name": "Luna"},
            "2": {"longitude": 38.0, "name": "Mercurio"}
        },
        "include_minor": True
    }
    print(json.dumps(aspects_request, indent=2))
    
    print("\n\n5. GENERAR INTERPRETACIÓN")
    print("-" * 70)
    print("POST /api/astrology/interpret")
    print("\nHeaders:")
    print("  Authorization: Bearer <token>")
    print("  Content-Type: application/json")
    print("\nBody (ejemplo para posición en casa):")
    interpret_house = {
        "type": "house_placement",
        "data": {
            "planet_name": "Sol",
            "house_number": 10,
            "sign": "Capricornio",
            "degree": 15.5
        }
    }
    print(json.dumps(interpret_house, indent=2))
    
    print("\n\nBody (ejemplo para aspecto):")
    interpret_aspect = {
        "type": "aspect",
        "data": {
            "planet1_name": "Sol",
            "planet2_name": "Luna",
            "aspect_name": "Trígono",
            "aspect_angle": 120,
            "orb": 2.5,
            "nature": "harmonious"
        }
    }
    print(json.dumps(interpret_aspect, indent=2))
    
    print("\n\n6. INTERPRETAR CARTA NATAL COMPLETA")
    print("-" * 70)
    print("POST /api/astrology/birth-chart/<chart_id>/interpret")
    print("\nHeaders:")
    print("  Authorization: Bearer <token>")
    print("  Content-Type: application/json")
    print("\nBody (opcional):")
    interpret_chart = {
        "question": "¿Cuál es mi propósito de vida?"
    }
    print(json.dumps(interpret_chart, indent=2))
    
    print("\n\n7. OBTENER SISTEMAS DE CASAS")
    print("-" * 70)
    print("GET /api/astrology/house-systems")
    print("\nNo requiere autenticación")
    
    print("\n\n8. OBTENER ZONAS HORARIAS")
    print("-" * 70)
    print("GET /api/astrology/timezones")
    print("\nNo requiere autenticación")
    
    print("\n\n9. VALIDAR UBICACIÓN")
    print("-" * 70)
    print("POST /api/astrology/validate-location")
    print("\nHeaders:")
    print("  Content-Type: application/json")
    print("\nBody:")
    validate_location = {
        "latitude": 19.4326,
        "longitude": -99.1332,
        "timezone": "America/Mexico_City"
    }
    print(json.dumps(validate_location, indent=2))
    
    print("\n\n" + "="*70)
    print("COMANDOS CURL DE EJEMPLO")
    print("="*70)
    
    print("\n# Calcular carta natal")
    print('curl -X POST http://localhost:5000/api/astrology/birth-chart \\')
    print('  -H "Authorization: Bearer YOUR_TOKEN" \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"birth_datetime":"1990-05-15T14:30:00","timezone":"America/Mexico_City","latitude":19.4326,"longitude":-99.1332,"location_name":"Ciudad de México","house_system":"P","include_interpretations":false}\'')
    
    print("\n\n# Obtener sistemas de casas")
    print('curl http://localhost:5000/api/astrology/house-systems')
    
    print("\n\n# Validar ubicación")
    print('curl -X POST http://localhost:5000/api/astrology/validate-location \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"latitude":19.4326,"longitude":-99.1332,"timezone":"America/Mexico_City"}\'')
    
    print("\n\n" + "="*70)
    print("NOTAS IMPORTANTES")
    print("="*70)
    print("""
1. La mayoría de endpoints requieren autenticación JWT
2. Para usar interpretaciones con Gemini, configure GEMINI_API_KEY en .env
3. Los sistemas de casas disponibles son:
   - P: Placidus (más popular)
   - K: Koch
   - E: Equal House (Casas Iguales)
   - W: Whole Sign (Signos Completos)
   - C: Campanus
   - R: Regiomontanus

4. Formatos de fecha: ISO 8601 (YYYY-MM-DDTHH:MM:SS)
5. Coordenadas: Latitud (-90 a 90), Longitud (-180 a 180)
6. Zonas horarias: Formato IANA (ej: America/Mexico_City, Europe/Madrid)
    """)
    
    print("\n" + "="*70)
    print("✓ DOCUMENTACIÓN DE API GENERADA")
    print("="*70)


if __name__ == '__main__':
    test_api_endpoints()
