"""
Módulo de cálculos astrológicos precisos
Utiliza Swiss Ephemeris para cálculos de posiciones planetarias
"""
import swisseph as swe
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pytz
from timezonefinder import TimezoneFinder
import math


class AstrologyCalculator:
    """Calculadora de posiciones planetarias y carta natal"""
    
    # Planetas a calcular (códigos Swiss Ephemeris)
    PLANETS = {
        'sun': swe.SUN,
        'moon': swe.MOON,
        'mercury': swe.MERCURY,
        'venus': swe.VENUS,
        'mars': swe.MARS,
        'jupiter': swe.JUPITER,
        'saturn': swe.SATURN,
        'uranus': swe.URANUS,
        'neptune': swe.NEPTUNE,
        'pluto': swe.PLUTO
    }
    
    # Nombres en español
    PLANET_NAMES_ES = {
        'sun': 'Sol',
        'moon': 'Luna',
        'mercury': 'Mercurio',
        'venus': 'Venus',
        'mars': 'Marte',
        'jupiter': 'Júpiter',
        'saturn': 'Saturno',
        'uranus': 'Urano',
        'neptune': 'Neptuno',
        'pluto': 'Plutón'
    }
    
    # Signos zodiacales
    ZODIAC_SIGNS = [
        'Aries', 'Tauro', 'Géminis', 'Cáncer', 'Leo', 'Virgo',
        'Libra', 'Escorpio', 'Sagitario', 'Capricornio', 'Acuario', 'Piscis'
    ]
    
    # Símbolos de signos
    ZODIAC_SYMBOLS = {
        'Aries': '♈', 'Tauro': '♉', 'Géminis': '♊', 'Cáncer': '♋',
        'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Escorpio': '♏',
        'Sagitario': '♐', 'Capricornio': '♑', 'Acuario': '♒', 'Piscis': '♓'
    }
    
    # Elementos
    ELEMENTS = {
        'Aries': 'Fuego', 'Leo': 'Fuego', 'Sagitario': 'Fuego',
        'Tauro': 'Tierra', 'Virgo': 'Tierra', 'Capricornio': 'Tierra',
        'Géminis': 'Aire', 'Libra': 'Aire', 'Acuario': 'Aire',
        'Cáncer': 'Agua', 'Escorpio': 'Agua', 'Piscis': 'Agua'
    }
    
    # Modalidades
    MODALITIES = {
        'Aries': 'Cardinal', 'Cáncer': 'Cardinal', 'Libra': 'Cardinal', 'Capricornio': 'Cardinal',
        'Tauro': 'Fijo', 'Leo': 'Fijo', 'Escorpio': 'Fijo', 'Acuario': 'Fijo',
        'Géminis': 'Mutable', 'Virgo': 'Mutable', 'Sagitario': 'Mutable', 'Piscis': 'Mutable'
    }
    
    def __init__(self):
        """Inicializa el calculador astrológico"""
        # Configurar Swiss Ephemeris para usar datos incluidos
        swe.set_ephe_path(None)  # Usa datos incluidos en la biblioteca
        self.tf = TimezoneFinder()
    
    def get_timezone(self, latitude: float, longitude: float) -> str:
        """Obtiene la zona horaria basada en coordenadas"""
        try:
            tz_name = self.tf.timezone_at(lat=latitude, lng=longitude)
            return tz_name if tz_name else 'UTC'
        except Exception:
            return 'UTC'
    
    def datetime_to_julian_day(self, dt: datetime) -> float:
        """Convierte datetime a día juliano"""
        year = dt.year
        month = dt.month
        day = dt.day
        hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
        
        jd = swe.julday(year, month, day, hour)
        return jd
    
    def degrees_to_dms(self, degrees: float) -> Tuple[int, int, int]:
        """Convierte grados decimales a grados, minutos, segundos"""
        d = int(degrees)
        m = int((degrees - d) * 60)
        s = int(((degrees - d) * 60 - m) * 60)
        return d, m, s
    
    def position_to_zodiac(self, longitude: float) -> Dict:
        """Convierte longitud eclíptica a signo zodiacal con grados"""
        # Normalizar a 0-360
        longitude = longitude % 360
        
        # Calcular signo (cada signo = 30 grados)
        sign_index = int(longitude / 30)
        sign = self.ZODIAC_SIGNS[sign_index]
        
        # Grados dentro del signo
        degrees_in_sign = longitude % 30
        deg, min, sec = self.degrees_to_dms(degrees_in_sign)
        
        return {
            'sign': sign,
            'symbol': self.ZODIAC_SYMBOLS[sign],
            'degrees': deg,
            'minutes': min,
            'seconds': sec,
            'absolute_position': longitude,
            'element': self.ELEMENTS[sign],
            'modality': self.MODALITIES[sign],
            'formatted': f"{sign} {deg}° {min}' {sec}\""
        }
    
    def calculate_planet_position(self, planet_code: int, julian_day: float) -> Dict:
        """Calcula la posición de un planeta"""
        try:
            # Calcular posición (geocéntrica, tropical)
            result = swe.calc_ut(julian_day, planet_code)
            longitude = result[0][0]  # Longitud eclíptica
            latitude = result[0][1]   # Latitud eclíptica
            distance = result[0][2]   # Distancia
            speed = result[0][3]      # Velocidad
            
            # Convertir a signo zodiacal
            zodiac_info = self.position_to_zodiac(longitude)
            
            # Determinar si está retrógrado
            is_retrograde = speed < 0
            
            return {
                'longitude': longitude,
                'latitude': latitude,
                'distance': distance,
                'speed': speed,
                'is_retrograde': is_retrograde,
                'zodiac': zodiac_info
            }
        except Exception as e:
            raise Exception(f"Error calculando posición planetaria: {str(e)}")
    
    def calculate_houses(self, julian_day: float, latitude: float, longitude: float) -> Dict:
        """Calcula las casas astrológicas y puntos importantes"""
        try:
            # Calcular casas usando sistema Placidus (más común)
            houses, ascmc = swe.houses(julian_day, latitude, longitude, b'P')
            
            # Ascendente (ASC)
            ascendant = ascmc[0]
            asc_zodiac = self.position_to_zodiac(ascendant)
            
            # Medio Cielo (MC)
            midheaven = ascmc[1]
            mc_zodiac = self.position_to_zodiac(midheaven)
            
            # Descendente (DSC) - opuesto al ascendente
            descendant = (ascendant + 180) % 360
            dsc_zodiac = self.position_to_zodiac(descendant)
            
            # Fondo del Cielo (IC) - opuesto al MC
            imum_coeli = (midheaven + 180) % 360
            ic_zodiac = self.position_to_zodiac(imum_coeli)
            
            # Casas (12 casas)
            house_cusps = []
            for i, house_cusp in enumerate(houses, 1):
                house_cusps.append({
                    'house': i,
                    'cusp': house_cusp,
                    'zodiac': self.position_to_zodiac(house_cusp)
                })
            
            return {
                'ascendant': {
                    'position': ascendant,
                    'zodiac': asc_zodiac
                },
                'midheaven': {
                    'position': midheaven,
                    'zodiac': mc_zodiac
                },
                'descendant': {
                    'position': descendant,
                    'zodiac': dsc_zodiac
                },
                'imum_coeli': {
                    'position': imum_coeli,
                    'zodiac': ic_zodiac
                },
                'houses': house_cusps
            }
        except Exception as e:
            raise Exception(f"Error calculando casas: {str(e)}")
    
    def calculate_aspects(self, positions: Dict) -> List[Dict]:
        """Calcula aspectos entre planetas"""
        aspects = []
        
        # Definir aspectos y sus orbes
        aspect_definitions = {
            'Conjunción': (0, 8),
            'Oposición': (180, 8),
            'Trígono': (120, 8),
            'Cuadratura': (90, 8),
            'Sextil': (60, 6),
            'Quincuncio': (150, 3),
            'Semisextil': (30, 3)
        }
        
        planet_list = list(positions.keys())
        
        for i, planet1 in enumerate(planet_list):
            for planet2 in planet_list[i+1:]:
                pos1 = positions[planet1]['longitude']
                pos2 = positions[planet2]['longitude']
                
                # Calcular diferencia angular
                diff = abs(pos1 - pos2)
                if diff > 180:
                    diff = 360 - diff
                
                # Verificar cada tipo de aspecto
                for aspect_name, (angle, orb) in aspect_definitions.items():
                    if abs(diff - angle) <= orb:
                        aspects.append({
                            'planet1': self.PLANET_NAMES_ES[planet1],
                            'planet2': self.PLANET_NAMES_ES[planet2],
                            'aspect': aspect_name,
                            'angle': angle,
                            'actual_angle': round(diff, 2),
                            'orb': round(abs(diff - angle), 2)
                        })
        
        return aspects
    
    def calculate_birth_chart(
        self,
        birth_date: datetime,
        latitude: float,
        longitude: float,
        timezone_str: Optional[str] = None
    ) -> Dict:
        """
        Calcula la carta natal completa
        
        Args:
            birth_date: Fecha y hora de nacimiento (datetime)
            latitude: Latitud del lugar de nacimiento
            longitude: Longitud del lugar de nacimiento
            timezone_str: Zona horaria (opcional, se detecta automáticamente)
        
        Returns:
            Diccionario con toda la información de la carta natal
        """
        try:
            # Obtener zona horaria si no se proporciona
            if not timezone_str:
                timezone_str = self.get_timezone(latitude, longitude)
            
            # Convertir a UTC si tiene zona horaria
            if birth_date.tzinfo is None:
                # Asumir que está en la zona horaria local
                local_tz = pytz.timezone(timezone_str)
                birth_date = local_tz.localize(birth_date)
            
            birth_date_utc = birth_date.astimezone(pytz.UTC)
            
            # Convertir a día juliano
            julian_day = self.datetime_to_julian_day(birth_date_utc)
            
            # Calcular posiciones planetarias
            planetary_positions = {}
            for planet_key, planet_code in self.PLANETS.items():
                position = self.calculate_planet_position(planet_code, julian_day)
                planetary_positions[planet_key] = position
            
            # Calcular casas y puntos importantes
            houses_data = self.calculate_houses(julian_day, latitude, longitude)
            
            # Calcular aspectos
            aspects = self.calculate_aspects(planetary_positions)
            
            # Crear resumen de planetas por signo
            planets_by_sign = {}
            for planet_key, position in planetary_positions.items():
                sign = position['zodiac']['sign']
                planet_name = self.PLANET_NAMES_ES[planet_key]
                
                if sign not in planets_by_sign:
                    planets_by_sign[sign] = []
                
                planets_by_sign[sign].append({
                    'planet': planet_name,
                    'position': position['zodiac']['formatted'],
                    'retrograde': position['is_retrograde']
                })
            
            # Calcular elemento dominante
            element_count = {}
            for position in planetary_positions.values():
                element = position['zodiac']['element']
                element_count[element] = element_count.get(element, 0) + 1
            
            dominant_element = max(element_count, key=element_count.get)
            
            # Calcular modalidad dominante
            modality_count = {}
            for position in planetary_positions.values():
                modality = position['zodiac']['modality']
                modality_count[modality] = modality_count.get(modality, 0) + 1
            
            dominant_modality = max(modality_count, key=modality_count.get)
            
            return {
                'birth_data': {
                    'date': birth_date.isoformat(),
                    'date_utc': birth_date_utc.isoformat(),
                    'latitude': latitude,
                    'longitude': longitude,
                    'timezone': timezone_str,
                    'julian_day': julian_day
                },
                'planets': {
                    planet_key: {
                        'name': self.PLANET_NAMES_ES[planet_key],
                        'position': position['zodiac']['formatted'],
                        'sign': position['zodiac']['sign'],
                        'symbol': position['zodiac']['symbol'],
                        'degrees': position['zodiac']['degrees'],
                        'minutes': position['zodiac']['minutes'],
                        'element': position['zodiac']['element'],
                        'modality': position['zodiac']['modality'],
                        'retrograde': position['is_retrograde'],
                        'longitude': position['longitude']
                    }
                    for planet_key, position in planetary_positions.items()
                },
                'houses': houses_data,
                'aspects': aspects,
                'summary': {
                    'sun_sign': planetary_positions['sun']['zodiac']['sign'],
                    'moon_sign': planetary_positions['moon']['zodiac']['sign'],
                    'rising_sign': houses_data['ascendant']['zodiac']['sign'],
                    'dominant_element': dominant_element,
                    'dominant_modality': dominant_modality,
                    'element_distribution': element_count,
                    'modality_distribution': modality_count,
                    'planets_by_sign': planets_by_sign,
                    'retrograde_planets': [
                        self.PLANET_NAMES_ES[k] for k, v in planetary_positions.items()
                        if v['is_retrograde']
                    ]
                }
            }
        except Exception as e:
            raise Exception(f"Error calculando carta natal: {str(e)}")
    
    def calculate_planetary_positions(
        self,
        date: datetime,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        Calcula solo las posiciones planetarias (versión simplificada)
        
        Args:
            date: Fecha y hora
            latitude: Latitud
            longitude: Longitud
        
        Returns:
            Diccionario con posiciones planetarias
        """
        try:
            # Convertir a UTC
            if date.tzinfo is None:
                timezone_str = self.get_timezone(latitude, longitude)
                local_tz = pytz.timezone(timezone_str)
                date = local_tz.localize(date)
            
            date_utc = date.astimezone(pytz.UTC)
            julian_day = self.datetime_to_julian_day(date_utc)
            
            # Calcular posiciones
            positions = {}
            for planet_key, planet_code in self.PLANETS.items():
                position = self.calculate_planet_position(planet_code, julian_day)
                positions[planet_key] = {
                    'name': self.PLANET_NAMES_ES[planet_key],
                    'sign': position['zodiac']['sign'],
                    'position': position['zodiac']['formatted'],
                    'degrees': position['zodiac']['degrees'],
                    'minutes': position['zodiac']['minutes'],
                    'retrograde': position['is_retrograde']
                }
            
            return {
                'date': date.isoformat(),
                'location': {
                    'latitude': latitude,
                    'longitude': longitude
                },
                'positions': positions
            }
        except Exception as e:
            raise Exception(f"Error calculando posiciones: {str(e)}")


# Función de utilidad para pruebas rápidas
def test_calculation():
    """Función de prueba con fecha conocida"""
    calc = AstrologyCalculator()
    
    # Fecha de prueba: 1 de enero de 2000, 00:00 UTC
    test_date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
    
    # Ciudad de México
    latitude = 19.4326
    longitude = -99.1332
    
    print("Calculando carta natal de prueba...")
    print(f"Fecha: {test_date}")
    print(f"Ubicación: Ciudad de México ({latitude}, {longitude})")
    print("-" * 60)
    
    try:
        chart = calc.calculate_birth_chart(test_date, latitude, longitude)
        
        print("\n=== POSICIONES PLANETARIAS ===")
        for planet_key, planet_data in chart['planets'].items():
            retro = " (R)" if planet_data['retrograde'] else ""
            print(f"{planet_data['name']}: {planet_data['position']}{retro}")
        
        print("\n=== PUNTOS IMPORTANTES ===")
        print(f"Ascendente: {chart['houses']['ascendant']['zodiac']['formatted']}")
        print(f"Medio Cielo: {chart['houses']['midheaven']['zodiac']['formatted']}")
        
        print("\n=== RESUMEN ===")
        print(f"Signo Solar: {chart['summary']['sun_sign']}")
        print(f"Signo Lunar: {chart['summary']['moon_sign']}")
        print(f"Signo Ascendente: {chart['summary']['rising_sign']}")
        print(f"Elemento Dominante: {chart['summary']['dominant_element']}")
        print(f"Modalidad Dominante: {chart['summary']['dominant_modality']}")
        
        if chart['summary']['retrograde_planets']:
            print(f"\nPlanetas Retrógrados: {', '.join(chart['summary']['retrograde_planets'])}")
        
        print("\n=== ASPECTOS PRINCIPALES ===")
        for aspect in chart['aspects'][:5]:  # Mostrar solo los primeros 5
            print(f"{aspect['planet1']} {aspect['aspect']} {aspect['planet2']} (orbe: {aspect['orb']}°)")
        
        print("\n✓ Cálculo exitoso!")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


if __name__ == "__main__":
    test_calculation()
