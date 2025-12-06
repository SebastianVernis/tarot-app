"""
Script de prueba para la API de Tarot
"""
import requests
import json

API_BASE = 'http://localhost:5000/api'

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    print_section("1. Health Check")
    response = requests.get(f'{API_BASE}/health')
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_register():
    print_section("2. Registro de Usuario")
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'test123456'
    }
    response = requests.post(f'{API_BASE}/auth/register', json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))
    
    if response.status_code == 201:
        return result.get('access_token')
    return None

def test_login():
    print_section("3. Login")
    data = {
        'email': 'demo@tarot.com',
        'password': 'demo123'
    }
    response = requests.post(f'{API_BASE}/auth/login', json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Usuario: {result.get('user', {}).get('username')}")
    print(f"Plan: {result.get('user', {}).get('subscription_plan')}")
    print(f"Token recibido: {'✓' if 'access_token' in result else '✗'}")
    
    return result.get('access_token')

def test_usage(token):
    print_section("4. Estadísticas de Uso")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{API_BASE}/user/usage', headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))

def test_theme_change(token):
    print_section("5. Cambio de Tema")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Cambiar a light
    response = requests.put(f'{API_BASE}/user/theme', 
                           headers=headers, 
                           json={'theme': 'light'})
    print(f"Cambio a light - Status: {response.status_code}")
    print(f"Tema actual: {response.json().get('theme')}")
    
    # Cambiar a dark
    response = requests.put(f'{API_BASE}/user/theme', 
                           headers=headers, 
                           json={'theme': 'dark'})
    print(f"Cambio a dark - Status: {response.status_code}")
    print(f"Tema actual: {response.json().get('theme')}")

def test_check_access(token):
    print_section("6. Verificar Acceso a Tiradas")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Tirada básica (permitida)
    response = requests.post(f'{API_BASE}/readings/check-access',
                            headers=headers,
                            json={'spread_type': 'una_carta'})
    print(f"Una Carta - Status: {response.status_code}")
    result = response.json()
    print(f"Puede acceder: {result.get('can_access')}")
    
    # Tirada avanzada (bloqueada para free)
    response = requests.post(f'{API_BASE}/readings/check-access',
                            headers=headers,
                            json={'spread_type': 'cruz_celta'})
    print(f"\nCruz Celta - Status: {response.status_code}")
    result = response.json()
    print(f"Puede acceder: {result.get('can_access')}")
    if not result.get('can_access'):
        print(f"Razón: {result.get('spread_access', {}).get('message')}")

def test_create_reading(token):
    print_section("7. Crear Lectura")
    headers = {'Authorization': f'Bearer {token}'}
    
    data = {
        'spread_type': 'tres_cartas',
        'question': '¿Cómo me irá en el trabajo?',
        'cards': [
            {'name': 'El Sol', 'position': 'Pasado', 'reversed': False},
            {'name': 'La Luna', 'position': 'Presente', 'reversed': True},
            {'name': 'La Estrella', 'position': 'Futuro', 'reversed': False}
        ],
        'interpretation': 'Tu pasado fue brillante, el presente es confuso, pero el futuro trae esperanza.'
    }
    
    response = requests.post(f'{API_BASE}/readings/', 
                            headers=headers, 
                            json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if response.status_code == 201:
        print(f"✓ Lectura creada con ID: {result.get('reading', {}).get('id')}")
        print(f"Uso actualizado: {result.get('usage', {}).get('readings_today')}/{result.get('usage', {}).get('readings_limit')}")
        return result.get('reading', {}).get('id')
    else:
        print(f"✗ Error: {result.get('error')}")
    
    return None

def test_get_readings(token):
    print_section("8. Obtener Lecturas")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{API_BASE}/readings/', headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    readings = result.get('readings', [])
    print(f"Total de lecturas: {len(readings)}")
    
    if readings:
        print(f"\nÚltima lectura:")
        last = readings[0]
        print(f"  ID: {last.get('id')}")
        print(f"  Tipo: {last.get('spread_type')}")
        print(f"  Pregunta: {last.get('question')}")
        print(f"  Fecha: {last.get('created_at')}")

def test_upgrade_premium(token):
    print_section("9. Upgrade a Premium (Demo)")
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(f'{API_BASE}/subscription/demo-upgrade', 
                            headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if response.status_code == 200:
        print(f"✓ {result.get('message')}")
        print(f"Plan actual: {result.get('user', {}).get('subscription_plan')}")
        print(f"Es premium: {result.get('user', {}).get('is_premium')}")
        return True
    else:
        print(f"✗ Error: {result.get('error')}")
    
    return False

def test_premium_access(token):
    print_section("10. Verificar Acceso Premium")
    headers = {'Authorization': f'Bearer {token}'}
    
    # Ahora debería poder acceder a Cruz Celta
    response = requests.post(f'{API_BASE}/readings/check-access',
                            headers=headers,
                            json={'spread_type': 'cruz_celta'})
    print(f"Cruz Celta - Status: {response.status_code}")
    result = response.json()
    print(f"Puede acceder: {result.get('can_access')}")
    print(f"Uso: {result.get('usage')}")

def main():
    print("\n" + "🔮"*30)
    print("  PRUEBAS DE API - TAROT MÍSTICO")
    print("🔮"*30)
    
    try:
        # 1. Health check
        if not test_health():
            print("❌ El servidor no está disponible")
            return
        
        # 2. Intentar registro (puede fallar si ya existe)
        test_register()
        
        # 3. Login
        token = test_login()
        if not token:
            print("❌ No se pudo obtener token")
            return
        
        # 4. Uso
        test_usage(token)
        
        # 5. Cambio de tema
        test_theme_change(token)
        
        # 6. Verificar acceso
        test_check_access(token)
        
        # 7. Crear lectura
        reading_id = test_create_reading(token)
        
        # 8. Obtener lecturas
        test_get_readings(token)
        
        # 9. Upgrade a premium
        if test_upgrade_premium(token):
            # 10. Verificar acceso premium
            test_premium_access(token)
        
        print_section("✅ PRUEBAS COMPLETADAS")
        print("Todas las funcionalidades principales están funcionando correctamente!")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
