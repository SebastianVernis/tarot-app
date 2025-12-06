"""
Servicio de integración con Google Gemini AI
Para interpretaciones astrológicas personalizadas
"""
import google.generativeai as genai
from typing import Dict, List, Optional
import os
from config import Config


class GeminiAstrologyService:
    """Servicio para generar interpretaciones astrológicas usando Gemini AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el servicio de Gemini
        
        Args:
            api_key: Clave API de Google Gemini (opcional, usa variable de entorno si no se proporciona)
        """
        self.api_key = api_key or os.environ.get('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY no configurada. "
                "Proporciona la clave en el constructor o como variable de entorno."
            )
        
        # Configurar Gemini
        genai.configure(api_key=self.api_key)
        
        # Usar el modelo Gemini Pro
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Configuración de generación
        self.generation_config = {
            'temperature': 0.7,  # Balance entre creatividad y coherencia
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
        
        # Configuración de seguridad (permitir contenido astrológico)
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
    
    def interpret_house_placement(
        self,
        planet_name: str,
        house_number: int,
        sign: str,
        degree: float
    ) -> str:
        """
        Genera interpretación de un planeta en una casa específica
        
        Args:
            planet_name: Nombre del planeta
            house_number: Número de casa (1-12)
            sign: Signo zodiacal
            degree: Grado dentro del signo
        
        Returns:
            Interpretación textual
        """
        prompt = f"""Como astrólogo experto, proporciona una interpretación detallada y personalizada de:

Planeta: {planet_name}
Casa: Casa {house_number}
Signo: {sign}
Grado: {degree:.2f}°

Incluye en tu interpretación:
1. El significado general de {planet_name} en la Casa {house_number}
2. Cómo el signo {sign} modifica esta energía
3. Áreas de vida afectadas
4. Fortalezas y desafíos potenciales
5. Consejo práctico para aprovechar esta posición

Escribe en español, de forma clara, empática y profesional. Máximo 200 palabras."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            return f"Error al generar interpretación: {str(e)}"
    
    def interpret_aspect(
        self,
        planet1_name: str,
        planet2_name: str,
        aspect_name: str,
        aspect_angle: float,
        orb: float,
        nature: str
    ) -> str:
        """
        Genera interpretación de un aspecto entre dos planetas
        
        Args:
            planet1_name: Nombre del primer planeta
            planet2_name: Nombre del segundo planeta
            aspect_name: Nombre del aspecto
            aspect_angle: Ángulo del aspecto
            orb: Orbe (diferencia con el aspecto exacto)
            nature: Naturaleza del aspecto (harmonious/challenging/neutral)
        
        Returns:
            Interpretación textual
        """
        nature_es = {
            'harmonious': 'armónico',
            'challenging': 'desafiante',
            'neutral': 'neutral',
            'minor': 'menor'
        }
        
        prompt = f"""Como astrólogo experto, interpreta este aspecto astrológico:

Aspecto: {planet1_name} {aspect_name} {planet2_name}
Ángulo: {aspect_angle}°
Orbe: {orb:.2f}° (precisión del aspecto)
Naturaleza: {nature_es.get(nature, nature)}

Proporciona una interpretación que incluya:
1. El significado de la interacción entre {planet1_name} y {planet2_name}
2. Cómo este aspecto {aspect_name} afecta la personalidad y vida de la persona
3. Oportunidades y desafíos que presenta
4. Consejo para trabajar constructivamente con esta energía
5. Si el orbe es pequeño (< 2°), menciona que es un aspecto muy fuerte

Escribe en español, de forma clara y constructiva. Máximo 180 palabras."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            return f"Error al generar interpretación: {str(e)}"
    
    def interpret_ascendant(self, sign: str, degree: float) -> str:
        """
        Interpreta el Ascendente
        
        Args:
            sign: Signo del Ascendente
            degree: Grado dentro del signo
        
        Returns:
            Interpretación del Ascendente
        """
        prompt = f"""Como astrólogo experto, interpreta el Ascendente:

Ascendente en {sign} a {degree:.2f}°

El Ascendente representa la máscara social, la primera impresión y el enfoque de vida.

Proporciona una interpretación que incluya:
1. Cómo se presenta esta persona al mundo
2. Su apariencia física y energía general
3. Su enfoque natural ante nuevas situaciones
4. Fortalezas de este Ascendente
5. Áreas de desarrollo personal

Escribe en español, de forma inspiradora y práctica. Máximo 200 palabras."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            return f"Error al generar interpretación: {str(e)}"
    
    def interpret_midheaven(self, sign: str, degree: float) -> str:
        """
        Interpreta el Medio Cielo (MC)
        
        Args:
            sign: Signo del MC
            degree: Grado dentro del signo
        
        Returns:
            Interpretación del MC
        """
        prompt = f"""Como astrólogo experto, interpreta el Medio Cielo (MC):

Medio Cielo en {sign} a {degree:.2f}°

El MC representa la vocación, carrera, reputación pública y aspiraciones.

Proporciona una interpretación que incluya:
1. Vocación y carrera ideal
2. Cómo alcanza el éxito profesional
3. Su reputación pública y legado
4. Metas y aspiraciones naturales
5. Consejo para el desarrollo profesional

Escribe en español, de forma motivadora y práctica. Máximo 200 palabras."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            return f"Error al generar interpretación: {str(e)}"
    
    def generate_birth_chart_summary(
        self,
        chart_data: Dict,
        focus_areas: Optional[List[str]] = None
    ) -> str:
        """
        Genera un resumen completo de la carta natal
        
        Args:
            chart_data: Datos completos de la carta natal
            focus_areas: Áreas específicas de enfoque (amor, carrera, etc.)
        
        Returns:
            Resumen interpretativo completo
        """
        summary = chart_data.get('chart_summary', {})
        
        # Construir información clave
        sun_sign = summary.get('sun_sign', 'Desconocido')
        moon_sign = summary.get('moon_sign', 'Desconocido')
        ascendant = summary.get('ascendant', {})
        asc_sign = ascendant.get('sign', 'Desconocido')
        dominant_element = summary.get('dominant_element', 'Desconocido')
        retrograde_planets = summary.get('retrograde_planets', [])
        
        focus_text = ""
        if focus_areas:
            focus_text = f"\nEnfócate especialmente en: {', '.join(focus_areas)}"
        
        prompt = f"""Como astrólogo experto, proporciona un análisis completo de esta carta natal:

DATOS PRINCIPALES:
- Sol en {sun_sign}
- Luna en {moon_sign}
- Ascendente en {asc_sign}
- Elemento dominante: {dominant_element}
- Planetas retrógrados: {', '.join(retrograde_planets) if retrograde_planets else 'Ninguno'}
{focus_text}

Proporciona un análisis que incluya:
1. Personalidad central (Sol, Luna, Ascendente)
2. Fortalezas y talentos naturales
3. Desafíos y áreas de crecimiento
4. Propósito de vida y vocación
5. Relaciones y vida emocional
6. Consejo general para el desarrollo personal

Escribe en español, de forma empática, inspiradora y práctica. Máximo 400 palabras."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            return f"Error al generar resumen: {str(e)}"
    
    def interpret_house_system(self, house_system: str) -> str:
        """
        Explica el sistema de casas utilizado
        
        Args:
            house_system: Código del sistema de casas
        
        Returns:
            Explicación del sistema
        """
        systems = {
            'P': 'Placidus',
            'K': 'Koch',
            'E': 'Casas Iguales (Equal House)',
            'W': 'Signos Completos (Whole Sign)',
            'C': 'Campanus',
            'R': 'Regiomontanus'
        }
        
        system_name = systems.get(house_system, 'Desconocido')
        
        prompt = f"""Como astrólogo experto, explica brevemente el sistema de casas {system_name}:

1. ¿Qué es y cómo funciona?
2. ¿Cuáles son sus ventajas?
3. ¿Por qué es popular entre astrólogos?

Escribe en español, de forma clara y educativa. Máximo 150 palabras."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            return f"Sistema de casas: {system_name}"
    
    def interpret_multiple_aspects(self, aspects: List[Dict], limit: int = 5) -> str:
        """
        Interpreta los aspectos más importantes de la carta
        
        Args:
            aspects: Lista de aspectos
            limit: Número máximo de aspectos a interpretar
        
        Returns:
            Interpretación de los aspectos principales
        """
        if not aspects:
            return "No se encontraron aspectos significativos en esta carta."
        
        # Tomar los aspectos más exactos (menor orbe)
        top_aspects = aspects[:limit]
        
        aspects_text = "\n".join([
            f"- {a['planet1']['name']} {a['aspect']} {a['planet2']['name']} "
            f"(orbe: {a['orb']:.2f}°, naturaleza: {a['nature']})"
            for a in top_aspects
        ])
        
        prompt = f"""Como astrólogo experto, interpreta estos aspectos principales de la carta natal:

{aspects_text}

Proporciona:
1. Una visión general de cómo estos aspectos trabajan juntos
2. Los temas principales que emergen
3. El balance entre aspectos armónicos y desafiantes
4. Consejo para integrar estas energías

Escribe en español, de forma sintética y práctica. Máximo 300 palabras."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            return f"Error al generar interpretación de aspectos: {str(e)}"
    
    def generate_personalized_reading(
        self,
        chart_data: Dict,
        question: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Genera una lectura astrológica completa y personalizada
        
        Args:
            chart_data: Datos completos de la carta natal
            question: Pregunta específica del usuario (opcional)
        
        Returns:
            Diccionario con diferentes secciones interpretadas
        """
        interpretations = {}
        
        # Interpretar Ascendente
        asc = chart_data['houses']['ascendant']
        interpretations['ascendant'] = self.interpret_ascendant(
            asc['sign'],
            asc['degree_in_sign']
        )
        
        # Interpretar Medio Cielo
        mc = chart_data['houses']['midheaven']
        interpretations['midheaven'] = self.interpret_midheaven(
            mc['sign'],
            mc['degree_in_sign']
        )
        
        # Interpretar aspectos principales
        aspects = chart_data.get('aspects', [])
        if aspects:
            interpretations['main_aspects'] = self.interpret_multiple_aspects(aspects, limit=5)
        
        # Resumen general
        interpretations['summary'] = self.generate_birth_chart_summary(
            chart_data,
            focus_areas=['personalidad', 'vocación', 'relaciones'] if not question else None
        )
        
        # Si hay una pregunta específica, generar respuesta
        if question:
            interpretations['question_answer'] = self._answer_specific_question(
                chart_data,
                question
            )
        
        return interpretations
    
    def _answer_specific_question(self, chart_data: Dict, question: str) -> str:
        """
        Responde una pregunta específica basada en la carta natal
        
        Args:
            chart_data: Datos de la carta natal
            question: Pregunta del usuario
        
        Returns:
            Respuesta personalizada
        """
        summary = chart_data.get('chart_summary', {})
        
        prompt = f"""Como astrólogo experto, responde esta pregunta basándote en la carta natal:

PREGUNTA: {question}

DATOS DE LA CARTA:
- Sol en {summary.get('sun_sign', 'Desconocido')}
- Luna en {summary.get('moon_sign', 'Desconocido')}
- Ascendente en {summary.get('ascendant', {}).get('sign', 'Desconocido')}
- Elemento dominante: {summary.get('dominant_element', 'Desconocido')}

Proporciona una respuesta:
1. Directa y relevante a la pregunta
2. Basada en las posiciones astrológicas
3. Con consejo práctico y accionable
4. Empática y constructiva

Escribe en español. Máximo 250 palabras."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            return f"Error al responder pregunta: {str(e)}"


# Función de utilidad para uso rápido
def get_gemini_service() -> GeminiAstrologyService:
    """
    Obtiene una instancia del servicio Gemini
    
    Returns:
        Instancia de GeminiAstrologyService
    """
    return GeminiAstrologyService()
