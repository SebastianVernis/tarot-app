#!/usr/bin/env python3
"""
Sistema de Lectura de Tarot con Aleatorización Mejorada
Autor: Assistant
Descripción: Sistema de tarot con múltiples capas de aleatorización para simular el azar real
"""

import random
import json
import time
import hashlib
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import secrets  # Para aleatorización criptográficamente segura


class TipoTirada(Enum):
    """Tipos de tiradas disponibles"""
    TRES_CARTAS = "tres_cartas"
    CRUZ_CELTA = "cruz_celta"
    HERRADURA = "herradura"
    UNA_CARTA = "una_carta"
    RELACION = "relacion"


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


class GeneradorAleatorio:
    """Clase para manejar múltiples fuentes de aleatoriedad"""
    
    def __init__(self):
        # Inicializar con múltiples fuentes de entropía
        self.inicializar_semillas()
    
    def inicializar_semillas(self):
        """Inicializa las semillas con múltiples fuentes de entropía"""
        # Combinar múltiples fuentes de entropía
        entropia_fuentes = [
            str(time.time()),  # Tiempo actual con microsegundos
            str(os.getpid()),  # ID del proceso
            str(secrets.randbits(256)),  # Bits aleatorios criptográficos
            str(time.perf_counter()),  # Contador de rendimiento de alta precisión
        ]
        
        # Si el usuario hace algún input, usar eso también
        try:
            # Capturar cualquier movimiento del mouse o teclas (simulado con tiempo de respuesta)
            start_time = time.perf_counter()
            input("🎲 Presiona Enter cuando estés listo para barajar las cartas... ")
            end_time = time.perf_counter()
            tiempo_respuesta = str(end_time - start_time)
            entropia_fuentes.append(tiempo_respuesta)
        except:
            pass
        
        # Combinar toda la entropía
        entropia_combinada = ''.join(entropia_fuentes)
        hash_entropia = hashlib.sha256(entropia_combinada.encode()).hexdigest()
        
        # Usar el hash como semilla
        semilla = int(hash_entropia[:16], 16)  # Usar primeros 16 caracteres hex
        random.seed(semilla)
        
        # También inicializar el generador del sistema
        random.SystemRandom()
    
    def mezclar_lista(self, lista: List) -> List:
        """Mezcla una lista usando múltiples algoritmos"""
        lista_copia = lista.copy()
        
        # Primera mezcla: Fisher-Yates con random estándar
        random.shuffle(lista_copia)
        
        # Segunda mezcla: Usar secrets para algunas transposiciones
        num_transposiciones = secrets.randbelow(len(lista_copia) // 2) + 5
        for _ in range(num_transposiciones):
            i = secrets.randbelow(len(lista_copia))
            j = secrets.randbelow(len(lista_copia))
            lista_copia[i], lista_copia[j] = lista_copia[j], lista_copia[i]
        
        # Tercera mezcla: Corte aleatorio (como cortar un mazo real)
        punto_corte = secrets.randbelow(len(lista_copia) - 10) + 5
        lista_copia = lista_copia[punto_corte:] + lista_copia[:punto_corte]
        
        # Mezcla final
        random.shuffle(lista_copia)
        
        return lista_copia
    
    def obtener_bool_aleatorio(self) -> bool:
        """Obtiene un booleano aleatorio con alta entropía"""
        # Usar múltiples fuentes para decidir
        fuentes = [
            random.random() > 0.5,
            secrets.randbits(1) == 1,
            int(time.time() * 1000000) % 2 == 0,
            random.SystemRandom().random() > 0.5
        ]
        
        # Votar por mayoría
        return sum(fuentes) >= 2
    
    def obtener_indice_aleatorio(self, maximo: int) -> int:
        """Obtiene un índice aleatorio con alta calidad"""
        if maximo <= 0:
            return 0
        
        # Combinar múltiples métodos
        metodos = [
            random.randint(0, maximo - 1),
            secrets.randbelow(maximo),
            int(random.SystemRandom().random() * maximo)
        ]
        
        # Elegir uno de los métodos aleatoriamente
        return secrets.choice(metodos)


class MazoTarot:
    """Mazo completo de 78 cartas del Tarot con aleatorización mejorada"""
    
    def __init__(self):
        self.cartas: List[Carta] = []
        self.cartas_sacadas: List[Carta] = []  # Historial de cartas sacadas
        self.generador_aleatorio = GeneradorAleatorio()
        self._crear_arcanos_mayores()
        self._crear_arcanos_menores()
        self.barajar_inicial()
        
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
        
        # Significados específicos para cada número
        significados_numeros = {
            1: ("nuevo comienzo, potencial puro", "retraso, oportunidad perdida"),
            2: ("balance, cooperación, dualidad", "desequilibrio, tensión, indecisión"),
            3: ("creatividad, crecimiento, expansión", "falta de progreso, conflictos menores"),
            4: ("estabilidad, fundación, descanso", "estancamiento, falta de motivación"),
            5: ("conflicto, cambio, desafío", "evitar conflicto, tensión interna"),
            6: ("armonía, generosidad, éxito", "desequilibrio, egoísmo, fracaso"),
            7: ("reflexión, evaluación, perseverancia", "duda, falta de confianza"),
            8: ("movimiento, progreso rápido, acción", "retrasos, frustración, prisa"),
            9: ("cerca de la completitud, perseverancia", "agotamiento, lucha final"),
            10: ("completitud, final de ciclo, logro", "fracaso, carga pesada, colapso")
        }
        
        for palo, info in palos.items():
            for num in range(1, 11):
                nombre = f"As de {palo}" if num == 1 else f"{num} de {palo}"
                sig_derecho, sig_invertido = significados_numeros[num]
                
                self.cartas.append(Carta(
                    nombre=nombre,
                    numero=num,
                    palo=palo,
                    significado_derecho=f"{sig_derecho} en {info['area']}",
                    significado_invertido=f"{sig_invertido} en {info['area']}",
                    palabras_clave=[f"numero_{num}", palo.lower(), info["elemento"].lower()],
                    elemento=info["elemento"]
                ))
        
        # Cartas de la corte
        figuras = [
            ("Sota", "Mensajero, estudiante, nuevas ideas", "Inmadurez, malas noticias"),
            ("Caballo", "Acción, movimiento, impulso", "Impulsividad, dirección equivocada"),
            ("Reina", "Madurez emocional, nutrición", "Frialdad emocional, manipulación"),
            ("Rey", "Dominio, control, liderazgo", "Tiranía, abuso de poder")
        ]
        
        for palo, info in palos.items():
            for i, (figura, desc_derecho, desc_invertido) in enumerate(figuras):
                self.cartas.append(Carta(
                    nombre=f"{figura} de {palo}",
                    numero=11 + i,
                    palo=palo,
                    significado_derecho=f"{desc_derecho} en {info['area']}",
                    significado_invertido=f"{desc_invertido} en {info['area']}",
                    palabras_clave=[figura.lower(), palo.lower(), "corte"],
                    elemento=info["elemento"]
                ))
    
    def barajar_inicial(self):
        """Baraja inicial del mazo con máxima aleatoriedad"""
        print("\n🌀 Mezclando las energías del universo...")
        time.sleep(0.5)  # Pausa dramática
        
        # Aplicar múltiples barajadas
        for i in range(7):  # 7 es un número místico
            self.cartas = self.generador_aleatorio.mezclar_lista(self.cartas)
            print(f"   ✨ Barajada {i+1} de 7 completada...")
            time.sleep(0.2)
        
        print("   🎴 El mazo está listo.\n")
    
    def cortar_mazo(self):
        """Simula el corte del mazo por el consultante"""
        print("\n✂️ Cortando el mazo...")
        
        # El usuario "corta" el mazo con su energía
        input("   Piensa en tu pregunta y presiona Enter para cortar el mazo... ")
        
        # Usar el tiempo de respuesta como factor adicional de aleatoriedad
        punto_corte = self.generador_aleatorio.obtener_indice_aleatorio(len(self.cartas) - 20) + 10
        self.cartas = self.cartas[punto_corte:] + self.cartas[:punto_corte]
        
        print("   📚 El mazo ha sido cortado.\n")
    
    def sacar_carta(self) -> Tuple[Carta, bool]:
        """Saca una carta del mazo con máxima aleatoriedad"""
        if not self.cartas:
            raise ValueError("No hay más cartas en el mazo")
        
        # Mezclar ligeramente antes de sacar (como cuando se extienden las cartas)
        if len(self.cartas) > 10:
            # Pequeña mezcla de las primeras cartas
            primeras = self.cartas[:10]
            random.shuffle(primeras)
            self.cartas[:10] = primeras
        
        # Elegir posición aleatoria, no necesariamente la primera
        indice = self.generador_aleatorio.obtener_indice_aleatorio(min(5, len(self.cartas)))
        carta = self.cartas.pop(indice)
        
        # Determinar si está invertida con alta aleatoriedad
        invertida = self.generador_aleatorio.obtener_bool_aleatorio()
        
        # Agregar al historial
        self.cartas_sacadas.append(carta)
        
        return carta, invertida


class LectorTarot:
    """Clase principal para realizar lecturas de tarot con aleatorización mejorada"""
    
    def __init__(self):
        self.mazo = MazoTarot()
        self.tiradas = self._definir_tiradas()
        self.historial_lecturas = []
        
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
            }
        }
    
    def realizar_lectura(self, tipo_tirada: TipoTirada, pregunta: str = "") -> Dict:
        """Realiza una lectura de tarot completa con máxima aleatoriedad"""
        # Reiniciar mazo para cada lectura
        self.mazo = MazoTarot()
        
        # Permitir al consultante cortar el mazo
        self.mazo.cortar_mazo()
        
        tirada_info = self.tiradas[tipo_tirada]
        lectura = {
            "fecha": datetime.now().isoformat(),
            "timestamp": time.time(),
            "tipo_tirada": tirada_info["nombre"],
            "pregunta": pregunta,
            "cartas": [],
            "semilla_lectura": secrets.token_hex(8)  # ID único de la lectura
        }
        
        print(f"\n{'='*60}")
        print(f"🔮 {tirada_info['nombre']} 🔮")
        print(f"{'='*60}")
        print(f"\n{tirada_info['descripcion']}")
        
        if pregunta:
            print(f"\nPregunta: {pregunta}")
        
        print(f"\n{'─'*60}\n")
        
        # Pausa dramática antes de empezar
        print("🌙 Conectando con las energías cósmicas...")
        time.sleep(1)
        
        for i, posicion in enumerate(tirada_info["posiciones"]):
            # Pequeña pausa entre cartas para aumentar la anticipación
            time.sleep(0.5)
            
            carta, invertida = self.mazo.sacar_carta()
            
            estado = "Invertida 🔄" if invertida else "Derecha ⬆️"
            print(f"Posición {i+1} - {posicion}:")
            print(f"  📌 {carta.nombre} ({estado})")
            print(f"  ✨ {carta.obtener_significado(invertida)}")
            print(f"  🔑 Palabras clave: {', '.join(carta.palabras_clave)}")
            
            if carta.elemento:
                print(f"  🌀 Elemento: {carta.elemento}")
            print()
            
            lectura["cartas"].append({
                "posicion": posicion,
                "carta": carta.nombre,
                "numero": carta.numero,
                "palo": carta.palo,
                "invertida": invertida,
                "significado": carta.obtener_significado(invertida),
                "palabras_clave": carta.palabras_clave,
                "elemento": carta.elemento
            })
        
        print(f"{'─'*60}\n")
        
        # Generar interpretación general
        interpretacion = self._generar_interpretacion(lectura, tipo_tirada)
        lectura["interpretacion"] = interpretacion
        
        print("📖 Interpretación General:")
        print(f"{interpretacion}\n")
        
        # Análisis adicional
        self._analizar_patrones(lectura)
        
        # Agregar al historial
        self.historial_lecturas.append(lectura)
        
        return lectura
    
    def _generar_interpretacion(self, lectura: Dict, tipo_tirada: TipoTirada) -> str:
        """Genera una interpretación general basada en las cartas"""
        cartas = lectura["cartas"]
        
        # Análisis de patrones
        num_invertidas = sum(1 for c in cartas if c["invertida"])
        num_mayores = sum(1 for c in cartas if c["palo"] is None)
        
        # Contar elementos
        elementos = {}
        for carta in cartas:
            if carta["elemento"]:
                elementos[carta["elemento"]] = elementos.get(carta["elemento"], 0) + 1
        
        interpretacion_base = ""
        
        # Interpretaciones específicas por tipo
        if tipo_tirada == TipoTirada.UNA_CARTA:
            c = cartas[0]
            interpretacion_base = f"La carta {c['carta']} "
            if c["invertida"]:
                interpretacion_base += "aparece invertida, sugiriendo que debes prestar atención a los aspectos ocultos o bloqueados de "
            else:
                interpretacion_base += "te invita a embracar "
            interpretacion_base += f"{c['significado'].lower()}. "
            interpretacion_base += f"Las energías de {', '.join(c['palabras_clave'][:2])} están presentes en tu día."
            
        elif tipo_tirada == TipoTirada.TRES_CARTAS:
            interpretacion_base = self._interpretar_tres_cartas(cartas)
            
        else:
            # Interpretación general para tiradas complejas
            interpretacion_base = self._interpretar_tirada_compleja(cartas, elementos, num_mayores, num_invertidas)
        
        # Agregar observaciones sobre patrones
        observaciones = []
        
        if num_invertidas > len(cartas) * 0.6:
            observaciones.append("Hay una fuerte presencia de cartas invertidas, sugiriendo bloqueos o la necesidad de trabajo interno")
        elif num_invertidas == 0:
            observaciones.append("Todas las cartas están derechas, indicando un flujo claro de energía")
        
        if num_mayores >= 3:
            observaciones.append("Los Arcanos Mayores dominan esta lectura, señalando eventos significativos o lecciones kármicas importantes")
        
        if elementos:
            elemento_dominante = max(elementos, key=elementos.get)
            if elementos[elemento_dominante] >= 3:
                observaciones.append(f"El elemento {elemento_dominante} domina, sugiriendo un enfoque en sus cualidades")
        
        if observaciones:
            interpretacion_base += " " + ". ".join(observaciones) + "."
        
        return interpretacion_base
    
    def _interpretar_tres_cartas(self, cartas: List[Dict]) -> str:
        """Interpretación específica para tirada de tres cartas"""
        pasado, presente, futuro = cartas
        
        interp = f"Tu pasado está marcado por {pasado['carta']}, "
        
        if pasado["invertida"]:
            interp += f"donde experimentaste desafíos relacionados con {pasado['palabras_clave'][0]}. "
        else:
            interp += f"donde {pasado['palabras_clave'][0]} jugó un papel importante. "
        
        interp += f"En el presente, {presente['carta']} "
        if presente["invertida"]:
            interp += f"sugiere que estás lidiando con {presente['significado'].lower()}. "
        else:
            interp += f"indica que {presente['significado'].lower()}. "
        
        interp += f"Mirando hacia el futuro, {futuro['carta']} "
        if futuro["invertida"]:
            interp += f"advierte sobre posibles obstáculos en {futuro['palabras_clave'][0]}, pero también ofrece la oportunidad de crecimiento."
        else:
            interp += f"promete {futuro['significado'].lower()}."
        
        return interp
    
    def _interpretar_tirada_compleja(self, cartas: List[Dict], elementos: Dict, 
                                   num_mayores: int, num_invertidas: int) -> str:
        """Interpretación para tiradas complejas"""
        
        # Buscar temas comunes
        temas_comunes = {}
        for carta in cartas:
            for palabra in carta["palabras_clave"]:
                temas_comunes[palabra] = temas_comunes.get(palabra, 0) + 1
        
        # Encontrar el tema más común
        if temas_comunes:
            tema_principal = max(temas_comunes, key=temas_comunes.get)
            if temas_comunes[tema_principal] > 1:
                return f"El tema de '{tema_principal}' aparece repetidamente en tu lectura, sugiriendo su importancia central en tu situación actual. "
        
        # Interpretación basada en balance de elementos
        if elementos:
            return self._interpretar_por_elementos(elementos)
        
        # Interpretación genérica
        return "Esta lectura revela múltiples capas de significado en tu situación actual. "
    
    def _interpretar_por_elementos(self, elementos: Dict[str, int]) -> str:
        """Interpretación basada en elementos dominantes"""
        total = sum(elementos.values())
        interpretaciones = {
            "Fuego": "La energía del Fuego domina, indicando acción, pasión y creatividad",
            "Agua": "El elemento Agua fluye fuertemente, señalando emociones profundas e intuición",
            "Aire": "El Aire prevalece, sugiriendo comunicación, ideas y decisiones mentales",
            "Tierra": "La Tierra ancla tu lectura, indicando asuntos prácticos y materiales"
        }
        
        elemento_dominante = max(elementos, key=elementos.get)
        porcentaje = (elementos[elemento_dominante] / total) * 100
        
        interp = interpretaciones.get(elemento_dominante, "Las energías están en movimiento")
        
        if porcentaje > 50:
            interp += f" de manera muy marcada ({porcentaje:.0f}% de las cartas). "
        else:
            interp += ". "
        
        # Mencionar elementos faltantes
        elementos_posibles = {"Fuego", "Agua", "Aire", "Tierra"}
        faltantes = elementos_posibles - set(elementos.keys())
        
        if faltantes:
            interp += f"La ausencia de {', '.join(faltantes)} sugiere áreas que podrían necesitar atención. "
        
        return interp
    
    def _analizar_patrones(self, lectura: Dict):
        """Analiza patrones adicionales en la lectura"""
        print("\n🔍 Análisis de Patrones:")
        
        cartas = lectura["cartas"]
        
        # Análisis numérico
        numeros = [c["numero"] for c in cartas if c["numero"] is not None]
        if numeros:
            promedio = sum(numeros) / len(numeros)
            print(f"  • Vibración numérica promedio: {promedio:.1f}")
            
            if promedio < 7:
                print("    → Enfoque en inicios y desarrollo")
            elif promedio > 14:
                print("    → Enfoque en completitud y maestría")
            else:
                print("    → Balance entre crecimiento y estabilidad")
        
        # Análisis de palos
        palos = [c["palo"] for c in cartas if c["palo"]]
        if palos:
            palo_counts = {}
            for palo in palos:
                palo_counts[palo] = palo_counts.get(palo, 0) + 1
            
            print(f"  • Distribución de palos: {dict(palo_counts)}")
        
        print()
    
    def guardar_lectura(self, lectura: Dict, archivo: str = "lecturas_tarot.json"):
        """Guarda la lectura en un archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                lecturas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lecturas = []
        
        lecturas.append(lectura)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(lecturas, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Lectura guardada en {archivo}")
        print(f"🔖 ID de lectura: {lectura['semilla_lectura']}")


def menu_principal():
    """Muestra el menú principal e interactúa con el usuario"""
    
    print("\n✨ Bienvenido al Lector de Tarot de Alta Aleatoriedad ✨")
    print("="*60)
    print("Este sistema utiliza múltiples capas de aleatoriedad")
    print("para simular una experiencia de lectura genuina.")
    print("="*60)
    
    lector = LectorTarot()
    
    while True:
        print("\n¿Qué tipo de lectura deseas realizar?")
        print("1. Una Carta del Día")
        print("2. Pasado, Presente y Futuro (3 cartas)")
        print("3. Cruz Celta (10 cartas)")
        print("4. Herradura (7 cartas)")
        print("5. Lectura de Relación (6 cartas)")
        print("6. Salir")
        
        opcion = input("\nElige una opción (1-6): ")
        
        if opcion == "6":
            print("\n✨ Que las estrellas iluminen tu camino. ¡Hasta pronto! ✨")
            break
        
        tipo_map = {
            "1": TipoTirada.UNA_CARTA,
            "2": TipoTirada.TRES_CARTAS,
            "3": TipoTirada.CRUZ_CELTA,
            "4": TipoTirada.HERRADURA,
            "5": TipoTirada.RELACION
        }
        
        if opcion in tipo_map:
            print("\n🌟 Preparando el espacio sagrado...")
            time.sleep(1)
            
            pregunta = input("\n¿Cuál es tu pregunta? (presiona Enter para omitir): ").strip()
            
            if pregunta:
                print("\n🕯️ Tu pregunta ha sido recibida por el universo...")
                time.sleep(1)
            
            lectura = lector.realizar_lectura(tipo_map[opcion], pregunta)
            
            guardar = input("\n¿Deseas guardar esta lectura? (s/n): ").lower()
            if guardar == 's':
                lector.guardar_lectura(lectura)
        else:
            print("\n❌ Opción no válida. Por favor, elige entre 1 y 6.")
        
        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    menu_principal()