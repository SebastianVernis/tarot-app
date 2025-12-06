"""
Módulo de cálculos astrológicos avanzados
Implementa sistemas de casas y detección de aspectos planetarios
"""
import swisseph as swe
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pytz
import math


class HouseSystem:
    """Sistemas de casas astrológicas"""
    PLACIDUS = 'P'  # Sistema Placidus (más popular)
    KOCH = 'K'      # Sistema Koch
    EQUAL = 'E'     # Casas Iguales (Equal House)
    WHOLE_SIGN = 'W'  # Signos Completos
    CAMPANUS = 'C'  # Campanus
    REGIOMONTANUS = 'R'  # Regiomontanus


class Planet:
    """Constantes para planetas y puntos astrológicos"""
    SUN = 0
    MOON = 1
    MERCURY = 2
    VENUS = 3
    MARS = 4
    JUPITER = 5
    SATURN = 6
    URANUS = 7
    NEPTUNE = 8
    PLUTO = 9
    NORTH_NODE = 10  # Nodo Norte (Rahu)
    SOUTH_NODE = 11  # Nodo Sur (Ketu)
    
    NAMES = {
        0: "Sol", 1: "Luna", 2: "Mercurio", 3: "Venus",
        4: "Marte", 5: "Júpiter", 6: "Saturno", 7: "Urano",
        8: "Neptuno", 9: "Plutón", 10: "Nodo Norte", 11: "Nodo Sur"
    }
    
    SYMBOLS = {
        0: "☉", 1: "☽", 2: "☿", 3: "♀",
        4: "♂", 5: "♃", 6: "♄", 7: "♅",
        8: "♆", 9: "♇", 10: "☊", 11: "☋"
    }


class Aspect:
    """Tipos de aspectos astrológicos"""
    # Aspectos mayores
    CONJUNCTION = {"name": "Conjunción", "angle": 0, "orb": 8, "symbol": "☌", "nature": "neutral"}
    SEXTILE = {"name": "Sextil", "angle": 60, "orb": 6, "symbol": "⚹", "nature": "harmonious"}
    SQUARE = {"name": "Cuadratura", "angle": 90, "orb": 8, "symbol": "□", "nature": "challenging"}
    TRINE = {"name": "Trígono", "angle": 120, "orb": 8, "symbol": "△", "nature": "harmonious"}
    OPPOSITION = {"name": "Oposición", "angle": 180, "orb": 8, "symbol": "☍", "nature": "challenging"}
    
    # Aspectos menores
    SEMI_SEXTILE = {"name": "Semi-sextil", "angle": 30, "orb": 2, "symbol": "⚺", "nature": "minor"}
    SEMI_SQUARE = {"name": "Semi-cuadratura", "angle": 45, "orb": 2, "symbol": "∠", "nature": "minor"}
    SESQUIQUADRATE = {"name": "Sesquicuadratura", "angle": 135, "orb": 2, "symbol": "⚼", "nature": "minor"}
    QUINCUNX = {"name": "Quincuncio", "angle": 150, "orb": 2, "symbol": "⚻", "nature": "minor"}
    
    ALL_ASPECTS = [
        CONJUNCTION, SEXTILE, SQUARE, TRINE, OPPOSITION,
        SEMI_SEXTILE, SEMI_SQUARE, SESQUIQUADRATE, QUINCUNX
    ]
    
    MAJOR_ASPECTS = [CONJUNCTION, SEXTILE, SQUARE, TRINE, OPPOSITION]
    MINOR_ASPECTS = [SEMI_SEXTILE, SEMI_SQUARE, SESQUIQUADRATE, QUINCUNX]


class ZodiacSign:
    """Signos zodiacales"""
    SIGNS = [
        {"name": "Aries", "symbol": "♈", "element": "Fuego", "quality": "Cardinal"},
        {"name": "Tauro", "symbol": "♉", "element": "Tierra", "quality": "Fijo"},
        {"name": "Géminis", "symbol": "♊", "element": "Aire", "quality": "Mutable"},
        {"name": "Cáncer", "symbol": "♋", "element": "Agua", "quality": "Cardinal"},
        {"name": "Leo", "symbol": "♌", "element": "Fuego", "quality": "Fijo"},
        {"name": "Virgo", "symbol": "♍", "element": "Tierra", "quality": "Mutable"},
        {"name": "Libra", "symbol": "♎", "element": "Aire", "quality": "Cardinal"},
        {"name": "Escorpio", "symbol": "♏", "element": "Agua", "quality": "Fijo"},
        {"name": "Sagitario", "symbol": "♐", "element": "Fuego", "quality": "Mutable"},
        {"name": "Capricornio", "symbol": "♑", "element": "Tierra", "quality": "Cardinal"},
        {"name": "Acuario", "symbol": "♒", "element": "Aire", "quality": "Fijo"},
        {"name": "Piscis", "symbol": "♓", "element": "Agua", "quality": "Mutable"}
    ]
    
    @staticmethod
    def get_sign(longitude: float) -> Dict:
        """Obtiene el signo zodiacal para una longitud dada"""
        sign_index = int(longitude / 30)
        degree_in_sign = longitude % 30
        sign_info = ZodiacSign.SIGNS[sign_index].copy()
        sign_info['degree'] = degree_in_sign
        return sign_info


class AstrologyCalculator:
    """Calculadora principal de astrología"""
    
    def __init__(self):
        """Inicializa el calculador astrológico"""
        # Configurar la ruta de los archivos efemerides de Swiss Ephemeris
        # Por defecto usa los archivos incluidos en pyswisseph
        swe.set_ephe_path(None)
    
    def calculate_julian_day(self, dt: datetime, timezone_str: str = 'UTC') -> float:
        """
        Calcula el día juliano para una fecha/hora dada
        
        Args:
            dt: Fecha y hora
            timezone_str: Zona horaria (ej: 'America/Mexico_City', 'Europe/Madrid')
        
        Returns:
            Día juliano
        """
        # Convertir a UTC si tiene zona horaria
        if dt.tzinfo is None:
            tz = pytz.timezone(timezone_str)
            dt = tz.localize(dt)
        
        dt_utc = dt.astimezone(pytz.UTC)
        
        # Calcular día juliano
        jd = swe.julday(
            dt_utc.year,
            dt_utc.month,
            dt_utc.day,
            dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
        )
        
        return jd
    
    def calculate_planetary_positions(self, jd: float) -> Dict[int, Dict]:
        """
        Calcula las posiciones de todos los planetas
        
        Args:
            jd: Día juliano
        
        Returns:
            Diccionario con posiciones planetarias
        """
        positions = {}
        
        # Planetas principales
        planets = [
            Planet.SUN, Planet.MOON, Planet.MERCURY, Planet.VENUS,
            Planet.MARS, Planet.JUPITER, Planet.SATURN, Planet.URANUS,
            Planet.NEPTUNE, Planet.PLUTO
        ]
        
        for planet_id in planets:
            # Calcular posición
            result, ret_flag = swe.calc_ut(jd, planet_id)
            
            longitude = result[0]  # Longitud eclíptica
            latitude = result[1]   # Latitud eclíptica
            distance = result[2]   # Distancia
            speed = result[3]      # Velocidad
            
            # Determinar si está retrógrado
            is_retrograde = speed < 0
            
            # Obtener signo zodiacal
            sign_info = ZodiacSign.get_sign(longitude)
            
            positions[planet_id] = {
                'name': Planet.NAMES[planet_id],
                'symbol': Planet.SYMBOLS[planet_id],
                'longitude': longitude,
                'latitude': latitude,
                'distance': distance,
                'speed': speed,
                'retrograde': is_retrograde,
                'sign': sign_info['name'],
                'sign_symbol': sign_info['symbol'],
                'degree_in_sign': sign_info['degree'],
                'element': sign_info['element'],
                'quality': sign_info['quality']
            }
        
        # Calcular Nodo Norte
        result, ret_flag = swe.calc_ut(jd, swe.TRUE_NODE)
        longitude = result[0]
        sign_info = ZodiacSign.get_sign(longitude)
        
        positions[Planet.NORTH_NODE] = {
            'name': Planet.NAMES[Planet.NORTH_NODE],
            'symbol': Planet.SYMBOLS[Planet.NORTH_NODE],
            'longitude': longitude,
            'sign': sign_info['name'],
            'sign_symbol': sign_info['symbol'],
            'degree_in_sign': sign_info['degree']
        }
        
        return positions
    
    def calculate_houses(
        self,
        jd: float,
        latitude: float,
        longitude: float,
        house_system: str = HouseSystem.PLACIDUS
    ) -> Dict:
        """
        Calcula las casas astrológicas
        
        Args:
            jd: Día juliano
            latitude: Latitud del lugar de nacimiento
            longitude: Longitud del lugar de nacimiento
            house_system: Sistema de casas a usar
        
        Returns:
            Diccionario con información de las casas
        """
        # Calcular casas
        cusps, ascmc = swe.houses(jd, latitude, longitude, house_system.encode())
        
        # cusps es una tupla con 13 elementos (índices 0-12, donde 0 no se usa en algunos sistemas)
        # ascmc contiene: [Ascendente, MC, ARMC, Vertex, Equatorial Ascendant, ...]
        
        houses = {}
        # Swiss Ephemeris devuelve cusps con índice 0 no usado, casas 1-12 en índices 1-12
        # Pero algunas versiones pueden devolver solo 12 elementos (0-11)
        for i in range(1, 13):
            # Ajustar índice según la longitud de cusps
            cusp_index = i if len(cusps) > 12 else i - 1
            cusp_longitude = cusps[cusp_index]
            sign_info = ZodiacSign.get_sign(cusp_longitude)
            
            houses[i] = {
                'number': i,
                'cusp_longitude': cusp_longitude,
                'sign': sign_info['name'],
                'sign_symbol': sign_info['symbol'],
                'degree_in_sign': sign_info['degree'],
                'element': sign_info['element']
            }
        
        # Puntos importantes
        ascendant = ascmc[0]
        mc = ascmc[1]  # Medium Coeli (Medio Cielo)
        
        asc_sign = ZodiacSign.get_sign(ascendant)
        mc_sign = ZodiacSign.get_sign(mc)
        
        return {
            'houses': houses,
            'ascendant': {
                'longitude': ascendant,
                'sign': asc_sign['name'],
                'sign_symbol': asc_sign['symbol'],
                'degree_in_sign': asc_sign['degree']
            },
            'midheaven': {
                'longitude': mc,
                'sign': mc_sign['name'],
                'sign_symbol': mc_sign['symbol'],
                'degree_in_sign': mc_sign['degree']
            },
            'house_system': house_system
        }
    
    def assign_planets_to_houses(
        self,
        planetary_positions: Dict[int, Dict],
        houses: Dict
    ) -> Dict[int, List[Dict]]:
        """
        Asigna planetas a sus casas correspondientes
        
        Args:
            planetary_positions: Posiciones planetarias
            houses: Información de las casas
        
        Returns:
            Diccionario con planetas por casa
        """
        planets_in_houses = {i: [] for i in range(1, 13)}
        
        house_cusps = houses['houses']
        
        for planet_id, planet_data in planetary_positions.items():
            planet_longitude = planet_data['longitude']
            
            # Determinar en qué casa está el planeta
            house_number = self._find_house_for_planet(planet_longitude, house_cusps)
            
            planets_in_houses[house_number].append({
                'planet_id': planet_id,
                'name': planet_data['name'],
                'symbol': planet_data['symbol'],
                'longitude': planet_longitude,
                'sign': planet_data['sign'],
                'degree_in_sign': planet_data['degree_in_sign']
            })
        
        return planets_in_houses
    
    def _find_house_for_planet(self, planet_longitude: float, house_cusps: Dict) -> int:
        """
        Encuentra la casa en la que está un planeta
        
        Args:
            planet_longitude: Longitud del planeta
            house_cusps: Cúspides de las casas
        
        Returns:
            Número de casa (1-12)
        """
        # Normalizar longitud a 0-360
        planet_long = planet_longitude % 360
        
        for i in range(1, 13):
            cusp_start = house_cusps[i]['cusp_longitude']
            
            # Siguiente cúspide (casa 13 = casa 1)
            next_house = (i % 12) + 1
            cusp_end = house_cusps[next_house]['cusp_longitude']
            
            # Manejar el caso cuando cruza 0° Aries
            if cusp_start > cusp_end:
                if planet_long >= cusp_start or planet_long < cusp_end:
                    return i
            else:
                if cusp_start <= planet_long < cusp_end:
                    return i
        
        return 1  # Por defecto, casa 1
    
    def calculate_aspects(
        self,
        planetary_positions: Dict[int, Dict],
        include_minor: bool = True
    ) -> List[Dict]:
        """
        Calcula aspectos entre planetas
        
        Args:
            planetary_positions: Posiciones planetarias
            include_minor: Incluir aspectos menores
        
        Returns:
            Lista de aspectos detectados
        """
        aspects_list = []
        
        # Aspectos a considerar
        aspects_to_check = Aspect.ALL_ASPECTS if include_minor else Aspect.MAJOR_ASPECTS
        
        # Obtener lista de planetas
        planet_ids = list(planetary_positions.keys())
        
        # Comparar cada par de planetas
        for i in range(len(planet_ids)):
            for j in range(i + 1, len(planet_ids)):
                planet1_id = planet_ids[i]
                planet2_id = planet_ids[j]
                
                planet1 = planetary_positions[planet1_id]
                planet2 = planetary_positions[planet2_id]
                
                # Calcular diferencia angular
                angle_diff = abs(planet1['longitude'] - planet2['longitude'])
                
                # Normalizar a 0-180
                if angle_diff > 180:
                    angle_diff = 360 - angle_diff
                
                # Verificar cada tipo de aspecto
                for aspect_type in aspects_to_check:
                    target_angle = aspect_type['angle']
                    orb = aspect_type['orb']
                    
                    # Calcular diferencia con el ángulo del aspecto
                    diff = abs(angle_diff - target_angle)
                    
                    # Si está dentro del orbe, es un aspecto válido
                    if diff <= orb:
                        aspects_list.append({
                            'planet1': {
                                'id': planet1_id,
                                'name': planet1['name'],
                                'symbol': planet1['symbol'],
                                'longitude': planet1['longitude']
                            },
                            'planet2': {
                                'id': planet2_id,
                                'name': planet2['name'],
                                'symbol': planet2['symbol'],
                                'longitude': planet2['longitude']
                            },
                            'aspect': aspect_type['name'],
                            'aspect_symbol': aspect_type['symbol'],
                            'angle': target_angle,
                            'orb': diff,
                            'max_orb': orb,
                            'nature': aspect_type['nature'],
                            'exact_angle': angle_diff,
                            'applying': self._is_applying(planet1, planet2, angle_diff, target_angle)
                        })
        
        # Ordenar por orbe (aspectos más exactos primero)
        aspects_list.sort(key=lambda x: x['orb'])
        
        return aspects_list
    
    def _is_applying(
        self,
        planet1: Dict,
        planet2: Dict,
        current_angle: float,
        target_angle: float
    ) -> bool:
        """
        Determina si un aspecto está aplicando (acercándose) o separando
        
        Args:
            planet1: Datos del primer planeta
            planet2: Datos del segundo planeta
            current_angle: Ángulo actual entre planetas
            target_angle: Ángulo del aspecto
        
        Returns:
            True si está aplicando, False si está separando
        """
        # Si alguno no tiene velocidad, no podemos determinar
        if 'speed' not in planet1 or 'speed' not in planet2:
            return False
        
        # Velocidad relativa
        relative_speed = planet1['speed'] - planet2['speed']
        
        # Si la velocidad relativa reduce la diferencia con el ángulo objetivo, está aplicando
        return relative_speed < 0 if current_angle < target_angle else relative_speed > 0
    
    def calculate_birth_chart(
        self,
        birth_datetime: datetime,
        latitude: float,
        longitude: float,
        timezone_str: str = 'UTC',
        house_system: str = HouseSystem.PLACIDUS,
        include_minor_aspects: bool = True
    ) -> Dict:
        """
        Calcula una carta natal completa
        
        Args:
            birth_datetime: Fecha y hora de nacimiento
            latitude: Latitud del lugar de nacimiento
            longitude: Longitud del lugar de nacimiento
            timezone_str: Zona horaria
            house_system: Sistema de casas
            include_minor_aspects: Incluir aspectos menores
        
        Returns:
            Carta natal completa con planetas, casas y aspectos
        """
        # Calcular día juliano
        jd = self.calculate_julian_day(birth_datetime, timezone_str)
        
        # Calcular posiciones planetarias
        planetary_positions = self.calculate_planetary_positions(jd)
        
        # Calcular casas
        houses = self.calculate_houses(jd, latitude, longitude, house_system)
        
        # Asignar planetas a casas
        planets_in_houses = self.assign_planets_to_houses(planetary_positions, houses)
        
        # Calcular aspectos
        aspects = self.calculate_aspects(planetary_positions, include_minor_aspects)
        
        return {
            'birth_data': {
                'datetime': birth_datetime.isoformat(),
                'timezone': timezone_str,
                'latitude': latitude,
                'longitude': longitude,
                'julian_day': jd
            },
            'planetary_positions': planetary_positions,
            'houses': houses,
            'planets_in_houses': planets_in_houses,
            'aspects': aspects,
            'chart_summary': self._generate_chart_summary(
                planetary_positions,
                houses,
                planets_in_houses,
                aspects
            )
        }
    
    def _generate_chart_summary(
        self,
        planetary_positions: Dict,
        houses: Dict,
        planets_in_houses: Dict,
        aspects: List[Dict]
    ) -> Dict:
        """
        Genera un resumen de la carta natal
        
        Returns:
            Resumen con estadísticas y puntos clave
        """
        # Contar elementos
        elements = {'Fuego': 0, 'Tierra': 0, 'Aire': 0, 'Agua': 0}
        for planet_data in planetary_positions.values():
            if 'element' in planet_data:
                elements[planet_data['element']] += 1
        
        # Elemento dominante
        dominant_element = max(elements, key=elements.get)
        
        # Contar aspectos por naturaleza
        aspect_counts = {'harmonious': 0, 'challenging': 0, 'neutral': 0, 'minor': 0}
        for aspect in aspects:
            aspect_counts[aspect['nature']] += 1
        
        return {
            'ascendant': houses['ascendant'],
            'midheaven': houses['midheaven'],
            'sun_sign': planetary_positions[Planet.SUN]['sign'],
            'moon_sign': planetary_positions[Planet.MOON]['sign'],
            'elements': elements,
            'dominant_element': dominant_element,
            'aspect_counts': aspect_counts,
            'total_aspects': len(aspects),
            'retrograde_planets': [
                p['name'] for p in planetary_positions.values()
                if p.get('retrograde', False)
            ]
        }


# Funciones de utilidad para uso rápido
def calculate_houses_and_aspects(
    birth_datetime: datetime,
    latitude: float,
    longitude: float,
    timezone_str: str = 'UTC',
    house_system: str = HouseSystem.PLACIDUS
) -> Dict:
    """
    Función de conveniencia para calcular casas y aspectos
    
    Args:
        birth_datetime: Fecha y hora de nacimiento
        latitude: Latitud del lugar
        longitude: Longitud del lugar
        timezone_str: Zona horaria
        house_system: Sistema de casas
    
    Returns:
        Carta natal completa
    """
    calculator = AstrologyCalculator()
    return calculator.calculate_birth_chart(
        birth_datetime,
        latitude,
        longitude,
        timezone_str,
        house_system
    )


def find_aspects(planetary_positions: Dict, include_minor: bool = True) -> List[Dict]:
    """
    Función de conveniencia para encontrar aspectos
    
    Args:
        planetary_positions: Posiciones planetarias
        include_minor: Incluir aspectos menores
    
    Returns:
        Lista de aspectos
    """
    calculator = AstrologyCalculator()
    return calculator.calculate_aspects(planetary_positions, include_minor)
