"""
Servicio de integración con Google Gemini API
Para generar interpretaciones astrológicas personalizadas
"""
import google.generativeai as genai
from typing import Dict, Optional
import os
import time
from functools import wraps


class GeminiService:
    """Servicio para interactuar con Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el servicio Gemini
        
        Args:
            api_key: Clave API de Gemini (opcional, se puede obtener de variable de entorno)
        """
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Se requiere GEMINI_API_KEY. "
                "Proporciona la clave en el constructor o como variable de entorno."
            )
        
        # Configurar Gemini
        genai.configure(api_key=self.api_key)
        
        # Configuración del modelo
        self.generation_config = {
            'temperature': 0.9,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
        
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        
        # Inicializar modelo
        self.model = genai.GenerativeModel(
            model_name='gemini-pro',
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
    
    def retry_on_error(max_retries=3, delay=1):
        """Decorador para reintentar en caso de error"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_retries - 1:
                            raise
                        time.sleep(delay * (attempt + 1))
                return None
            return wrapper
        return decorator
    
    @retry_on_error(max_retries=3, delay=2)
    def generate_birth_chart_interpretation(self, chart_data: Dict) -> str:
        """
        Genera una interpretación completa de la carta natal
        
        Args:
            chart_data: Datos de la carta natal del AstrologyCalculator
        
        Returns:
            Interpretación textual personalizada
        """
        # Extraer información clave
        planets = chart_data.get('planets', {})
        summary = chart_data.get('summary', {})
        aspects = chart_data.get('aspects', [])
        houses = chart_data.get('houses', {})
        
        # Construir prompt detallado
        prompt = self._build_birth_chart_prompt(planets, summary, aspects, houses)
        
        # Generar interpretación
        response = self.model.generate_content(prompt)
        
        return response.text
    
    def _build_birth_chart_prompt(
        self,
        planets: Dict,
        summary: Dict,
        aspects: list,
        houses: Dict
    ) -> str:
        """Construye el prompt para la interpretación de carta natal"""
        
        # Información de planetas
        planet_info = []
        for planet_key, planet_data in planets.items():
            retro = " (retrógrado)" if planet_data.get('retrograde') else ""
            planet_info.append(
                f"- {planet_data['name']} en {planet_data['sign']} "
                f"a {planet_data['degrees']}°{retro}"
            )
        
        # Aspectos principales (top 10)
        aspect_info = []
        for aspect in aspects[:10]:
            aspect_info.append(
                f"- {aspect['planet1']} {aspect['aspect']} {aspect['planet2']} "
                f"(orbe: {aspect['orb']}°)"
            )
        
        # Construir prompt
        prompt = f"""Eres un astrólogo profesional experto. Genera una interpretación astrológica 
completa, profunda y personalizada basada en la siguiente carta natal.

DATOS DE LA CARTA NATAL:

Signo Solar: {summary.get('sun_sign')}
Signo Lunar: {summary.get('moon_sign')}
Signo Ascendente: {summary.get('rising_sign')}

Elemento Dominante: {summary.get('dominant_element')}
Modalidad Dominante: {summary.get('dominant_modality')}

POSICIONES PLANETARIAS:
{chr(10).join(planet_info)}

ASPECTOS PRINCIPALES:
{chr(10).join(aspect_info) if aspect_info else "No hay aspectos significativos"}

PLANETAS RETRÓGRADOS:
{', '.join(summary.get('retrograde_planets', [])) if summary.get('retrograde_planets') else 'Ninguno'}

INSTRUCCIONES:
1. Proporciona una interpretación detallada y personalizada
2. Explica el significado del Sol, Luna y Ascendente
3. Analiza el elemento y modalidad dominante
4. Interpreta los aspectos más importantes
5. Menciona los planetas retrógrados y su significado
6. Incluye consejos prácticos y áreas de desarrollo personal
7. Usa un tono profesional pero accesible
8. Estructura la respuesta en secciones claras
9. Escribe en español

La interpretación debe ser comprensiva (mínimo 800 palabras) y cubrir:
- Personalidad básica (Sol, Luna, Ascendente)
- Fortalezas y talentos naturales
- Desafíos y áreas de crecimiento
- Relaciones y comunicación
- Carrera y propósito de vida
- Espiritualidad y desarrollo interior
"""
        
        return prompt
    
    @retry_on_error(max_retries=3, delay=2)
    def generate_planetary_interpretation(self, positions: Dict) -> str:
        """
        Genera interpretación de posiciones planetarias (versión simplificada)
        
        Args:
            positions: Diccionario con posiciones planetarias
        
        Returns:
            Interpretación textual
        """
        planet_list = []
        for planet_key, planet_data in positions.items():
            retro = " (R)" if planet_data.get('retrograde') else ""
            planet_list.append(
                f"- {planet_data['name']}: {planet_data['sign']} {planet_data['position']}{retro}"
            )
        
        prompt = f"""Eres un astrólogo experto. Proporciona una interpretación breve pero significativa 
de las siguientes posiciones planetarias:

{chr(10).join(planet_list)}

Instrucciones:
1. Explica el significado general de estas posiciones
2. Destaca los aspectos más importantes
3. Proporciona insights prácticos
4. Usa un tono profesional y accesible
5. Escribe en español
6. Mantén la respuesta concisa (300-500 palabras)
"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    @retry_on_error(max_retries=3, delay=2)
    def generate_daily_horoscope(self, sun_sign: str, date: str) -> str:
        """
        Genera horóscopo diario para un signo
        
        Args:
            sun_sign: Signo solar
            date: Fecha en formato ISO
        
        Returns:
            Horóscopo diario
        """
        prompt = f"""Eres un astrólogo profesional. Genera un horóscopo diario para {sun_sign} 
para la fecha {date}.

El horóscopo debe incluir:
1. Energía general del día
2. Amor y relaciones
3. Trabajo y finanzas
4. Salud y bienestar
5. Consejo del día
6. Números de la suerte
7. Color del día

Usa un tono positivo, inspirador y práctico.
Escribe en español.
Longitud: 200-300 palabras.
"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    @retry_on_error(max_retries=3, delay=2)
    def generate_compatibility_reading(
        self,
        person1_data: Dict,
        person2_data: Dict
    ) -> str:
        """
        Genera lectura de compatibilidad entre dos personas
        
        Args:
            person1_data: Datos astrológicos de la persona 1
            person2_data: Datos astrológicos de la persona 2
        
        Returns:
            Análisis de compatibilidad
        """
        prompt = f"""Eres un astrólogo experto en sinastría (compatibilidad astrológica).
Analiza la compatibilidad entre estas dos personas:

PERSONA 1:
- Sol: {person1_data.get('sun_sign')}
- Luna: {person1_data.get('moon_sign')}
- Ascendente: {person1_data.get('rising_sign')}

PERSONA 2:
- Sol: {person2_data.get('sun_sign')}
- Luna: {person2_data.get('moon_sign')}
- Ascendente: {person2_data.get('rising_sign')}

Proporciona un análisis detallado que incluya:
1. Compatibilidad general (porcentaje y explicación)
2. Compatibilidad emocional (Lunas)
3. Compatibilidad de personalidad (Soles)
4. Atracción inicial (Ascendentes)
5. Fortalezas de la relación
6. Desafíos potenciales
7. Consejos para una relación armoniosa

Usa un tono profesional, equilibrado y constructivo.
Escribe en español.
Longitud: 500-700 palabras.
"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    @retry_on_error(max_retries=3, delay=2)
    def generate_transit_interpretation(
        self,
        natal_chart: Dict,
        transit_positions: Dict
    ) -> str:
        """
        Genera interpretación de tránsitos planetarios
        
        Args:
            natal_chart: Carta natal de la persona
            transit_positions: Posiciones planetarias actuales
        
        Returns:
            Interpretación de tránsitos
        """
        prompt = f"""Eres un astrólogo experto en tránsitos planetarios.
Analiza los tránsitos actuales para una persona con:

CARTA NATAL:
- Sol: {natal_chart['summary']['sun_sign']}
- Luna: {natal_chart['summary']['moon_sign']}
- Ascendente: {natal_chart['summary']['rising_sign']}

TRÁNSITOS ACTUALES:
{self._format_positions_for_prompt(transit_positions)}

Proporciona:
1. Tránsitos más importantes del momento
2. Áreas de vida afectadas
3. Oportunidades y desafíos
4. Consejos prácticos
5. Timing de eventos importantes

Usa un tono profesional y práctico.
Escribe en español.
Longitud: 400-600 palabras.
"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _format_positions_for_prompt(self, positions: Dict) -> str:
        """Formatea posiciones planetarias para el prompt"""
        lines = []
        for planet_key, planet_data in positions.items():
            lines.append(f"- {planet_data['name']}: {planet_data['sign']} {planet_data['position']}")
        return '\n'.join(lines)
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión con Gemini API
        
        Returns:
            True si la conexión es exitosa
        """
        try:
            response = self.model.generate_content("Di 'Conexión exitosa' en español.")
            return 'exitosa' in response.text.lower() or 'éxito' in response.text.lower()
        except Exception as e:
            print(f"Error probando conexión: {str(e)}")
            return False


# Función de prueba
def test_gemini_service():
    """Prueba el servicio Gemini"""
    try:
        # Intentar obtener API key
        api_key = os.environ.get('GEMINI_API_KEY')
        
        if not api_key:
            print("⚠️  GEMINI_API_KEY no configurada")
            print("Para probar el servicio, configura la variable de entorno:")
            print("export GEMINI_API_KEY='tu-clave-api'")
            return
        
        print("Inicializando servicio Gemini...")
        service = GeminiService(api_key)
        
        print("Probando conexión...")
        if service.test_connection():
            print("✓ Conexión exitosa con Gemini API")
        else:
            print("✗ Error en la conexión")
            return
        
        # Datos de prueba
        test_chart = {
            'planets': {
                'sun': {'name': 'Sol', 'sign': 'Capricornio', 'degrees': 10, 'retrograde': False},
                'moon': {'name': 'Luna', 'sign': 'Libra', 'degrees': 15, 'retrograde': False},
            },
            'summary': {
                'sun_sign': 'Capricornio',
                'moon_sign': 'Libra',
                'rising_sign': 'Aries',
                'dominant_element': 'Tierra',
                'dominant_modality': 'Cardinal',
                'retrograde_planets': []
            },
            'aspects': [
                {
                    'planet1': 'Sol',
                    'planet2': 'Luna',
                    'aspect': 'Cuadratura',
                    'orb': 5.0
                }
            ],
            'houses': {}
        }
        
        print("\nGenerando interpretación de prueba...")
        interpretation = service.generate_birth_chart_interpretation(test_chart)
        
        print("\n" + "="*60)
        print("INTERPRETACIÓN GENERADA:")
        print("="*60)
        print(interpretation[:500] + "..." if len(interpretation) > 500 else interpretation)
        print("\n✓ Servicio funcionando correctamente")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


if __name__ == "__main__":
    test_gemini_service()
