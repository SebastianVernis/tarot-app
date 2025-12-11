"""
Script de prueba para validar cálculos astrológicos
"""
from datetime import datetime
from src.astrology_calculator import (
    AstrologyCalculator,
    HouseSystem,
    Planet,
    Aspect,
    ZodiacSign
)
import json


def test_planetary_positions():
    """Prueba cálculo de posiciones planetarias"""
    print("\n" + "="*70)
    print("TEST 1: POSICIONES PLANETARIAS")
    print("="*70)
    
    calculator = AstrologyCalculator()
    
    # Fecha de prueba: 15 de mayo de 1990, 14:30 UTC
    test_date = datetime(1990, 5, 15, 14, 30, 0)
    
    jd = calculator.calculate_julian_day(test_date, 'UTC')
    print(f"\nFecha de prueba: {test_date}")
    print(f"Día Juliano: {jd}")
    
    positions = calculator.calculate_planetary_positions(jd)
    
    print("\nPosiciones planetarias:")
    for planet_id, data in positions.items():
        print(f"\n{data['symbol']} {data['name']}:")
        print(f"  Signo: {data['sign_symbol']} {data['sign']}")
        print(f"  Grado: {data['degree_in_sign']:.2f}°")
        print(f"  Longitud: {data['longitude']:.2f}°")
        if 'retrograde' in data:
            print(f"  Retrógrado: {'Sí' if data['retrograde'] else 'No'}")
    
    return positions


def test_house_calculation():
    """Prueba cálculo de casas"""
    print("\n" + "="*70)
    print("TEST 2: CÁLCULO DE CASAS")
    print("="*70)
    
    calculator = AstrologyCalculator()
    
    # Fecha y lugar de prueba: Ciudad de México
    test_date = datetime(1990, 5, 15, 14, 30, 0)
    latitude = 19.4326
    longitude = -99.1332
    
    jd = calculator.calculate_julian_day(test_date, 'America/Mexico_City')
    
    print(f"\nFecha: {test_date}")
    print(f"Lugar: Ciudad de México ({latitude}, {longitude})")
    
    # Probar diferentes sistemas de casas
    systems = [
        (HouseSystem.PLACIDUS, "Placidus"),
        (HouseSystem.KOCH, "Koch"),
        (HouseSystem.EQUAL, "Casas Iguales")
    ]
    
    for system_code, system_name in systems:
        print(f"\n--- Sistema: {system_name} ---")
        houses = calculator.calculate_houses(jd, latitude, longitude, system_code)
        
        print(f"\nAscendente: {houses['ascendant']['sign_symbol']} {houses['ascendant']['sign']} "
              f"{houses['ascendant']['degree_in_sign']:.2f}°")
        print(f"Medio Cielo: {houses['midheaven']['sign_symbol']} {houses['midheaven']['sign']} "
              f"{houses['midheaven']['degree_in_sign']:.2f}°")
        
        print("\nCúspides de las casas:")
        for i in range(1, 13):
            house = houses['houses'][i]
            print(f"  Casa {i:2d}: {house['sign_symbol']} {house['sign']} {house['degree_in_sign']:.2f}°")
    
    return houses


def test_aspects():
    """Prueba detección de aspectos"""
    print("\n" + "="*70)
    print("TEST 3: DETECCIÓN DE ASPECTOS")
    print("="*70)
    
    calculator = AstrologyCalculator()
    
    test_date = datetime(1990, 5, 15, 14, 30, 0)
    jd = calculator.calculate_julian_day(test_date, 'UTC')
    
    positions = calculator.calculate_planetary_positions(jd)
    aspects = calculator.calculate_aspects(positions, include_minor=True)
    
    print(f"\nTotal de aspectos encontrados: {len(aspects)}")
    
    # Mostrar aspectos mayores
    major_aspects = [a for a in aspects if a['nature'] in ['harmonious', 'challenging', 'neutral']]
    print(f"\nAspectos mayores: {len(major_aspects)}")
    
    for aspect in major_aspects[:10]:  # Mostrar primeros 10
        p1 = aspect['planet1']
        p2 = aspect['planet2']
        print(f"\n{p1['symbol']} {p1['name']} {aspect['aspect_symbol']} {p2['symbol']} {p2['name']}")
        print(f"  Tipo: {aspect['aspect']} ({aspect['angle']}°)")
        print(f"  Orbe: {aspect['orb']:.2f}° (máx: {aspect['max_orb']}°)")
        print(f"  Naturaleza: {aspect['nature']}")
        print(f"  Aplicando: {'Sí' if aspect['applying'] else 'No'}")
    
    return aspects


def test_full_birth_chart():
    """Prueba carta natal completa"""
    print("\n" + "="*70)
    print("TEST 4: CARTA NATAL COMPLETA")
    print("="*70)
    
    calculator = AstrologyCalculator()
    
    # Datos de prueba
    birth_date = datetime(1990, 5, 15, 14, 30, 0)
    latitude = 19.4326
    longitude = -99.1332
    timezone = 'America/Mexico_City'
    
    print(f"\nCalculando carta natal para:")
    print(f"  Fecha: {birth_date}")
    print(f"  Lugar: Ciudad de México")
    print(f"  Coordenadas: {latitude}, {longitude}")
    print(f"  Zona horaria: {timezone}")
    
    chart = calculator.calculate_birth_chart(
        birth_date,
        latitude,
        longitude,
        timezone,
        HouseSystem.PLACIDUS,
        include_minor_aspects=True
    )
    
    summary = chart['chart_summary']
    
    print("\n--- RESUMEN DE LA CARTA ---")
    print(f"\nSol: {summary['sun_sign']}")
    print(f"Luna: {summary['moon_sign']}")
    print(f"Ascendente: {summary['ascendant']['sign']}")
    print(f"Medio Cielo: {summary['midheaven']['sign']}")
    
    print(f"\nElementos:")
    for element, count in summary['elements'].items():
        print(f"  {element}: {count}")
    print(f"Elemento dominante: {summary['dominant_element']}")
    
    print(f"\nAspectos:")
    for nature, count in summary['aspect_counts'].items():
        print(f"  {nature}: {count}")
    
    if summary['retrograde_planets']:
        print(f"\nPlanetas retrógrados: {', '.join(summary['retrograde_planets'])}")
    else:
        print("\nNo hay planetas retrógrados")
    
    # Planetas en casas
    planets_in_houses = chart['planets_in_houses']
    print("\n--- PLANETAS EN CASAS ---")
    for house_num in range(1, 13):
        planets = planets_in_houses[house_num]
        if planets:
            print(f"\nCasa {house_num}:")
            for planet in planets:
                print(f"  {planet['symbol']} {planet['name']} en {planet['sign']} "
                      f"{planet['degree_in_sign']:.2f}°")
    
    return chart


def test_known_birth_chart():
    """Prueba con una carta natal conocida para validación"""
    print("\n" + "="*70)
    print("TEST 5: VALIDACIÓN CON CARTA CONOCIDA")
    print("="*70)
    print("\nUsando datos de Albert Einstein:")
    print("  Nacimiento: 14 de marzo de 1879, 11:30 AM")
    print("  Lugar: Ulm, Alemania (48.4°N, 9.99°E)")
    
    calculator = AstrologyCalculator()
    
    birth_date = datetime(1879, 3, 14, 11, 30, 0)
    latitude = 48.4
    longitude = 9.99
    
    chart = calculator.calculate_birth_chart(
        birth_date,
        latitude,
        longitude,
        'Europe/Berlin',
        HouseSystem.PLACIDUS
    )
    
    summary = chart['chart_summary']
    
    print("\nResultados:")
    print(f"  Sol: {summary['sun_sign']} (esperado: Piscis)")
    print(f"  Luna: {summary['moon_sign']}")
    print(f"  Ascendente: {summary['ascendant']['sign']}")
    
    # Validar que el Sol esté en Piscis
    if summary['sun_sign'] == 'Piscis':
        print("\n✓ VALIDACIÓN EXITOSA: Sol en Piscis confirmado")
    else:
        print("\n✗ ERROR: Sol debería estar en Piscis")
    
    return chart


def save_test_results(chart):
    """Guarda resultados de prueba en JSON"""
    print("\n" + "="*70)
    print("GUARDANDO RESULTADOS")
    print("="*70)
    
    # Convertir a formato serializable
    def convert_to_serializable(obj):
        if isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        else:
            return str(obj)
    
    serializable_chart = convert_to_serializable(chart)
    
    with open('test_birth_chart_result.json', 'w', encoding='utf-8') as f:
        json.dump(serializable_chart, f, indent=2, ensure_ascii=False)
    
    print("\nResultados guardados en: test_birth_chart_result.json")


def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*70)
    print("SUITE DE PRUEBAS - SISTEMA ASTROLÓGICO")
    print("="*70)
    
    try:
        # Test 1: Posiciones planetarias
        positions = test_planetary_positions()
        
        # Test 2: Cálculo de casas
        houses = test_house_calculation()
        
        # Test 3: Aspectos
        aspects = test_aspects()
        
        # Test 4: Carta natal completa
        chart = test_full_birth_chart()
        
        # Test 5: Validación con carta conocida
        einstein_chart = test_known_birth_chart()
        
        # Guardar resultados
        save_test_results(chart)
        
        print("\n" + "="*70)
        print("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("="*70)
        
    except Exception as e:
        print("\n" + "="*70)
        print("✗ ERROR EN LAS PRUEBAS")
        print("="*70)
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
