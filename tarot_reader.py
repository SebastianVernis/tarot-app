#!/usr/bin/env python3
"""
Sistema de Lectura de Tarot Interactivo
Autor: Assistant
Descripción: Simula una lectura de tarot con múltiples tiradas y significados

SECURITY: Uses cryptographically secure randomness (CSPRNG) for all card
shuffling and selection operations. No predictable seeds are used.
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from tarot_secure_random import TarotSecureShuffler


class TipoTirada(Enum):
    """Tipos de tiradas disponibles"""
    TRES_CARTAS = "tres_cartas"
    CRUZ_CELTA = "cruz_celta"
    HERRADURA = "herradura"
    UNA_CARTA = "una_carta"
    RELACION = "relacion"
    AMOR = "amor"
    ANUAL = "anual"
    DECISION = "decision"
    CHAKRAS = "chakras"


@dataclass
class Carta:
    """Representa una carta del tarot"""
    nombre: str
    numero: int
    palo: Optional[str]
    significado_derecho: str
    significado_invertido: str
    palabras_clave: List[str]
    elemento: Optional[str]
    
    def obtener_significado(self, invertida: bool = False) -> str:
        """Retorna el significado según la orientación de la carta"""
        return self.significado_invertido if invertida else self.significado_derecho


class MazoTarot:
    """Mazo completo de 78 cartas del Tarot con aleatoriedad criptográfica"""
    
    def __init__(self):
        self.cartas: List[Carta] = []
        self._crear_arcanos_mayores()
        self._crear_arcanos_menores()
        # Initialize secure shuffler for cryptographic randomness
        self.secure_shuffler = TarotSecureShuffler()
        
    def _crear_arcanos_mayores(self):
        """Crea las 22 cartas de los Arcanos Mayores"""
        arcanos_mayores = [
            Carta(
                nombre="El Loco",
                numero=0,
                palo=None,
                significado_derecho="Nuevos comienzos, espontaneidad, inocencia, espíritu libre",
                significado_invertido="Imprudencia, riesgo innecesario, caos, falta de dirección",
                palabras_clave=["inicio", "libertad", "aventura", "potencial"],
                elemento="Aire"
            ),
            Carta(
                nombre="El Mago",
                numero=1,
                palo=None,
                significado_derecho="Manifestación, poder personal, acción, habilidad",
                significado_invertido="Manipulación, engaño, talentos desperdiciados",
                palabras_clave=["poder", "habilidad", "concentración", "recursos"],
                elemento="Mercurio"
            ),
            Carta(
                nombre="La Sacerdotisa",
                numero=2,
                palo=None,
                significado_derecho="Intuición, misterio, conocimiento oculto, subconsciente",
                significado_invertido="Secretos revelados, desconexión de la intuición",
                palabras_clave=["intuición", "misterio", "sabiduría", "receptividad"],
                elemento="Luna"
            ),
            Carta(
                nombre="La Emperatriz",
                numero=3,
                palo=None,
                significado_derecho="Fertilidad, feminidad, belleza, abundancia, naturaleza",
                significado_invertido="Bloqueo creativo, dependencia, esterilidad",
                palabras_clave=["creatividad", "abundancia", "nutrición", "madre"],
                elemento="Venus"
            ),
            Carta(
                nombre="El Emperador",
                numero=4,
                palo=None,
                significado_derecho="Autoridad, estructura, control, figura paterna",
                significado_invertido="Tiranía, rigidez, frialdad, abuso de poder",
                palabras_clave=["autoridad", "estabilidad", "liderazgo", "padre"],
                elemento="Aries"
            ),
            Carta(
                nombre="El Hierofante",
                numero=5,
                palo=None,
                significado_derecho="Tradición, conformidad, moralidad, espiritualidad",
                significado_invertido="Rebelión, subversión, nuevos métodos, libertad",
                palabras_clave=["tradición", "enseñanza", "creencias", "conformidad"],
                elemento="Tauro"
            ),
            Carta(
                nombre="Los Enamorados",
                numero=6,
                palo=None,
                significado_derecho="Amor, armonía, relaciones, valores, elección",
                significado_invertido="Desarmonía, desequilibrio, desalineación de valores",
                palabras_clave=["amor", "elección", "unión", "valores"],
                elemento="Géminis"
            ),
            Carta(
                nombre="El Carro",
                numero=7,
                palo=None,
                significado_derecho="Control, fuerza de voluntad, éxito, victoria",
                significado_invertido="Falta de control, falta de dirección, agresión",
                palabras_clave=["victoria", "control", "determinación", "viaje"],
                elemento="Cáncer"
            ),
            Carta(
                nombre="La Justicia",
                numero=8,
                palo=None,
                significado_derecho="Justicia, equidad, verdad, causa y efecto, ley",
                significado_invertido="Injusticia, deshonestidad, falta de responsabilidad",
                palabras_clave=["equilibrio", "karma", "honestidad", "ley"],
                elemento="Libra"
            ),
            Carta(
                nombre="El Ermitaño",
                numero=9,
                palo=None,
                significado_derecho="Introspección, búsqueda interior, guía, soledad",
                significado_invertido="Aislamiento, soledad, rechazo de ayuda",
                palabras_clave=["sabiduría", "introspección", "soledad", "guía"],
                elemento="Virgo"
            ),
            Carta(
                nombre="La Rueda de la Fortuna",
                numero=10,
                palo=None,
                significado_derecho="Buena suerte, karma, ciclos, destino, punto de inflexión",
                significado_invertido="Mala suerte, falta de control, revés del destino",
                palabras_clave=["cambio", "ciclos", "destino", "suerte"],
                elemento="Júpiter"
            ),
            Carta(
                nombre="La Fuerza",
                numero=11,
                palo=None,
                significado_derecho="Fuerza interior, coraje, paciencia, control",
                significado_invertido="Debilidad, inseguridad, falta de confianza",
                palabras_clave=["coraje", "paciencia", "control", "compasión"],
                elemento="Leo"
            ),
            Carta(
                nombre="El Colgado",
                numero=12,
                palo=None,
                significado_derecho="Suspensión, restricción, sacrificio, nueva perspectiva",
                significado_invertido="Estancamiento, resistencia al cambio, indecisión",
                palabras_clave=["sacrificio", "paciencia", "perspectiva", "suspensión"],
                elemento="Agua"
            ),
            Carta(
                nombre="La Muerte",
                numero=13,
                palo=None,
                significado_derecho="Fin, transformación, transición, liberación",
                significado_invertido="Resistencia al cambio, estancamiento personal",
                palabras_clave=["transformación", "final", "renovación", "transición"],
                elemento="Escorpio"
            ),
            Carta(
                nombre="La Templanza",
                numero=14,
                palo=None,
                significado_derecho="Balance, moderación, paciencia, propósito",
                significado_invertido="Desequilibrio, exceso, falta de armonía",
                palabras_clave=["equilibrio", "moderación", "paciencia", "alquimia"],
                elemento="Sagitario"
            ),
            Carta(
                nombre="El Diablo",
                numero=15,
                palo=None,
                significado_derecho="Ataduras, adicción, sexualidad, materialismo",
                significado_invertido="Liberación, ruptura de cadenas, poder recuperado",
                palabras_clave=["tentación", "atadura", "materialismo", "sombra"],
                elemento="Capricornio"
            ),
            Carta(
                nombre="La Torre",
                numero=16,
                palo=None,
                significado_derecho="Destrucción súbita, revelación, cambio drástico",
                significado_invertido="Desastre evitado, miedo al cambio, retraso inevitable",
                palabras_clave=["caos", "revelación", "destrucción", "liberación"],
                elemento="Marte"
            ),
            Carta(
                nombre="La Estrella",
                numero=17,
                palo=None,
                significado_derecho="Esperanza, fe, propósito, renovación, espiritualidad",
                significado_invertido="Falta de fe, desesperación, desconexión",
                palabras_clave=["esperanza", "inspiración", "serenidad", "renovación"],
                elemento="Acuario"
            ),
            Carta(
                nombre="La Luna",
                numero=18,
                palo=None,
                significado_derecho="Ilusión, miedo, ansiedad, subconsciente, intuición",
                significado_invertido="Liberación del miedo, verdad revelada, claridad",
                palabras_clave=["ilusión", "intuición", "sueños", "subconsciente"],
                elemento="Piscis"
            ),
            Carta(
                nombre="El Sol",
                numero=19,
                palo=None,
                significado_derecho="Alegría, éxito, celebración, positividad",
                significado_invertido="Tristeza temporal, nubes pasajeras, ego",
                palabras_clave=["alegría", "éxito", "vitalidad", "iluminación"],
                elemento="Sol"
            ),
            Carta(
                nombre="El Juicio",
                numero=20,
                palo=None,
                significado_derecho="Juicio, renacimiento, llamada interior, absolución",
                significado_invertido="Autocrítica, duda, incapacidad de perdonar",
                palabras_clave=["renacimiento", "evaluación", "despertar", "llamada"],
                elemento="Fuego"
            ),
            Carta(
                nombre="El Mundo",
                numero=21,
                palo=None,
                significado_derecho="Completitud, logro, viaje completado, plenitud",
                significado_invertido="Falta de cierre, búsqueda externa, incompletitud",
                palabras_clave=["completitud", "logro", "integración", "cumplimiento"],
                elemento="Saturno"
            )
        ]
        
        self.cartas.extend(arcanos_mayores)
    
    def _crear_arcanos_menores(self):
        """Crea las 56 cartas de los Arcanos Menores"""
        palos = {
            "Bastos": {
                "elemento": "Fuego",
                "area": "creatividad, acción, energía, inspiración"
            },
            "Copas": {
                "elemento": "Agua",
                "area": "emociones, relaciones, intuición, espiritualidad"
            },
            "Espadas": {
                "elemento": "Aire",
                "area": "pensamiento, comunicación, conflicto, decisiones"
            },
            "Oros": {
                "elemento": "Tierra",
                "area": "material, trabajo, dinero, salud física"
            }
        }
        
        # Cartas numeradas (As al 10)
        for palo, info in palos.items():
            # As
            self.cartas.append(Carta(
                nombre=f"As de {palo}",
                numero=1,
                palo=palo,
                significado_derecho=f"Nuevo comienzo en {info['area']}",
                significado_invertido=f"Oportunidad perdida en {info['area']}",
                palabras_clave=["inicio", "potencial", "semilla"],
                elemento=info["elemento"]
            ))
            
            # Cartas 2-10 (versión simplificada)
            for num in range(2, 11):
                self.cartas.append(Carta(
                    nombre=f"{num} de {palo}",
                    numero=num,
                    palo=palo,
                    significado_derecho=f"Progreso y desarrollo en {info['area']}",
                    significado_invertido=f"Desafíos y obstáculos en {info['area']}",
                    palabras_clave=["progreso", "desarrollo", palo.lower()],
                    elemento=info["elemento"]
                ))
        
        # Cartas de la corte
        figuras = [
            ("Sota", "Mensajero, estudiante, nuevas ideas"),
            ("Caballo", "Acción, movimiento, impulso"),
            ("Reina", "Madurez emocional, nutrición, receptividad"),
            ("Rey", "Dominio, control, liderazgo")
        ]
        
        for palo, info in palos.items():
            for figura, descripcion in figuras:
                self.cartas.append(Carta(
                    nombre=f"{figura} de {palo}",
                    numero=11 + figuras.index((figura, descripcion)),
                    palo=palo,
                    significado_derecho=f"{descripcion} en {info['area']}",
                    significado_invertido=f"Aspectos negativos de {descripcion.lower()}",
                    palabras_clave=[figura.lower(), palo.lower()],
                    elemento=info["elemento"]
                ))
    
    def barajar(self):
        """
        Baraja el mazo usando Fisher-Yates con CSPRNG.
        
        Security: Uses cryptographically secure random number generator
        (secrets module) to ensure unpredictable, uniform shuffling.
        No seeds or predictable parameters are used.
        """
        self.cartas = self.secure_shuffler.shuffle_deck(self.cartas)
    
    def sacar_carta(self) -> Tuple[Carta, bool]:
        """
        Saca una carta del mazo y determina si está invertida.
        
        Security: Uses cryptographically secure boolean generation
        for card orientation (50/50 probability, unpredictable).
        """
        if not self.cartas:
            raise ValueError("No hay más cartas en el mazo")
        
        carta = self.cartas.pop()
        invertida = self.secure_shuffler.determine_orientation()
        return carta, invertida


class LectorTarot:
    """Clase principal para realizar lecturas de tarot"""
    
    def __init__(self):
        self.mazo = MazoTarot()
        self.tiradas = self._definir_tiradas()
        
    def _definir_tiradas(self) -> Dict[TipoTirada, Dict]:
        """Define las diferentes tiradas disponibles"""
        return {
            TipoTirada.UNA_CARTA: {
                "nombre": "Una Carta del Día",
                "descripcion": "Una sola carta para guía o reflexión diaria",
                "posiciones": ["Mensaje del día"],
                "num_cartas": 1
            },
            TipoTirada.TRES_CARTAS: {
                "nombre": "Pasado, Presente y Futuro",
                "descripcion": "Visión general de una situación en el tiempo",
                "posiciones": ["Pasado", "Presente", "Futuro"],
                "num_cartas": 3
            },
            TipoTirada.CRUZ_CELTA: {
                "nombre": "Cruz Celta",
                "descripcion": "Lectura completa y detallada de una situación",
                "posiciones": [
                    "Situación actual",
                    "Desafío o Cruz",
                    "Pasado distante",
                    "Pasado reciente",
                    "Futuro posible",
                    "Futuro inmediato",
                    "Tu enfoque",
                    "Influencias externas",
                    "Esperanzas y miedos",
                    "Resultado final"
                ],
                "num_cartas": 10
            },
            TipoTirada.HERRADURA: {
                "nombre": "Herradura",
                "descripcion": "Análisis de una situación con consejo",
                "posiciones": [
                    "Pasado",
                    "Presente", 
                    "Influencias ocultas",
                    "Obstáculos",
                    "Ambiente",
                    "Mejor curso de acción",
                    "Resultado probable"
                ],
                "num_cartas": 7
            },
            TipoTirada.RELACION: {
                "nombre": "Lectura de Relación",
                "descripcion": "Análisis de una relación entre dos personas",
                "posiciones": [
                    "Cómo te ves a ti mismo",
                    "Cómo ves a la otra persona",
                    "Cómo te ve la otra persona",
                    "Lo que necesitas de la relación",
                    "Lo que la otra persona necesita",
                    "Dónde va la relación"
                ],
                "num_cartas": 6
            },
            TipoTirada.AMOR: {
                "nombre": "Lectura de Amor",
                "descripcion": "Análisis profundo de tu vida amorosa y relaciones románticas",
                "posiciones": [
                    "Tu situación amorosa actual",
                    "Tus sentimientos verdaderos",
                    "Los sentimientos de la otra persona",
                    "Obstáculos en el amor",
                    "Fortalezas de la relación",
                    "Consejo para el amor",
                    "Futuro de la relación"
                ],
                "num_cartas": 7
            },
            TipoTirada.ANUAL: {
                "nombre": "Lectura Anual",
                "descripcion": "Visión de los próximos 12 meses, una carta por mes",
                "posiciones": [
                    "Enero - Nuevos comienzos",
                    "Febrero - Relaciones",
                    "Marzo - Acción y energía",
                    "Abril - Estabilidad",
                    "Mayo - Cambios",
                    "Junio - Amor y armonía",
                    "Julio - Reflexión",
                    "Agosto - Fuerza interior",
                    "Septiembre - Sabiduría",
                    "Octubre - Transformación",
                    "Noviembre - Esperanza",
                    "Diciembre - Completitud"
                ],
                "num_cartas": 12
            },
            TipoTirada.DECISION: {
                "nombre": "Lectura de Decisión",
                "descripcion": "Ayuda para tomar una decisión importante entre dos opciones",
                "posiciones": [
                    "La situación actual",
                    "Opción A - Pros",
                    "Opción A - Contras",
                    "Opción B - Pros",
                    "Opción B - Contras"
                ],
                "num_cartas": 5
            },
            TipoTirada.CHAKRAS: {
                "nombre": "Lectura de Chakras",
                "descripcion": "Análisis energético de tus siete chakras principales",
                "posiciones": [
                    "Chakra Raíz - Seguridad y supervivencia",
                    "Chakra Sacro - Creatividad y sexualidad",
                    "Chakra Plexo Solar - Poder personal",
                    "Chakra Corazón - Amor y compasión",
                    "Chakra Garganta - Comunicación",
                    "Chakra Tercer Ojo - Intuición",
                    "Chakra Corona - Espiritualidad"
                ],
                "num_cartas": 7
            }
        }
    
    def realizar_lectura(self, tipo_tirada: TipoTirada, pregunta: str = "") -> Dict:
        """Realiza una lectura de tarot completa"""
        self.mazo = MazoTarot()  # Reiniciar mazo
        self.mazo.barajar()
        
        tirada_info = self.tiradas[tipo_tirada]
        lectura = {
            "fecha": datetime.now().isoformat(),
            "tipo_tirada": tirada_info["nombre"],
            "pregunta": pregunta,
            "cartas": []
        }
        
        print(f"\n{'='*60}")
        print(f"🔮 {tirada_info['nombre']} 🔮")
        print(f"{'='*60}")
        print(f"\n{tirada_info['descripcion']}")
        
        if pregunta:
            print(f"\nPregunta: {pregunta}")
        
        print(f"\n{'─'*60}\n")
        
        for i, posicion in enumerate(tirada_info["posiciones"]):
            carta, invertida = self.mazo.sacar_carta()
            
            estado = "Invertida" if invertida else "Derecha"
            print(f"Posición {i+1} - {posicion}:")
            print(f"  📌 {carta.nombre} ({estado})")
            print(f"  ✨ {carta.obtener_significado(invertida)}")
            print(f"  🔑 Palabras clave: {', '.join(carta.palabras_clave)}")
            print()
            
            lectura["cartas"].append({
                "posicion": posicion,
                "carta": carta.nombre,
                "invertida": invertida,
                "significado": carta.obtener_significado(invertida),
                "palabras_clave": carta.palabras_clave
            })
        
        print(f"{'─'*60}\n")
        
        # Generar interpretación general
        interpretacion = self._generar_interpretacion(lectura, tipo_tirada)
        lectura["interpretacion"] = interpretacion
        
        print("📖 Interpretación General:")
        print(f"{interpretacion}\n")
        
        return lectura
    
    def _generar_interpretacion(self, lectura: Dict, tipo_tirada: TipoTirada) -> str:
        """Genera una interpretación general basada en las cartas"""
        cartas = lectura["cartas"]
        
        if tipo_tirada == TipoTirada.UNA_CARTA:
            return f"La carta {cartas[0]['carta']} te invita a reflexionar sobre {cartas[0]['significado'].lower()}. Es un momento para considerar {', '.join(cartas[0]['palabras_clave'][:2])}."
        
        elif tipo_tirada == TipoTirada.TRES_CARTAS:
            return f"Tu pasado muestra {cartas[0]['carta']}, indicando {cartas[0]['palabras_clave'][0]}. " \
                   f"En el presente, {cartas[1]['carta']} sugiere enfocarte en {cartas[1]['palabras_clave'][0]}. " \
                   f"El futuro presenta {cartas[2]['carta']}, prometiendo {cartas[2]['palabras_clave'][0]}."
        
        else:
            # Interpretación genérica para tiradas complejas
            cartas_mayores = [c for c in cartas if "de" not in c["carta"]]
            if len(cartas_mayores) >= 3:
                return "Esta lectura muestra una fuerte presencia de Arcanos Mayores, indicando que fuerzas importantes están en juego. Es un momento de transformación significativa."
            else:
                elementos_dominantes = self._contar_elementos(cartas)
                elemento_principal = max(elementos_dominantes, key=elementos_dominantes.get)
                return f"La lectura muestra una fuerte influencia del elemento {elemento_principal}, sugiriendo un enfoque en sus cualidades asociadas."
    
    def _contar_elementos(self, cartas: List[Dict]) -> Dict[str, int]:
        """Cuenta la frecuencia de elementos en las cartas"""
        elementos = {"Fuego": 0, "Agua": 0, "Aire": 0, "Tierra": 0}
        
        for carta_info in cartas:
            # Aquí simplificamos, en una implementación real buscaríamos el elemento
            if "Bastos" in carta_info["carta"]:
                elementos["Fuego"] += 1
            elif "Copas" in carta_info["carta"]:
                elementos["Agua"] += 1
            elif "Espadas" in carta_info["carta"]:
                elementos["Aire"] += 1
            elif "Oros" in carta_info["carta"]:
                elementos["Tierra"] += 1
        
        return elementos
    
    def guardar_lectura(self, lectura: Dict, archivo: str = "lecturas_tarot.json"):
        """Guarda la lectura en un archivo JSON"""
        try:
            with open(archivo, 'r') as f:
                lecturas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lecturas = []
        
        lecturas.append(lectura)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(lecturas, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Lectura guardada en {archivo}")


def menu_principal():
    """Muestra el menú principal e interactúa con el usuario"""
    lector = LectorTarot()
    
    print("\n🌟 Bienvenido al Lector de Tarot Interactivo 🌟")
    print("="*60)
    
    while True:
        print("\n¿Qué tipo de lectura deseas realizar?")
        print("1. Una Carta del Día")
        print("2. Pasado, Presente y Futuro (3 cartas)")
        print("3. Cruz Celta (10 cartas)")
        print("4. Herradura (7 cartas)")
        print("5. Lectura de Relación (6 cartas)")
        print("6. Lectura de Amor (7 cartas)")
        print("7. Lectura Anual (12 cartas)")
        print("8. Lectura de Decisión (5 cartas)")
        print("9. Lectura de Chakras (7 cartas)")
        print("10. Salir")
        
        opcion = input("\nElige una opción (1-10): ")
        
        if opcion == "10":
            print("\n✨ Que las cartas iluminen tu camino. ¡Hasta pronto! ✨")
            break
        
        tipo_map = {
            "1": TipoTirada.UNA_CARTA,
            "2": TipoTirada.TRES_CARTAS,
            "3": TipoTirada.CRUZ_CELTA,
            "4": TipoTirada.HERRADURA,
            "5": TipoTirada.RELACION,
            "6": TipoTirada.AMOR,
            "7": TipoTirada.ANUAL,
            "8": TipoTirada.DECISION,
            "9": TipoTirada.CHAKRAS
        }
        
        if opcion in tipo_map:
            pregunta = input("\n¿Cuál es tu pregunta? (presiona Enter para omitir): ").strip()
            
            lectura = lector.realizar_lectura(tipo_map[opcion], pregunta)
            
            guardar = input("\n¿Deseas guardar esta lectura? (s/n): ").lower()
            if guardar == 's':
                lector.guardar_lectura(lectura)
        else:
            print("\n❌ Opción no válida. Por favor, elige entre 1 y 10.")
        
        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    menu_principal()