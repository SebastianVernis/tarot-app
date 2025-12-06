"""
Script de prueba para la API de astrología
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def test_astrology_endpoints():
    """Prueba los endpoints de astrología"""
    
    print("="*60)
    print("PRUEBA DE API DE ASTROLOGÍA")
    print("="*60)
    
    # 1. Registrar usuario
    print("\n1. Registrando usuario de prueba...")
    register_data = {
        "email": f"astro{datetime.now().timestamp()}@test.com",
        "username": f"astrouser{int(datetime.now().timestamp())}",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 201:
        print("✓ Usuario registrado exitosamente")
        auth_data = response.json()
        token = auth_data['access_token']
        print(f"  Token obtenido: {token[:50]}...")
    else:
        print(f"✗ Error registrando usuario: {response.json()}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Probar endpoint de información
    print("\n2. Probando endpoint de información...")
    response = requests.get(f"{BASE_URL}/astrology/info")
    if response.status_code == 200:
        print("✓ Información obtenida exitosamente")
        info = response.json()
        print(f"  Servicio: {info['service']}")
        print(f"  Versión: {info['version']}")
        print(f"  Planetas: {len(info['planets'])}")
    else:
        print(f"✗ Error: {response.json()}")
    
    # 3. Calcular posiciones planetarias
    print("\n3. Calculando posiciones planetarias...")
    calc_data = {
        "date": "1990-05-15T14:30:00",
        "latitude": 19.4326,
        "longitude": -99.1332
    }
    
    response = requests.post(
        f"{BASE_URL}/astrology/calculate",
        json=calc_data,
        headers=headers
    )
    
    if response.status_code == 200:
        print("✓ Posiciones calculadas exitosamente")
        result = response.json()
        positions = result['positions']['positions']
        print(f"\n  Fecha: {result['positions']['date']}")
        print(f"  Ubicación: {result['positions']['location']}")
        print("\n  Posiciones planetarias:")
        for planet, data in positions.items():
            retro = " (R)" if data.get('retrograde') else ""
            print(f"    {data['name']}: {data['sign']} {data['position']}{retro}")
    else:
        print(f"✗ Error: {response.json()}")
    
    # 4. Generar carta natal completa (sin interpretación para evitar necesitar API key)
    print("\n4. Generando carta natal completa...")
    chart_data = {
        "birth_date": "1990-05-15T14:30:00",
        "latitude": 19.4326,
        "longitude": -99.1332,
        "location_name": "Ciudad de México",
        "generate_interpretation": False  # Sin interpretación para no necesitar Gemini API
    }
    
    response = requests.post(
        f"{BASE_URL}/astrology/birth-chart",
        json=chart_data,
        headers=headers
    )
    
    if response.status_code == 201:
        print("✓ Carta natal generada exitosamente")
        result = response.json()
        reading = result['reading']
        print(f"\n  ID de lectura: {reading['id']}")
        print(f"  Fecha de nacimiento: {reading['birth_date']}")
        print(f"  Ubicación: {reading['birth_location']['name']}")
        print(f"\n  Resumen:")
        print(f"    Signo Solar: {reading['summary']['sun_sign']}")
        print(f"    Signo Lunar: {reading['summary']['moon_sign']}")
        print(f"    Signo Ascendente: {reading['summary']['rising_sign']}")
        
        # Mostrar algunos planetas
        if 'chart_data' in reading:
            print(f"\n  Planetas:")
            for planet_key, planet_data in list(reading['chart_data']['planets'].items())[:5]:
                retro = " (R)" if planet_data.get('retrograde') else ""
                print(f"    {planet_data['name']}: {planet_data['position']}{retro}")
            
            # Mostrar aspectos
            if reading['chart_data']['aspects']:
                print(f"\n  Aspectos principales:")
                for aspect in reading['chart_data']['aspects'][:3]:
                    print(f"    {aspect['planet1']} {aspect['aspect']} {aspect['planet2']} (orbe: {aspect['orb']}°)")
    else:
        print(f"✗ Error: {response.json()}")
    
    # 5. Obtener lecturas guardadas
    print("\n5. Obteniendo lecturas guardadas...")
    response = requests.get(
        f"{BASE_URL}/astrology/readings",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✓ Lecturas obtenidas exitosamente")
        result = response.json()
        print(f"  Total de lecturas: {result['pagination']['total']}")
        if result['readings']:
            print(f"  Primera lectura:")
            reading = result['readings'][0]
            print(f"    ID: {reading['id']}")
            print(f"    Tipo: {reading['reading_type']}")
            print(f"    Signo Solar: {reading['summary']['sun_sign']}")
    else:
        print(f"✗ Error: {response.json()}")
    
    print("\n" + "="*60)
    print("PRUEBAS COMPLETADAS")
    print("="*60)


if __name__ == "__main__":
    try:
        test_astrology_endpoints()
    except Exception as e:
        print(f"\n✗ Error en las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()
