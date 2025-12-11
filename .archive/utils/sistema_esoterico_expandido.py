#!/usr/bin/env python3
"""
Sistema Esotérico Expandido - Múltiples modalidades de adivinación y juegos de azar
Autor: Assistant
Descripción: Sistema completo de adivinación con múltiples disciplinas esotéricas
"""

import random
import json
import time
import hashlib
import os
from datetime import datetime, date
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import secrets
import math
from abc import ABC, abstractmethod

# Importar el sistema de tarot existente
try:
    from tarot_reader_enhanced import GeneradorAleatorio, Carta, MazoTarot, LectorTarot, TipoTirada
except ImportError:
    print("Sistema de tarot no disponible, funcionará solo con nuevas modalidades")


class TipoModalidad(Enum):
    """Tipos de modalidades esotéricas disponibles"""
    # Tarot existente
    TAROT = "tarot"
    
    # Nuevas modalidades
    NUMEROLOGIA = "numerologia"
    RUNAS = "runas"
    I_CHING = "i_ching"
    ORACULO_SI_NO = "oraculo_si_no"
    HOROSCOPO = "horoscopo"
    CARTAS_ANGEL = "cartas_angel"
    ASTROLOGIA_BASICA = "astrologia_basica"
    DADOS_COSMICOS = "dados_cosmicos"
    PENDULO_VIRTUAL = "pendulo_virtual"
    CRISTALES_ENERGIA = "cristales_energia"
    MEDICINA_ANCESTRAL = "medicina_ancestral"
    CHAKRAS_DETALLADO = "chakras_detallado"
    ELEMENTOS_NATURALES = "elementos_naturales"


@dataclass
class ResultadoEsoterico:
    """Resultado base para cualquier modalidad esotérica"""
    modalidad: str
    titulo: str
    resultado_principal: str
    interpretacion: str
    detalles_adicionales: Dict
    fecha: datetime
    id_unico: str


class ModalidadEsoterica(ABC):
    """Clase base abstracta para todas las modalidades esotéricas"""
    
    def __init__(self):
        self.generador = GeneradorAleatorio() if 'GeneradorAleatorio' in globals() else None
        self.nombre = ""
        self.descripcion = ""
    
    @abstractmethod
    def realizar_lectura(self, pregunta: str = "", parametros: Dict = None) -> ResultadoEsoterico:
        """Método abstracto que debe implementar cada modalidad"""
        pass
    
    def _generar_id_unico(self) -> str:
        """Genera un ID único para la lectura"""
        timestamp = str(time.time())
        random_data = str(secrets.randbits(64))
        return hashlib.md5((timestamp + random_data).encode()).hexdigest()[:12]


class Numerologia(ModalidadEsoterica):
    """Sistema de numerología con múltiples cálculos"""
    
    def __init__(self):
        super().__init__()
        self.nombre = "Numerología Completa"
        self.descripcion = "Análisis numerológico basado en tu fecha de nacimiento y nombre"
        
        self.significados_numeros = {
            1: {
                "titulo": "El Líder",
                "descripcion": "Independencia, liderazgo, innovación, iniciativa",
                "personalidad": "Eres un líder natural con gran iniciativa",
                "desafios": "Evita la terquedad y el egocentrismo",
                "color": "Rojo", "planeta": "Sol"
            },
            2: {
                "titulo": "El Cooperador",
                "descripcion": "Cooperación, diplomacia, sensibilidad, paz",
                "personalidad": "Tienes gran habilidad para trabajar en equipo",
                "desafios": "No te pierdas en complacer a otros",
                "color": "Naranja", "planeta": "Luna"
            },
            3: {
                "titulo": "El Comunicador",
                "descripcion": "Creatividad, comunicación, expresión, optimismo",
                "personalidad": "Posees gran talento creativo y expresivo",
                "desafios": "Enfócate y evita dispersarte demasiado",
                "color": "Amarillo", "planeta": "Júpiter"
            },
            4: {
                "titulo": "El Constructor",
                "descripcion": "Estabilidad, trabajo duro, organización, práctica",
                "personalidad": "Eres confiable y construyes bases sólidas",
                "desafios": "No seas demasiado rígido o pesimista",
                "color": "Verde", "planeta": "Urano"
            },
            5: {
                "titulo": "El Aventurero",
                "descripcion": "Libertad, aventura, versatilidad, experiencia",
                "personalidad": "Buscas libertad y nuevas experiencias",
                "desafios": "Aprende a comprometerte y ser constante",
                "color": "Azul", "planeta": "Mercurio"
            },
            6: {
                "titulo": "El Cuidador",
                "descripcion": "Responsabilidad, familia, sanación, servicio",
                "personalidad": "Tienes gran capacidad de cuidar a otros",
                "desafios": "No te sacrifiques excesivamente",
                "color": "Índigo", "planeta": "Venus"
            },
            7: {
                "titulo": "El Buscador",
                "descripcion": "Espiritualidad, introspección, análisis, sabiduría",
                "personalidad": "Buscas la verdad y el conocimiento profundo",
                "desafios": "No te aísles demasiado del mundo",
                "color": "Violeta", "planeta": "Neptuno"
            },
            8: {
                "titulo": "El Ejecutor",
                "descripcion": "Poder material, ambición, éxito, autoridad",
                "personalidad": "Tienes gran capacidad para el éxito material",
                "desafios": "Equilibra lo material con lo espiritual",
                "color": "Rosa", "planeta": "Saturno"
            },
            9: {
                "titulo": "El Humanitario",
                "descripcion": "Servicio universal, compasión, sabiduría, finalización",
                "personalidad": "Tienes una misión de servicio a la humanidad",
                "desafios": "No te pierdas en el drama emocional",
                "color": "Dorado", "planeta": "Marte"
            },
            11: {
                "titulo": "El Iluminador (Maestro)",
                "descripcion": "Intuición, iluminación, inspiración, liderazgo espiritual",
                "personalidad": "Posees gran intuición e inspiración",
                "desafios": "Mantén los pies en la tierra",
                "color": "Plata", "planeta": "Luna/Sol"
            },
            22: {
                "titulo": "El Constructor Maestro",
                "descripcion": "Construcción en gran escala, materialización de sueños",
                "personalidad": "Puedes materializar grandes visiones",
                "desafios": "No te abrumes con la magnitud",
                "color": "Oro", "planeta": "Urano/Tierra"
            },
            33: {
                "titulo": "El Maestro Sanador",
                "descripcion": "Sanación universal, maestría espiritual, sacrificio",
                "personalidad": "Tienes una misión de sanación mundial",
                "desafios": "Cuida tu propia energía",
                "color": "Blanco", "planeta": "Neptuno/Júpiter"
            }
        }
    
    def realizar_lectura(self, pregunta: str = "", parametros: Dict = None) -> ResultadoEsoterico:
        """Realiza análisis numerológico completo"""
        if not parametros:
            parametros = {}
        
        nombre = parametros.get('nombre', '')
        fecha_nacimiento = parametros.get('fecha_nacimiento', '')
        
        if not nombre or not fecha_nacimiento:
            return self._lectura_interactiva()
        
        return self._calcular_numerologia(nombre, fecha_nacimiento, pregunta)
    
    def _lectura_interactiva(self) -> ResultadoEsoterico:
        """Solicita datos al usuario de forma interactiva"""
        print("\n🔢 NUMEROLOGÍA COMPLETA 🔢")
        print("="*50)
        
        nombre = input("Ingresa tu nombre completo: ").strip()
        while True:
            try:
                fecha_str = input("Ingresa tu fecha de nacimiento (DD/MM/AAAA): ")
                dia, mes, año = map(int, fecha_str.split('/'))
                fecha_nacimiento = date(año, mes, dia)
                break
            except:
                print("Formato incorrecto. Usa DD/MM/AAAA")
        
        pregunta = input("¿Tienes alguna pregunta específica? (opcional): ").strip()
        
        return self._calcular_numerologia(nombre, fecha_str, pregunta)
    
    def _calcular_numerologia(self, nombre: str, fecha_nacimiento: str, pregunta: str) -> ResultadoEsoterico:
        """Calcula los números numerológicos principales"""
        
        # Número de la personalidad (suma de consonantes)
        consonantes = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
        suma_consonantes = sum(self._letra_a_numero(c) for c in nombre if c in consonantes)
        num_personalidad = self._reducir_numero(suma_consonantes)
        
        # Número del alma (suma de vocales)
        vocales = "aeiouAEIOU"
        suma_vocales = sum(self._letra_a_numero(c) for c in nombre if c in vocales)
        num_alma = self._reducir_numero(suma_vocales)
        
        # Número de destino (suma de todas las letras)
        suma_total = sum(self._letra_a_numero(c) for c in nombre if c.isalpha())
        num_destino = self._reducir_numero(suma_total)
        
        # Número de vida (fecha de nacimiento)
        try:
            dia, mes, año = map(int, fecha_nacimiento.split('/'))
            suma_fecha = dia + mes + año
            num_vida = self._reducir_numero(suma_fecha)
        except:
            num_vida = 1
        
        # Crear interpretación
        interpretacion = self._generar_interpretacion_numerologica(
            num_vida, num_destino, num_alma, num_personalidad, pregunta
        )
        
        detalles = {
            "numero_vida": num_vida,
            "numero_destino": num_destino,
            "numero_alma": num_alma,
            "numero_personalidad": num_personalidad,
            "significados": {
                "vida": self.significados_numeros.get(num_vida),
                "destino": self.significados_numeros.get(num_destino),
                "alma": self.significados_numeros.get(num_alma),
                "personalidad": self.significados_numeros.get(num_personalidad)
            },
            "nombre_analizado": nombre,
            "fecha_nacimiento": fecha_nacimiento
        }
        
        return ResultadoEsoterico(
            modalidad="Numerología",
            titulo=f"Perfil Numerológico de {nombre}",
            resultado_principal=f"Número de Vida: {num_vida} | Destino: {num_destino} | Alma: {num_alma} | Personalidad: {num_personalidad}",
            interpretacion=interpretacion,
            detalles_adicionales=detalles,
            fecha=datetime.now(),
            id_unico=self._generar_id_unico()
        )
    
    def _letra_a_numero(self, letra: str) -> int:
        """Convierte letra a su valor numerológico"""
        valores = {
            'a': 1, 'j': 1, 's': 1,
            'b': 2, 'k': 2, 't': 2,
            'c': 3, 'l': 3, 'u': 3,
            'd': 4, 'm': 4, 'v': 4,
            'e': 5, 'n': 5, 'w': 5,
            'f': 6, 'o': 6, 'x': 6,
            'g': 7, 'p': 7, 'y': 7,
            'h': 8, 'q': 8, 'z': 8,
            'i': 9, 'r': 9
        }
        return valores.get(letra.lower(), 0)
    
    def _reducir_numero(self, numero: int) -> int:
        """Reduce el número a un dígito (excepto 11, 22, 33)"""
        while numero > 9:
            if numero in [11, 22, 33]:
                return numero
            numero = sum(int(digito) for digito in str(numero))
        return numero
    
    def _generar_interpretacion_numerologica(self, vida: int, destino: int, 
                                           alma: int, personalidad: int, pregunta: str) -> str:
        """Genera interpretación completa"""
        
        interpretacion = f"""
🔮 Tu perfil numerológico revela una combinación única de energías:

📍 NÚMERO DE VIDA ({vida}): {self.significados_numeros[vida]['titulo']}
   {self.significados_numeros[vida]['personalidad']}
   
🎯 NÚMERO DE DESTINO ({destino}): {self.significados_numeros[destino]['titulo']}
   Tu propósito de vida está relacionado con {self.significados_numeros[destino]['descripcion'].lower()}
   
💫 NÚMERO DEL ALMA ({alma}): {self.significados_numeros[alma]['titulo']}
   Tu deseo más profundo es {self.significados_numeros[alma]['descripcion'].lower()}
   
🎭 NÚMERO DE PERSONALIDAD ({personalidad}): {self.significados_numeros[personalidad]['titulo']}
   Los demás te perciben como {self.significados_numeros[personalidad]['descripcion'].lower()}

🌈 COLORES DE PODER: {self.significados_numeros[vida]['color']}, {self.significados_numeros[destino]['color']}

⚠️  ÁREAS DE DESARROLLO:
   • {self.significados_numeros[vida]['desafios']}
   • {self.significados_numeros[destino]['desafios']}
        """
        
        if pregunta:
            interpretacion += f"\n\n❓ RESPECTO A TU PREGUNTA: '{pregunta}'\n"
            interpretacion += self._responder_pregunta_numerologica(vida, destino, alma, personalidad, pregunta)
        
        return interpretacion.strip()
    
    def _responder_pregunta_numerologica(self, vida: int, destino: int, 
                                        alma: int, personalidad: int, pregunta: str) -> str:
        """Responde pregunta específica basada en números"""
        
        # Análisis simple de palabras clave en la pregunta
        pregunta_lower = pregunta.lower()
        
        if any(palabra in pregunta_lower for palabra in ["amor", "pareja", "relación"]):
            if vida in [2, 6, 9]:
                return "Tus números sugieren gran capacidad para el amor y las relaciones. El momento es favorable."
            elif vida in [1, 8]:
                return "Tu independencia es fuerte. Busca balance entre tu autonomía y la pareja."
            else:
                return "En el amor, tu originalidad será tu mayor atractivo. Sé auténtico."
        
        elif any(palabra in pregunta_lower for palabra in ["trabajo", "carrera", "dinero"]):
            if vida in [4, 8, 22]:
                return "Tus números indican gran potencial para el éxito material y profesional."
            elif vida in [3, 5, 7]:
                return "Busca trabajos creativos o de comunicación. Tu talento único es tu valor."
            else:
                return "El éxito llegará a través del servicio a otros y siendo fiel a tus valores."
        
        elif any(palabra in pregunta_lower for palabra in ["salud", "bienestar"]):
            return "Tus números sugieren cuidar tanto el aspecto físico como el emocional. Busca equilibrio."
        
        else:
            numero_guia = (vida + destino + alma + personalidad) % 9
            if numero_guia == 0:
                numero_guia = 9
            return f"La respuesta está en el número {numero_guia}: {self.significados_numeros[numero_guia]['descripcion'].lower()}. Medita sobre esto."


class Runas(ModalidadEsoterica):
    """Sistema de runas nórdicas"""
    
    def __init__(self):
        super().__init__()
        self.nombre = "Runas Nórdicas"
        self.descripcion = "Antigua sabiduría nórdica a través de las runas del Futhark Antiguo"
        
        self.runas = {
            "Fehu": {
                "simbolo": "ᚠ",
                "nombre": "Fehu",
                "significado": "Ganado, riqueza, abundancia, nuevo comienzo",
                "elemento": "Fuego",
                "interpretacion": "Energía creativa en movimiento, prosperidad que llega, nuevos recursos"
            },
            "Uruz": {
                "simbolo": "ᚢ",
                "nombre": "Uruz", 
                "significado": "Uro salvaje, fuerza primitiva, vitalidad",
                "elemento": "Tierra",
                "interpretacion": "Fuerza interior sin domesticar, salud robusta, determinación"
            },
            "Thurisaz": {
                "simbolo": "ᚦ",
                "nombre": "Thurisaz",
                "significado": "Gigante, martillo de Thor, fuerza destructiva",
                "elemento": "Fuego",
                "interpretacion": "Fuerza que destruye para crear, protección, conflicto necesario"
            },
            "Ansuz": {
                "simbolo": "ᚨ",
                "nombre": "Ansuz",
                "significado": "Dios Odín, comunicación, inspiración divina",
                "elemento": "Aire",
                "interpretacion": "Mensajes divinos, sabiduría ancestral, comunicación sagrada"
            },
            "Raidho": {
                "simbolo": "ᚱ",
                "nombre": "Raidho",
                "significado": "Viaje, movimiento, ritmo",
                "elemento": "Aire",
                "interpretacion": "Viajes físicos o espirituales, progreso ordenado, aventura"
            },
            "Kenaz": {
                "simbolo": "ᚲ",
                "nombre": "Kenaz",
                "significado": "Antorcha, conocimiento, iluminación",
                "elemento": "Fuego",
                "interpretacion": "Conocimiento interno, creatividad ardiente, guía en la oscuridad"
            },
            "Gebo": {
                "simbolo": "ᚷ",
                "nombre": "Gebo",
                "significado": "Regalo, intercambio, generosidad",
                "elemento": "Aire",
                "interpretacion": "Equilibrio en el dar y recibir, partnerships, generosidad"
            },
            "Wunjo": {
                "simbolo": "ᚹ",
                "nombre": "Wunjo",
                "significado": "Alegría, armonía, realización",
                "elemento": "Agua",
                "interpretacion": "Alegría verdadera, armonía familiar, realización de deseos"
            },
            "Hagalaz": {
                "simbolo": "ᚺ",
                "nombre": "Hagalaz",
                "significado": "Granizo, destrucción natural, crisis",
                "elemento": "Agua",
                "interpretacion": "Crisis necesaria, destrucción que limpia, pruebas del destino"
            },
            "Nauthiz": {
                "simbolo": "ᚾ",
                "nombre": "Nauthiz",
                "significado": "Necesidad, resistencia, supervivencia",
                "elemento": "Fuego",
                "interpretacion": "Necesidad que enseña, resistencia desarrollada, supervivencia"
            },
            "Isa": {
                "simbolo": "ᛁ",
                "nombre": "Isa",
                "significado": "Hielo, pausa, reflexión",
                "elemento": "Agua",
                "interpretacion": "Pausa necesaria, tiempo de reflexión, preservación de energía"
            },
            "Jera": {
                "simbolo": "ᛃ",
                "nombre": "Jera",
                "significado": "Año, ciclos, cosecha",
                "elemento": "Tierra",
                "interpretacion": "Ciclos naturales, cosecha de esfuerzos, tiempo de recompensas"
            },
            "Eihwaz": {
                "simbolo": "ᛇ",
                "nombre": "Eihwaz",
                "significado": "Tejo, resistencia, conexión mundos",
                "elemento": "Tierra",
                "interpretacion": "Resistencia milenaria, conexión espiritual, protección duradera"
            },
            "Perthro": {
                "simbolo": "ᛈ",
                "nombre": "Perthro",
                "significado": "Pozo, misterio, destino oculto",
                "elemento": "Agua",
                "interpretacion": "Misterios por revelar, destino incierto, secretos del alma"
            },
            "Algiz": {
                "simbolo": "ᛉ",
                "nombre": "Algiz",
                "significado": "Alce, protección divina, conexión sagrada",
                "elemento": "Aire",
                "interpretacion": "Protección superior, conexión con lo sagrado, guía espiritual"
            },
            "Sowilo": {
                "simbolo": "ᛊ",
                "nombre": "Sowilo",
                "significado": "Sol, victoria, energía vital",
                "elemento": "Fuego",
                "interpretacion": "Victoria segura, energía solar, éxito brillante"
            },
            "Tiwaz": {
                "simbolo": "ᛏ",
                "nombre": "Tiwaz",
                "significado": "Dios Tyr, justicia, honor",
                "elemento": "Aire",
                "interpretacion": "Justicia divina, honor verdadero, sacrificio noble"
            },
            "Berkano": {
                "simbolo": "ᛒ",
                "nombre": "Berkano",
                "significado": "Abedul, renacimiento, feminidad",
                "elemento": "Tierra",
                "interpretacion": "Nuevos comienzos, fertilidad, cuidado maternal"
            },
            "Ehwaz": {
                "simbolo": "ᛖ",
                "nombre": "Ehwaz",
                "significado": "Caballo, cooperación, progreso",
                "elemento": "Tierra",
                "interpretacion": "Cooperación armónica, progreso conjunto, confianza mutua"
            },
            "Mannaz": {
                "simbolo": "ᛗ",
                "nombre": "Mannaz",
                "significado": "Humanidad, yo superior, colectivo",
                "elemento": "Aire",
                "interpretacion": "Conexión humana, desarrollo personal, responsabilidad social"
            },
            "Laguz": {
                "simbolo": "ᛚ",
                "nombre": "Laguz",
                "significado": "Agua, intuición, flujo",
                "elemento": "Agua",
                "interpretacion": "Intuición profunda, flujo emocional, adaptabilidad"
            },
            "Ingwaz": {
                "simbolo": "ᛜ",
                "nombre": "Ingwaz",
                "significado": "Dios Ing, fertilidad, potencial",
                "elemento": "Tierra",
                "interpretacion": "Potencial gestándose, fertilidad interna, energía acumulada"
            },
            "Othala": {
                "simbolo": "ᛟ",
                "nombre": "Othala",
                "significado": "Herencia ancestral, hogar, legado",
                "elemento": "Tierra",
                "interpretacion": "Legado ancestral, verdadero hogar, herencia espiritual"
            },
            "Dagaz": {
                "simbolo": "ᛞ",
                "nombre": "Dagaz",
                "significado": "Día, despertar, transformación",
                "elemento": "Fuego",
                "interpretacion": "Despertar espiritual, transformación radical, nueva consciencia"
            }
        }
        
        self.tipos_tirada = {
            "una_runa": {"nombre": "Runa del Día", "cantidad": 1, "posiciones": ["Mensaje del día"]},
            "tres_runas": {"nombre": "Pasado-Presente-Futuro", "cantidad": 3, "posiciones": ["Pasado", "Presente", "Futuro"]},
            "cinco_runas": {"nombre": "Cruz Rúnica", "cantidad": 5, "posiciones": ["Situación", "Desafío", "Pasado", "Futuro", "Resultado"]},
            "siete_runas": {"nombre": "Estrella de Siete", "cantidad": 7, "posiciones": ["Centro", "Norte", "Noreste", "Este", "Sureste", "Sur", "Suroeste"]},
            "nueve_runas": {"nombre": "Cuadrado Mágico", "cantidad": 9, "posiciones": ["Fundación", "Obstáculo", "Pasado distante", "Futuro posible", "Corona", "Futuro inmediato", "Yo interno", "Ambiente", "Esperanzas"]}
        }
    
    def realizar_lectura(self, pregunta: str = "", parametros: Dict = None) -> ResultadoEsoterico:
        """Realiza lectura de runas"""
        if not parametros:
            parametros = {}
        
        tipo_tirada = parametros.get('tipo_tirada', 'una_runa')
        
        if tipo_tirada not in self.tipos_tirada:
            tipo_tirada = 'tres_runas'
        
        return self._hacer_tirada_runas(tipo_tirada, pregunta)
    
    def _hacer_tirada_runas(self, tipo_tirada: str, pregunta: str) -> ResultadoEsoterico:
        """Realiza la tirada de runas específica"""
        info_tirada = self.tipos_tirada[tipo_tirada]
        nombres_runas = list(self.runas.keys())
        
        print(f"\n🔥 {info_tirada['nombre'].upper()} 🔥")
        print("="*50)
        print("Conectando con la sabiduría ancestral nórdica...")
        time.sleep(1)
        
        # Barajar las runas (simular sacarlas de una bolsa)
        if self.generador:
            runas_seleccionadas = []
            runas_disponibles = nombres_runas.copy()
            
            for i in range(info_tirada['cantidad']):
                indice = self.generador.obtener_indice_aleatorio(len(runas_disponibles))
                runa_elegida = runas_disponibles.pop(indice)
                
                # Determinar si está invertida (menos probable que en tarot)
                invertida = self.generador.obtener_bool_aleatorio() and random.random() < 0.3
                
                runas_seleccionadas.append({
                    'nombre': runa_elegida,
                    'posicion': info_tirada['posiciones'][i],
                    'invertida': invertida,
                    'info': self.runas[runa_elegida]
                })
                
                time.sleep(0.3)
        else:
            # Fallback sin generador avanzado
            runas_seleccionadas = []
            runas_disponibles = nombres_runas.copy()
            random.shuffle(runas_disponibles)
            
            for i in range(info_tirada['cantidad']):
                runa_elegida = runas_disponibles[i]
                invertida = random.random() < 0.3
                
                runas_seleccionadas.append({
                    'nombre': runa_elegida,
                    'posicion': info_tirada['posiciones'][i],
                    'invertida': invertida,
                    'info': self.runas[runa_elegida]
                })
        
        # Mostrar resultado
        resultado_texto = ""
        for i, runa in enumerate(runas_seleccionadas):
            estado = " (Invertida)" if runa['invertida'] else ""
            print(f"\n{i+1}. {runa['posicion']}: {runa['info']['simbolo']} {runa['nombre']}{estado}")
            print(f"   Elemento: {runa['info']['elemento']}")
            print(f"   Significado: {runa['info']['significado']}")
            print(f"   Interpretación: {runa['info']['interpretacion']}")
            if runa['invertida']:
                print(f"   ⚠️ Energía bloqueada o en proceso de desarrollo")
            resultado_texto += f"{runa['info']['simbolo']} {runa['nombre']} "
        
        # Generar interpretación
        interpretacion = self._generar_interpretacion_runas(runas_seleccionadas, pregunta, tipo_tirada)
        
        return ResultadoEsoterico(
            modalidad="Runas Nórdicas",
            titulo=f"Lectura Rúnica: {info_tirada['nombre']}",
            resultado_principal=resultado_texto.strip(),
            interpretacion=interpretacion,
            detalles_adicionales={
                "tipo_tirada": tipo_tirada,
                "runas_sacadas": runas_seleccionadas,
                "elementos_presentes": [r['info']['elemento'] for r in runas_seleccionadas]
            },
            fecha=datetime.now(),
            id_unico=self._generar_id_unico()
        )
    
    def _generar_interpretacion_runas(self, runas: List[Dict], pregunta: str, tipo_tirada: str) -> str:
        """Genera interpretación de la tirada de runas"""
        
        interpretacion = f"""
🔥 Los antiguos nórdicos han hablado a través de las runas sagradas:

"""
        
        if tipo_tirada == "una_runa":
            runa = runas[0]
            interpretacion += f"""La runa {runa['info']['simbolo']} {runa['nombre']} te acompaña hoy.
{runa['info']['interpretacion']}

El elemento {runa['info']['elemento']} guía tu energía del día."""
        
        elif tipo_tirada == "tres_runas":
            pasado, presente, futuro = runas
            interpretacion += f"""📍 PASADO: {pasado['info']['simbolo']} {pasado['nombre']}
   {pasado['info']['interpretacion']}
   
🎯 PRESENTE: {presente['info']['simbolo']} {presente['nombre']}
   {presente['info']['interpretacion']}
   
🌟 FUTURO: {futuro['info']['simbolo']} {futuro['nombre']}
   {futuro['info']['interpretacion']}"""
        
        else:
            # Tiradas más complejas
            interpretacion += "Las runas revelan múltiples aspectos:\n\n"
            for runa in runas:
                interpretacion += f"• {runa['posicion']}: {runa['info']['simbolo']} {runa['nombre']} - {runa['info']['interpretacion']}\n"
        
        # Análisis de elementos
        elementos = [r['info']['elemento'] for r in runas]
        elemento_dominante = max(set(elementos), key=elementos.count)
        
        interpretacion += f"""

🌀 ELEMENTO DOMINANTE: {elemento_dominante}
"""
        
        if elemento_dominante == "Fuego":
            interpretacion += "La energía del fuego domina: acción, pasión y transformación son clave."
        elif elemento_dominante == "Agua":
            interpretacion += "El flujo del agua prevalece: emociones, intuición y adaptabilidad guían tu camino."
        elif elemento_dominante == "Aire":
            interpretacion += "El elemento aire es fuerte: comunicación, ideas y conexiones mentales son importantes."
        else:  # Tierra
            interpretacion += "La estabilidad de la tierra se manifiesta: lo práctico, la paciencia y la construcción están en foco."
        
        if pregunta:
            interpretacion += f"""

❓ RESPECTO A TU PREGUNTA: "{pregunta}"
Las runas sugieren {self._interpretar_pregunta_runas(runas, pregunta)}"""
        
        return interpretacion
    
    def _interpretar_pregunta_runas(self, runas: List[Dict], pregunta: str) -> str:
        """Interpreta la pregunta específica con base en las runas"""
        
        # Contar runas "positivas" vs "desafiantes"
        runas_positivas = ["Fehu", "Wunjo", "Sowilo", "Jera", "Gebo", "Berkano", "Algiz"]
        runas_desafiantes = ["Hagalaz", "Nauthiz", "Thurisaz", "Isa", "Perthro"]
        
        positivas = sum(1 for r in runas if r['nombre'] in runas_positivas)
        desafiantes = sum(1 for r in runas if r['nombre'] in runas_desafiantes)
        
        if positivas > desafiantes:
            return "que la situación tiene aspectos favorables. Las fuerzas ancestrales te apoyan."
        elif desafiantes > positivas:
            return "que hay desafíos significativos, pero también oportunidades de crecimiento."
        else:
            return "que necesitas equilibrio y paciencia. Los antiguos aconsejan reflexión profunda."


class IChing(ModalidadEsoterica):
    """Sistema del I Ching (Libro de los Cambios)"""
    
    def __init__(self):
        super().__init__()
        self.nombre = "I Ching - Libro de los Cambios"
        self.descripcion = "Sabiduría milenaria china a través de los 64 hexagramas"
        
        # Solo incluiré algunos hexagramas representativos por brevedad
        self.hexagramas = {
            1: {
                "nombre": "Lo Creativo",
                "simbolo": "☰☰",
                "descripcion": "El Cielo sobre el Cielo",
                "significado": "Poder creativo primordial, liderazgo, fuerza yang",
                "consejo": "Es tiempo de actuar con firmeza y liderazgo natural",
                "trigrama_superior": "Cielo",
                "trigrama_inferior": "Cielo"
            },
            2: {
                "nombre": "Lo Receptivo", 
                "simbolo": "☷☷",
                "descripcion": "La Tierra sobre la Tierra",
                "significado": "Receptividad, nutrir, fuerza yin, paciencia",
                "consejo": "Cultiva la paciencia y la receptividad. Nutre lo que existe",
                "trigrama_superior": "Tierra",
                "trigrama_inferior": "Tierra"
            },
            3: {
                "nombre": "La Dificultad Inicial",
                "simbolo": "☵☳",
                "descripcion": "El Agua sobre el Trueno",
                "significado": "Comienzos difíciles, perseverancia necesaria",
                "consejo": "Los inicios son difíciles, pero persevera con ayuda de otros",
                "trigrama_superior": "Agua",
                "trigrama_inferior": "Trueno"
            },
            11: {
                "nombre": "La Paz",
                "simbolo": "☷☰",
                "descripcion": "La Tierra sobre el Cielo",
                "significado": "Armonía, equilibrio entre fuerzas opuestas, prosperidad",
                "consejo": "Momento de armonía y prosperidad. Mantén el equilibrio",
                "trigrama_superior": "Tierra", 
                "trigrama_inferior": "Cielo"
            },
            12: {
                "nombre": "El Estancamiento",
                "simbolo": "☰☷",
                "descripcion": "El Cielo sobre la Tierra",
                "significado": "Separación, estancamiento, comunicación bloqueada",
                "consejo": "Tiempo de retirada estratégica. No forces las situaciones",
                "trigrama_superior": "Cielo",
                "trigrama_inferior": "Tierra"
            },
            23: {
                "nombre": "La Desintegración",
                "simbolo": "☶☷",
                "descripción": "La Montaña sobre la Tierra",
                "significado": "Derrumbamiento de lo viejo, final necesario",
                "consejo": "Lo viejo debe caer para dar paso a lo nuevo",
                "trigrama_superior": "Montaña",
                "trigrama_inferior": "Tierra"
            },
            42: {
                "nombre": "El Aumento",
                "simbolo": "☴☳",
                "descripcion": "El Viento sobre el Trueno",
                "significado": "Crecimiento, progreso, beneficio mutuo",
                "consejo": "Tiempo favorable para el crecimiento y la expansión",
                "trigrama_superior": "Viento",
                "trigrama_inferior": "Trueno"
            },
            50: {
                "nombre": "El Caldero",
                "simbolo": "☲☴",
                "descripcion": "El Fuego sobre el Viento",
                "significado": "Transformación, nutrición espiritual, refinamiento",
                "consejo": "Transforma las experiencias crudas en sabiduría refinada",
                "trigrama_superior": "Fuego",
                "trigrama_inferior": "Viento"
            },
            64: {
                "nombre": "Antes de la Completitud",
                "simbolo": "☲☵",
                "descripcion": "El Fuego sobre el Agua",
                "significado": "Casi completado, últimas dificultades antes del éxito",
                "consejo": "Estás cerca del objetivo. Mantén la cautela y perseverancia",
                "trigrama_superior": "Fuego",
                "trigrama_inferior": "Agua"
            }
        }
        
        self.trigramas = {
            "☰": "Cielo", "☷": "Tierra", "☳": "Trueno", "☵": "Agua",
            "☶": "Montaña", "☴": "Viento", "☲": "Fuego", "☱": "Lago"
        }
    
    def realizar_lectura(self, pregunta: str = "", parametros: Dict = None) -> ResultadoEsoterico:
        """Realiza consulta al I Ching"""
        
        print("\n🏛️ I CHING - LIBRO DE LOS CAMBIOS 🏛️")
        print("="*50)
        
        if not pregunta:
            pregunta = input("Formúla tu pregunta al I Ching: ")
        
        print("\nLanzando las tres monedas seis veces...")
        print("Enfócate en tu pregunta mientras las monedas revelan el hexagrama...")
        time.sleep(2)
        
        # Generar hexagrama (método de 3 monedas)
        lineas = []
        for i in range(6):
            # Simular 3 monedas: cara=3, cruz=2
            monedas = [random.choice([2, 3]) for _ in range(3)]
            suma = sum(monedas)
            
            if suma == 6:  # 3 caras
                linea = "yang_viejo"  # se convierte en yin
                simbolo = "⚏"
            elif suma == 9:  # 3 cruces
                linea = "yin_viejo"   # se convierte en yang
                simbolo = "⚎"
            elif suma == 7:  # 2 caras, 1 cruz
                linea = "yang"
                simbolo = "⚊"
            else:  # suma == 8, 1 cara, 2 cruces
                linea = "yin"
                simbolo = "⚋"
            
            lineas.append({'tipo': linea, 'simbolo': simbolo})
            print(f"Línea {i+1}: {simbolo} ({linea})")
            time.sleep(0.5)
        
        # Determinar hexagrama (simplificado)
        numero_hex = self._calcular_hexagrama(lineas)
        hexagrama_info = self.hexagramas.get(numero_hex, self.hexagramas[1])
        
        # Verificar si hay líneas cambiantes
        lineas_cambiantes = [i for i, l in enumerate(lineas) if 'viejo' in l['tipo']]
        
        interpretacion = self._generar_interpretacion_iching(
            hexagrama_info, numero_hex, lineas_cambiantes, pregunta
        )
        
        return ResultadoEsoterico(
            modalidad="I Ching",
            titulo=f"Hexagrama {numero_hex}: {hexagrama_info['nombre']}",
            resultado_principal=f"{hexagrama_info['simbolo']} - {hexagrama_info['descripcion']}",
            interpretacion=interpretacion,
            detalles_adicionales={
                "numero_hexagrama": numero_hex,
                "lineas": lineas,
                "lineas_cambiantes": lineas_cambiantes,
                "trigramas": {
                    "superior": hexagrama_info['trigrama_superior'],
                    "inferior": hexagrama_info['trigrama_inferior']
                }
            },
            fecha=datetime.now(),
            id_unico=self._generar_id_unico()
        )
    
    def _calcular_hexagrama(self, lineas: List[Dict]) -> int:
        """Calcula el número del hexagrama (simplificado)"""
        # Método simplificado basado en patrones de líneas
        patron = ''.join(['1' if 'yang' in l['tipo'] else '0' for l in lineas])
        # Convertir binario a decimal y mapear a hexagramas disponibles
        valor = int(patron, 2)
        hexagramas_disponibles = list(self.hexagramas.keys())
        return hexagramas_disponibles[valor % len(hexagramas_disponibles)]
    
    def _generar_interpretacion_iching(self, hexagrama: Dict, numero: int,
                                      lineas_cambiantes: List[int], pregunta: str) -> str:
        """Genera interpretación del I Ching"""
        
        interpretacion = f"""
🏛️ El I Ching ha hablado:

HEXAGRAMA {numero}: {hexagrama['nombre']}
{hexagrama['simbolo']} - {hexagrama['descripcion']}

💫 SIGNIFICADO:
{hexagrama['significado']}

🎯 CONSEJO:
{hexagrama['consejo']}

🔄 ESTRUCTURA:
• Trigrama Superior: {hexagrama['trigrama_superior']} - Representa la situación externa
• Trigrama Inferior: {hexagrama['trigrama_inferior']} - Representa la situación interna
"""
        
        if lineas_cambiantes:
            interpretacion += f"""
⚡ LÍNEAS CAMBIANTES:
Hay {len(lineas_cambiantes)} líneas en transformación (posiciones: {[l+1 for l in lineas_cambiantes]})
Esto indica que la situación está en proceso de cambio dinámico.
"""
        else:
            interpretacion += """
🔒 SITUACIÓN ESTABLE:
No hay líneas cambiantes. La situación es estable en este momento.
"""
        
        if pregunta:
            interpretacion += f"""
❓ RESPECTO A TU PREGUNTA: "{pregunta}"

{self._interpretar_pregunta_iching(hexagrama, numero, lineas_cambiantes)}
"""
        
        interpretacion += """
🧘 MEDITACIÓN:
Reflexiona sobre cómo estos principios se aplican a tu situación actual.
El I Ching no predice el futuro, sino que revela las tendencias presentes.
"""
        
        return interpretacion
    
    def _interpretar_pregunta_iching(self, hexagrama: Dict, numero: int, 
                                    lineas_cambiantes: List[int]) -> str:
        """Interpreta la pregunta específica"""
        
        if numero in [1, 11, 42]:  # Hexagramas favorables
            respuesta = "Los signos son favorables. La energía fluye en dirección positiva."
        elif numero in [12, 23]:   # Hexagramas de desafío
            respuesta = "Hay obstáculos presentes, pero también oportunidades de crecimiento."
        else:
            respuesta = "La situación requiere equilibrio y paciencia."
        
        if lineas_cambiantes:
            respuesta += " Los cambios están en marcha - permanece atento a las oportunidades."
        else:
            respuesta += " Mantén tu curso actual con sabiduría."
        
        return respuesta


# Continúa con más modalidades...

class OraculoSiNo(ModalidadEsoterica):
    """Oráculo simple de Sí/No con variaciones"""
    
    def __init__(self):
        super().__init__()
        self.nombre = "Oráculo Sí/No"
        self.descripcion = "Respuestas directas del universo a preguntas específicas"
        
        self.respuestas = {
            "si_fuerte": {
                "respuesta": "SÍ DEFINITIVO",
                "descripcion": "El universo responde con un SÍ rotundo",
                "emoji": "✅",
                "color": "verde_brillante"
            },
            "si": {
                "respuesta": "SÍ",
                "descripcion": "La respuesta es afirmativa",
                "emoji": "✔️",
                "color": "verde"
            },
            "si_probable": {
                "respuesta": "PROBABLEMENTE SÍ",
                "descripcion": "Las posibilidades son favorables",
                "emoji": "🌟",
                "color": "verde_claro"
            },
            "neutral": {
                "respuesta": "NEUTRO / DEPENDE DE TI",
                "descripcion": "La respuesta está en tus manos",
                "emoji": "⚖️",
                "color": "amarillo"
            },
            "no_probable": {
                "respuesta": "PROBABLEMENTE NO",
                "descripcion": "Las energías no favorecen esta dirección",
                "emoji": "🤔",
                "color": "naranja"
            },
            "no": {
                "respuesta": "NO",
                "descripcion": "La respuesta es negativa",
                "emoji": "❌",
                "color": "rojo"
            },
            "no_fuerte": {
                "respuesta": "NO DEFINITIVO",
                "descripcion": "El universo te aconseja alejarte de esta opción",
                "emoji": "🚫",
                "color": "rojo_oscuro"
            },
            "espera": {
                "respuesta": "ESPERA",
                "descripcion": "No es el momento adecuado. Ten paciencia",
                "emoji": "⏳",
                "color": "azul"
            },
            "replantea": {
                "respuesta": "REPLANTEA LA PREGUNTA",
                "descripcion": "La pregunta necesita ser más específica",
                "emoji": "🔄",
                "color": "morado"
            }
        }
    
    def realizar_lectura(self, pregunta: str = "", parametros: Dict = None) -> ResultadoEsoterico:
        """Realiza consulta de Sí/No"""
        
        print("\n🔮 ORÁCULO SÍ/NO 🔮")
        print("="*40)
        
        if not pregunta:
            pregunta = input("Haz una pregunta que pueda responderse con Sí o No: ")
        
        print("\nConsultando al oráculo universal...")
        time.sleep(1.5)
        
        # Múltiples métodos de aleatoriedad
        if self.generador:
            # Método 1: Generador avanzado
            valor1 = self.generador.obtener_indice_aleatorio(100)
            
            # Método 2: Tiempo
            valor2 = int(time.time() * 1000) % 100
            
            # Método 3: Secretos
            valor3 = secrets.randbelow(100)
            
            # Combinar valores
            valor_final = (valor1 + valor2 + valor3) % 100
        else:
            valor_final = random.randint(0, 99)
        
        # Determinar respuesta basada en probabilidades
        if valor_final < 5:
            clave_respuesta = "replantea"
        elif valor_final < 10:
            clave_respuesta = "espera"
        elif valor_final < 15:
            clave_respuesta = "no_fuerte"
        elif valor_final < 30:
            clave_respuesta = "no"
        elif valor_final < 40:
            clave_respuesta = "no_probable"
        elif valor_final < 50:
            clave_respuesta = "neutral"
        elif valor_final < 65:
            clave_respuesta = "si_probable"
        elif valor_final < 85:
            clave_respuesta = "si"
        else:
            clave_respuesta = "si_fuerte"
        
        respuesta_info = self.respuestas[clave_respuesta]
        
        # Generar interpretación adicional
        interpretacion_adicional = self._generar_interpretacion_contexto(pregunta, respuesta_info, valor_final)
        
        return ResultadoEsoterico(
            modalidad="Oráculo Sí/No",
            titulo="Respuesta del Oráculo",
            resultado_principal=f"{respuesta_info['emoji']} {respuesta_info['respuesta']}",
            interpretacion=f"{respuesta_info['descripcion']}\n\n{interpretacion_adicional}",
            detalles_adicionales={
                "valor_aleatorio": valor_final,
                "tipo_respuesta": clave_respuesta,
                "pregunta_original": pregunta
            },
            fecha=datetime.now(),
            id_unico=self._generar_id_unico()
        )
    
    def _generar_interpretacion_contexto(self, pregunta: str, respuesta_info: Dict, valor: int) -> str:
        """Genera interpretación contextual adicional"""
        
        pregunta_lower = pregunta.lower()
        interpretacion = ""
        
        # Análisis contextual básico
        if any(palabra in pregunta_lower for palabra in ["amor", "relación", "pareja"]):
            if "si" in respuesta_info["respuesta"].lower():
                interpretacion += "💕 En el amor, las energías se alinean favorablemente. "
            elif "no" in respuesta_info["respuesta"].lower():
                interpretacion += "💔 En asuntos del corazón, tal vez sea momento de reflexionar. "
            else:
                interpretacion += "💭 En el amor, la respuesta está en tu propio corazón. "
        
        elif any(palabra in pregunta_lower for palabra in ["trabajo", "empleo", "carrera"]):
            if "si" in respuesta_info["respuesta"].lower():
                interpretacion += "💼 Profesionalmente, los caminos se abren. "
            elif "no" in respuesta_info["respuesta"].lower():
                interpretacion += "📊 En lo profesional, considera otras alternativas. "
            else:
                interpretacion += "🎯 Tu carrera depende de tu propia determinación. "
        
        elif any(palabra in pregunta_lower for palabra in ["dinero", "económico", "financiero"]):
            if "si" in respuesta_info["respuesta"].lower():
                interpretacion += "💰 Las finanzas muestran signos positivos. "
            elif "no" in respuesta_info["respuesta"].lower():
                interpretacion += "💸 Cuidado con las decisiones financieras apresuradas. "
            else:
                interpretacion += "💳 La estabilidad económica depende de tu planificación. "
        
        # Consejo adicional basado en el valor
        if valor < 25:
            interpretacion += "Considera esperar el momento más propicio."
        elif valor > 75:
            interpretacion += "La energía está en su punto más alto para actuar."
        else:
            interpretacion += "Confía en tu intuición para tomar la mejor decisión."
        
        return interpretacion


class Horoscopo(ModalidadEsoterica):
    """Sistema de horóscopo astrológico personalizado"""
    
    def __init__(self):
        super().__init__()
        self.nombre = "Horóscopo Personalizado"
        self.descripcion = "Predicciones astrológicas basadas en tu signo zodiacal"
        
        self.signos_zodiacales = {
            "aries": {
                "nombre": "Aries",
                "simbolo": "♈",
                "elemento": "Fuego",
                "planeta": "Marte",
                "fechas": "21 marzo - 19 abril",
                "cualidades": ["liderazgo", "energía", "valentía", "iniciativa"],
                "desafios": ["impaciencia", "impulsividad", "agresividad"]
            },
            "tauro": {
                "nombre": "Tauro", 
                "simbolo": "♉",
                "elemento": "Tierra",
                "planeta": "Venus",
                "fechas": "20 abril - 20 mayo",
                "cualidades": ["estabilidad", "determinación", "sensualidad", "practicidad"],
                "desafios": ["terquedad", "resistencia al cambio", "materialismo"]
            },
            "geminis": {
                "nombre": "Géminis",
                "simbolo": "♊", 
                "elemento": "Aire",
                "planeta": "Mercurio",
                "fechas": "21 mayo - 20 junio",
                "cualidades": ["comunicación", "versatilidad", "curiosidad", "adaptabilidad"],
                "desafios": ["dispersión", "superficialidad", "nerviosismo"]
            },
            "cancer": {
                "nombre": "Cáncer",
                "simbolo": "♋",
                "elemento": "Agua", 
                "planeta": "Luna",
                "fechas": "21 junio - 22 julio",
                "cualidades": ["intuición", "sensibilidad", "protección", "empatía"],
                "desafios": ["exceso emocional", "inseguridad", "tendencia a refugiarse"]
            },
            "leo": {
                "nombre": "Leo",
                "simbolo": "♌",
                "elemento": "Fuego",
                "planeta": "Sol", 
                "fechas": "23 julio - 22 agosto",
                "cualidades": ["creatividad", "generosidad", "liderazgo", "carisma"],
                "desafios": ["orgullo", "arrogancia", "necesidad de atención"]
            },
            "virgo": {
                "nombre": "Virgo",
                "simbolo": "♍",
                "elemento": "Tierra",
                "planeta": "Mercurio",
                "fechas": "23 agosto - 22 septiembre", 
                "cualidades": ["perfeccionismo", "análisis", "servicio", "organización"],
                "desafios": ["crítica excesiva", "preocupación", "detallismo extremo"]
            },
            "libra": {
                "nombre": "Libra", 
                "simbolo": "♎",
                "elemento": "Aire",
                "planeta": "Venus",
                "fechas": "23 septiembre - 22 octubre",
                "cualidades": ["equilibrio", "justicia", "diplomacia", "estética"],
                "desafios": ["indecisión", "dependencia", "evitar conflictos"]
            },
            "escorpio": {
                "nombre": "Escorpio",
                "simbolo": "♏",
                "elemento": "Agua",
                "planeta": "Plutón",
                "fechas": "23 octubre - 21 noviembre",
                "cualidades": ["intensidad", "transformación", "investigación", "magnetismo"],
                "desafios": ["obsesión", "venganza", "secretismo"]
            },
            "sagitario": {
                "nombre": "Sagitario",
                "simbolo": "♐",
                "elemento": "Fuego", 
                "planeta": "Júpiter",
                "fechas": "22 noviembre - 21 diciembre",
                "cualidades": ["aventura", "filosofía", "optimismo", "libertad"],
                "desafios": ["exageración", "falta de compromiso", "imprudencia"]
            },
            "capricornio": {
                "nombre": "Capricornio",
                "simbolo": "♑",
                "elemento": "Tierra",
                "planeta": "Saturno",
                "fechas": "22 diciembre - 19 enero",
                "cualidades": ["ambición", "disciplina", "responsabilidad", "perseverancia"],
                "desafios": ["rigidez", "pesimismo", "exceso de trabajo"]
            },
            "acuario": {
                "nombre": "Acuario", 
                "simbolo": "♒",
                "elemento": "Aire",
                "planeta": "Urano",
                "fechas": "20 enero - 18 febrero",
                "cualidades": ["originalidad", "humanitarismo", "innovación", "independencia"],
                "desafios": ["rebeldía", "frialdad emocional", "distanciamiento"]
            },
            "piscis": {
                "nombre": "Piscis",
                "simbolo": "♓",
                "elemento": "Agua",
                "planeta": "Neptuno", 
                "fechas": "19 febrero - 20 marzo",
                "cualidades": ["compasión", "intuición", "creatividad", "espiritualidad"],
                "desafios": ["escapismo", "confusión", "victimización"]
            }
        }
        
        self.areas_vida = {
            "amor": ["relaciones", "romance", "corazón", "pareja", "matrimonio"],
            "trabajo": ["carrera", "profesión", "empleo", "negocios", "dinero"],
            "salud": ["bienestar", "energía", "vitalidad", "cuidado personal"],
            "familia": ["hogar", "parientes", "hijos", "padres", "tradiciones"],
            "amistad": ["amigos", "social", "comunicación", "redes"],
            "espiritualidad": ["crecimiento", "meditación", "propósito", "sabiduría"]
        }
    
    def realizar_lectura(self, pregunta: str = "", parametros: Dict = None) -> ResultadoEsoterico:
        """Realiza lectura de horóscopo personalizada"""
        if not parametros:
            parametros = {}
        
        signo = parametros.get('signo', '').lower()
        
        if signo not in self.signos_zodiacales:
            return self._lectura_interactiva_horoscopo()
        
        return self._generar_horoscopo(signo, pregunta)
    
    def _lectura_interactiva_horoscopo(self) -> ResultadoEsoterico:
        """Solicita signo zodiacal de forma interactiva"""
        print("\n⭐ HORÓSCOPO PERSONALIZADO ⭐")
        print("="*50)
        
        print("Signos Zodiacales disponibles:")
        for i, (key, signo) in enumerate(self.signos_zodiacales.items(), 1):
            print(f"{i:2d}. {signo['simbolo']} {signo['nombre']} ({signo['fechas']})")
        
        while True:
            try:
                opcion = int(input("\nElige tu signo zodiacal (1-12): "))
                if 1 <= opcion <= 12:
                    signo_key = list(self.signos_zodiacales.keys())[opcion - 1]
                    break
                else:
                    print("❌ Opción fuera de rango. Elige entre 1 y 12.")
            except ValueError:
                print("❌ Por favor ingresa un número válido.")
        
        pregunta = input("\n¿En qué área te interesa la predicción? (amor/trabajo/salud/familia/general): ").strip().lower()
        
        return self._generar_horoscopo(signo_key, pregunta)
    
    def _generar_horoscopo(self, signo: str, area_consulta: str) -> ResultadoEsoterico:
        """Genera horóscopo personalizado"""
        info_signo = self.signos_zodiacales[signo]
        
        print(f"\n⭐ HORÓSCOPO PARA {info_signo['nombre'].upper()} {info_signo['simbolo']} ⭐")
        print("="*50)
        print("Consultando las estrellas y planetas...")
        time.sleep(2)
        
        # Generar predicciones basadas en área específica o general
        if area_consulta in self.areas_vida:
            prediccion = self._generar_prediccion_especifica(info_signo, area_consulta)
        else:
            prediccion = self._generar_prediccion_general(info_signo)
        
        # Agregar consejo del día
        consejo_dia = self._generar_consejo_dia(info_signo)
        
        # Números de la suerte
        numeros_suerte = self._generar_numeros_suerte()
        
        # Color del día
        color_dia = self._determinar_color_dia(info_signo)
        
        interpretacion_completa = f"""
⭐ PREDICCIÓN ASTROLÓGICA PARA {info_signo['nombre'].upper()} ⭐

{prediccion}

💫 CONSEJO DEL DÍA:
{consejo_dia}

🎨 COLOR FAVORABLE: {color_dia}
Usar este color te ayudará a atraer las energías positivas.

🎲 NÚMEROS DE LA SUERTE: {', '.join(map(str, numeros_suerte))}

🌟 CUALIDADES A POTENCIAR HOY:
• {info_signo['cualidades'][0].title()}
• {info_signo['cualidades'][1].title()}

⚠️ PRECAUCIONES:
Evita caer en {info_signo['desafios'][0]} y {info_signo['desafios'][1]}.

🪐 INFLUENCIA PLANETARIA:
Tu planeta regente {info_signo['planeta']} está influyendo positivamente en las decisiones de hoy.
"""
        
        return ResultadoEsoterico(
            modalidad="Horóscopo",
            titulo=f"Horóscopo {info_signo['nombre']} - {datetime.now().strftime('%d/%m/%Y')}",
            resultado_principal=f"{info_signo['simbolo']} {info_signo['nombre']} - {area_consulta.title() if area_consulta in self.areas_vida else 'General'}",
            interpretacion=interpretacion_completa,
            detalles_adicionales={
                "signo": signo,
                "info_signo": info_signo,
                "area_consulta": area_consulta,
                "numeros_suerte": numeros_suerte,
                "color_dia": color_dia
            },
            fecha=datetime.now(),
            id_unico=self._generar_id_unico()
        )
    
    def _generar_prediccion_especifica(self, info_signo: Dict, area: str) -> str:
        """Genera predicción para área específica"""
        elemento = info_signo['elemento']
        planeta = info_signo['planeta']
        
        predicciones_base = {
            "amor": {
                "Fuego": f"Tu naturaleza ardiente de {elemento} atrae el amor verdadero. {planeta} favorece encuentros románticos.",
                "Tierra": f"La estabilidad de {elemento} construye relaciones duraderas. {planeta} trae armonía sentimental.",
                "Aire": f"Tu comunicación natural facilita conexiones profundas. {planeta} inspira conversaciones románticas.",
                "Agua": f"Tu sensibilidad emocional profundiza los vínculos. {planeta} intensifica los sentimientos."
            },
            "trabajo": {
                "Fuego": f"Tu liderazgo natural brilla en proyectos importantes. {planeta} impulsa tu ambición profesional.",
                "Tierra": f"Tu practicidad resuelve problemas complejos. {planeta} estabiliza tu situación laboral.",
                "Aire": f"Tus ideas innovadoras son reconocidas. {planeta} favorece la comunicación profesional.",
                "Agua": f"Tu intuición guía decisiones acertadas. {planeta} fluye en colaboraciones exitosas."
            },
            "salud": {
                "Fuego": f"Tu energía vital está en su punto máximo. {planeta} fortalece tu sistema inmunológico.",
                "Tierra": f"Tu cuerpo responde bien a rutinas saludables. {planeta} favorece la recuperación física.",
                "Aire": f"Tu mente necesita ejercicio y estimulación. {planeta} mejora tu capacidad de concentración.",
                "Agua": f"Tus emociones afectan tu bienestar físico. {planeta} promueve el equilibrio interno."
            },
            "familia": {
                "Fuego": f"Tu carisma reúne a la familia en momentos importantes. {planeta} fortalece los lazos familiares.",
                "Tierra": f"Tu estabilidad es el refugio de tus seres queridos. {planeta} consolida las tradiciones.",
                "Aire": f"Tu comunicación resuelve malentendidos familiares. {planeta} facilita reuniones armoniosas.",
                "Agua": f"Tu comprensión emocional sana heridas del pasado. {planeta} intensifica el amor familiar."
            }
        }
        
        return predicciones_base.get(area, {}).get(elemento, 
            f"Las estrellas están alineadas favorablemente para ti en el área de {area}.")
    
    def _generar_prediccion_general(self, info_signo: Dict) -> str:
        """Genera predicción general"""
        elemento = info_signo['elemento']
        
        predicciones_generales = {
            "Fuego": "Día de gran energía y acción. Tu iniciativa abre nuevos caminos y oportunidades.",
            "Tierra": "Jornada de estabilidad y construcción. Tus esfuerzos constantes dan frutos tangibles.",
            "Aire": "Momento de comunicación y conexiones. Las ideas fluyen y los contactos se multiplican.",
            "Agua": "Período de intuición y emociones profundas. Confía en tus sentimientos internos."
        }
        
        return predicciones_generales.get(elemento, "Las energías cósmicas te favorecen hoy.")
    
    def _generar_consejo_dia(self, info_signo: Dict) -> str:
        """Genera consejo específico del día"""
        consejos = [
            f"Aprovecha tu don natural de {info_signo['cualidades'][0]} para resolver situaciones pendientes.",
            f"Tu {info_signo['cualidades'][1]} será la clave del éxito hoy.",
            f"Conecta con la energía de {info_signo['planeta']} a través de la meditación matutina.",
            f"El elemento {info_signo['elemento']} te guía hacia decisiones acertadas."
        ]
        
        return random.choice(consejos)
    
    def _generar_numeros_suerte(self) -> List[int]:
        """Genera números de la suerte"""
        if self.generador:
            return [self.generador.obtener_indice_aleatorio(99) + 1 for _ in range(6)]
        else:
            return [random.randint(1, 99) for _ in range(6)]
    
    def _determinar_color_dia(self, info_signo: Dict) -> str:
        """Determina color favorable del día"""
        colores_elemento = {
            "Fuego": ["Rojo", "Naranja", "Dorado", "Amarillo brillante"],
            "Tierra": ["Verde", "Marrón", "Beige", "Terracota"],
            "Aire": ["Azul claro", "Blanco", "Plata", "Celeste"],
            "Agua": ["Azul marino", "Turquesa", "Violeta", "Verde agua"]
        }
        
        colores_disponibles = colores_elemento.get(info_signo['elemento'], ["Blanco"])
        return random.choice(colores_disponibles)


class SistemaEsotericoExpandido:
    """Sistema principal que coordina todas las modalidades esotéricas"""
    
    def __init__(self):
        self.modalidades = {
            TipoModalidad.NUMEROLOGIA: Numerologia(),
            TipoModalidad.RUNAS: Runas(),
            TipoModalidad.I_CHING: IChing(),
            TipoModalidad.ORACULO_SI_NO: OraculoSiNo(),
            TipoModalidad.HOROSCOPO: Horoscopo(),
            # Se pueden agregar más modalidades aquí
        }
        
        # Si el tarot está disponible, agregarlo
        if 'LectorTarot' in globals():
            self.lector_tarot = LectorTarot()
        else:
            self.lector_tarot = None
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal con todas las modalidades"""
        
        print("\n" + "="*70)
        print("🌟  SISTEMA ESOTÉRICO EXPANDIDO  🌟")
        print("Múltiples caminos hacia la sabiduría universal")
        print("="*70)
        
        opciones = []
        
        # Modalidades nuevas
        opciones.extend([
            "1. 🔢 Numerología Completa - Análisis de tu nombre y fecha de nacimiento",
            "2. 🔥 Runas Nórdicas - Sabiduría ancestral vikinga",
            "3. 🏛️ I Ching - Libro de los Cambios chino",
            "4. 🔮 Oráculo Sí/No - Respuestas directas del universo",
            "5. ⭐ Horóscopo Personalizado - Predicciones astrológicas diarias"
        ])
        
        # Tarot si está disponible
        if self.lector_tarot:
            opciones.extend([
                "6. 🎴 Tarot Completo - Lectura de cartas tradicional",
                "7. 🌙 Lectura Combinada - Múltiples sistemas a la vez"
            ])
        
        opciones.extend([
            "0. ✨ Salir"
        ])
        
        for opcion in opciones:
            print(opcion)
        
        return len(opciones) - 1  # Número de opciones sin contar salir
    
    def ejecutar_sistema(self):
        """Ejecuta el sistema principal con menú interactivo"""
        
        while True:
            max_opciones = self.mostrar_menu_principal()
            
            try:
                opcion = int(input(f"\nElige una opción (0-{max_opciones}): "))
                
                if opcion == 0:
                    print("\n✨ Que la sabiduría universal te acompañe siempre ✨")
                    break
                
                elif opcion == 1:
                    self._ejecutar_modalidad(TipoModalidad.NUMEROLOGIA)
                
                elif opcion == 2:
                    self._ejecutar_modalidad(TipoModalidad.RUNAS)
                
                elif opcion == 3:
                    self._ejecutar_modalidad(TipoModalidad.I_CHING)
                
                elif opcion == 4:
                    self._ejecutar_modalidad(TipoModalidad.ORACULO_SI_NO)
                
                elif opcion == 5:
                    self._ejecutar_modalidad(TipoModalidad.HOROSCOPO)
                
                elif opcion == 6 and self.lector_tarot:
                    self._ejecutar_tarot()
                
                elif opcion == 7 and self.lector_tarot:
                    self._ejecutar_lectura_combinada()
                
                else:
                    print("\n❌ Opción no válida")
                
            except ValueError:
                print("\n❌ Por favor ingresa un número válido")
            
            input("\nPresiona Enter para continuar...")
    
    def _ejecutar_modalidad(self, tipo_modalidad: TipoModalidad):
        """Ejecuta una modalidad específica"""
        modalidad = self.modalidades[tipo_modalidad]
        
        print(f"\n🌟 {modalidad.nombre} 🌟")
        print(modalidad.descripcion)
        print("-" * 50)
        
        try:
            resultado = modalidad.realizar_lectura()
            self._mostrar_resultado(resultado)
            
            # Preguntar si guardar
            guardar = input("\n¿Deseas guardar esta lectura? (s/n): ").lower()
            if guardar == 's':
                self._guardar_resultado(resultado)
                
        except Exception as e:
            print(f"\n❌ Error en la lectura: {e}")
    
    def _ejecutar_tarot(self):
        """Ejecuta lectura de tarot tradicional"""
        if not self.lector_tarot:
            print("❌ Sistema de tarot no disponible")
            return
        
        print("\n🎴 SELECCIONAR TIPO DE TIRADA 🎴")
        print("1. Una Carta del Día")
        print("2. Pasado, Presente y Futuro (3 cartas)")
        print("3. Cruz Celta (10 cartas)")
        print("4. Herradura (7 cartas)")
        print("5. Lectura de Relación (6 cartas)")
        print("6. Lectura de Amor (7 cartas)")
        
        try:
            opcion_tarot = int(input("\nElige tipo de tirada (1-6): "))
            
            tipos_map = {
                1: TipoTirada.UNA_CARTA,
                2: TipoTirada.TRES_CARTAS,
                3: TipoTirada.CRUZ_CELTA,
                4: TipoTirada.HERRADURA,
                5: TipoTirada.RELACION,
                6: TipoTirada.AMOR
            }
            
            if opcion_tarot in tipos_map:
                pregunta = input("\n¿Cuál es tu pregunta? (opcional): ").strip()
                resultado_tarot = self.lector_tarot.realizar_lectura(tipos_map[opcion_tarot], pregunta)
                
                # Convertir formato del tarot al formato estándar
                resultado = ResultadoEsoterico(
                    modalidad="Tarot",
                    titulo=resultado_tarot["tipo_tirada"],
                    resultado_principal=f"{len(resultado_tarot['cartas'])} cartas reveladas",
                    interpretacion=resultado_tarot["interpretacion"],
                    detalles_adicionales=resultado_tarot,
                    fecha=datetime.fromisoformat(resultado_tarot["fecha"]),
                    id_unico=resultado_tarot["semilla_lectura"]
                )
                
                self._mostrar_resultado(resultado)
                
                guardar = input("\n¿Deseas guardar esta lectura? (s/n): ").lower()
                if guardar == 's':
                    self.lector_tarot.guardar_lectura(resultado_tarot)
            
        except Exception as e:
            print(f"❌ Error en lectura de tarot: {e}")
    
    def _ejecutar_lectura_combinada(self):
        """Ejecuta lectura combinando múltiples sistemas"""
        print("\n🌈 LECTURA COMBINADA - MÚLTIPLES SISTEMAS 🌈")
        print("Se consultarán varios sistemas para una perspectiva completa")
        print("-" * 60)
        
        pregunta = input("¿Cuál es tu pregunta principal? (importante para lectura combinada): ").strip()
        
        if not pregunta:
            print("❌ Para una lectura combinada necesitas formular una pregunta específica")
            return
        
        resultados = []
        
        # Oráculo Sí/No como base
        print("\n1️⃣ Consultando Oráculo Sí/No...")
        resultado_oraculo = self.modalidades[TipoModalidad.ORACULO_SI_NO].realizar_lectura(pregunta)
        resultados.append(resultado_oraculo)
        
        # Runas para el contexto
        print("\n2️⃣ Consultando Runas Nórdicas...")
        resultado_runas = self.modalidades[TipoModalidad.RUNAS].realizar_lectura(
            pregunta, {"tipo_tirada": "tres_runas"}
        )
        resultados.append(resultado_runas)
        
        # I Ching para la sabiduría profunda
        print("\n3️⃣ Consultando I Ching...")
        resultado_iching = self.modalidades[TipoModalidad.I_CHING].realizar_lectura(pregunta)
        resultados.append(resultado_iching)
        
        # Mostrar síntesis
        self._mostrar_lectura_combinada(pregunta, resultados)
    
    def _mostrar_resultado(self, resultado: ResultadoEsoterico):
        """Muestra un resultado de forma formateada"""
        print("\n" + "="*60)
        print(f"📋 {resultado.titulo}")
        print("="*60)
        print(f"🎯 Resultado: {resultado.resultado_principal}")
        print(f"\n📖 Interpretación:\n{resultado.interpretacion}")
        print(f"\n🕐 Fecha: {resultado.fecha.strftime('%d/%m/%Y %H:%M')}")
        print(f"🆔 ID: {resultado.id_unico}")
        print("="*60)
    
    def _mostrar_lectura_combinada(self, pregunta: str, resultados: List[ResultadoEsoterico]):
        """Muestra síntesis de lectura combinada"""
        print("\n" + "="*70)
        print("🌈 SÍNTESIS DE LECTURA COMBINADA 🌈")
        print("="*70)
        print(f"❓ PREGUNTA: {pregunta}")
        print("\n📊 RESULTADOS INDIVIDUALES:")
        
        for i, resultado in enumerate(resultados, 1):
            print(f"\n{i}. {resultado.modalidad}: {resultado.resultado_principal}")
        
        # Generar síntesis combinada
        print(f"\n🧠 SÍNTESIS INTEGRATIVA:")
        
        oraculo = resultados[0]  # Oráculo Sí/No
        runas = resultados[1]    # Runas
        iching = resultados[2]   # I Ching
        
        sintesis = f"""
La consulta combinada revela múltiples perspectivas sobre tu pregunta:

🔮 RESPUESTA DIRECTA (Oráculo): {oraculo.resultado_principal}
   {oraculo.interpretacion.split('.')[0]}.

🔥 CONTEXTO ANCESTRAL (Runas): {runas.resultado_principal}
   Las runas sugieren que la situación está influenciada por fuerzas ancestrales y necesita {self._extraer_consejo_runas(runas)}.

🏛️ SABIDURÍA PROFUNDA (I Ching): {iching.resultado_principal}
   El I Ching aconseja {self._extraer_consejo_iching(iching)}.

🎯 RECOMENDACIÓN FINAL:
   Todos los sistemas apuntan hacia la necesidad de {self._generar_consejo_final(oraculo, runas, iching)}. 
   La energía general es {self._evaluar_energia_general(resultados)} para tu pregunta.
"""
        
        print(sintesis)
        print("="*70)
        
        # Opción de guardar síntesis
        guardar = input("\n¿Deseas guardar esta lectura combinada? (s/n): ").lower()
        if guardar == 's':
            resultado_combinado = ResultadoEsoterico(
                modalidad="Lectura Combinada",
                titulo=f"Síntesis Multi-Sistema: {pregunta[:50]}...",
                resultado_principal=f"Oráculo: {oraculo.resultado_principal} | Runas: {runas.resultado_principal}",
                interpretacion=sintesis,
                detalles_adicionales={
                    "pregunta": pregunta,
                    "resultados_individuales": [r.__dict__ for r in resultados]
                },
                fecha=datetime.now(),
                id_unico=self._generar_id_unico()
            )
            self._guardar_resultado(resultado_combinado)
    
    def _extraer_consejo_runas(self, resultado_runas: ResultadoEsoterico) -> str:
        """Extrae consejo principal de las runas"""
        elementos = resultado_runas.detalles_adicionales.get("elementos_presentes", [])
        if "Fuego" in elementos:
            return "acción y determinación"
        elif "Agua" in elementos:
            return "paciencia y reflexión emocional"
        elif "Aire" in elementos:
            return "comunicación clara y decisiones mentales"
        else:
            return "estabilidad y construcción sólida"
    
    def _extraer_consejo_iching(self, resultado_iching: ResultadoEsoterico) -> str:
        """Extrae consejo principal del I Ching"""
        numero = resultado_iching.detalles_adicionales.get("numero_hexagrama", 1)
        if numero in [1, 11, 42]:
            return "tomar acción con confianza"
        elif numero in [12, 23]:
            return "paciencia y espera estratégica"
        else:
            return "mantener el equilibrio y la sabiduría"
    
    def _generar_consejo_final(self, oraculo: ResultadoEsoterico, 
                              runas: ResultadoEsoterico, iching: ResultadoEsoterico) -> str:
        """Genera consejo final integrado"""
        respuesta_oraculo = oraculo.resultado_principal.lower()
        
        if "sí" in respuesta_oraculo:
            return "avanzar con confianza pero manteniéndote atento a las señales"
        elif "no" in respuesta_oraculo:
            return "reconsiderar tu enfoque y buscar alternativas más alineadas"
        else:
            return "reflexión profunda antes de tomar cualquier acción definitiva"
    
    def _evaluar_energia_general(self, resultados: List[ResultadoEsoterico]) -> str:
        """Evalúa la energía general de todos los resultados"""
        # Análisis simple basado en patrones
        textos = [r.interpretacion.lower() for r in resultados]
        
        palabras_positivas = ["favorable", "positivo", "sí", "éxito", "alegría", "armonía"]
        palabras_negativas = ["obstáculo", "negativo", "no", "dificultad", "bloqueo", "crisis"]
        
        puntos_positivos = sum(sum(palabra in texto for palabra in palabras_positivas) for texto in textos)
        puntos_negativos = sum(sum(palabra in texto for palabra in palabras_negativas) for texto in textos)
        
        if puntos_positivos > puntos_negativos:
            return "favorable y propicia"
        elif puntos_negativos > puntos_positivos:
            return "desafiante pero educativa"
        else:
            return "equilibrada y neutral"
    
    def _guardar_resultado(self, resultado: ResultadoEsoterico):
        """Guarda un resultado en archivo JSON"""
        try:
            archivo = "lecturas_esotéricas.json"
            
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    lecturas = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                lecturas = []
            
            # Convertir resultado a diccionario JSON-serializable
            resultado_dict = {
                "modalidad": resultado.modalidad,
                "titulo": resultado.titulo,
                "resultado_principal": resultado.resultado_principal,
                "interpretacion": resultado.interpretacion,
                "detalles_adicionales": resultado.detalles_adicionales,
                "fecha": resultado.fecha.isoformat(),
                "id_unico": resultado.id_unico
            }
            
            lecturas.append(resultado_dict)
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(lecturas, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"✅ Lectura guardada en {archivo}")
            print(f"🔖 ID: {resultado.id_unico}")
            
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
    
    def _generar_id_unico(self) -> str:
        """Genera un ID único para la lectura"""
        timestamp = str(time.time())
        random_data = str(secrets.randbits(64))
        return hashlib.md5((timestamp + random_data).encode()).hexdigest()[:12]


def main():
    """Función principal"""
    try:
        sistema = SistemaEsotericoExpandido()
        sistema.ejecutar_sistema()
    except KeyboardInterrupt:
        print("\n\n✨ Sesión interrumpida. ¡Que la sabiduría te acompañe! ✨")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()