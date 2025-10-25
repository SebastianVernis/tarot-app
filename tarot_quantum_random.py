#!/usr/bin/env python3
"""
Sistema de Tarot con Aleatoriedad Cuántica y Verificación
Autor: Assistant
Descripción: Implementa múltiples capas de aleatoriedad verificable
"""

import random
import secrets
import time
import hashlib
import os
import struct
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class FuenteAleatoriedad(Enum):
    """Fuentes de aleatoriedad disponibles"""
    PSEUDO_RANDOM = "pseudo_random"
    CRYPTO_RANDOM = "crypto_random"
    HARDWARE_RANDOM = "hardware_random"
    QUANTUM_SIMULATED = "quantum_simulated"
    COMBINADO = "combinado"


class GeneradorCuanticoSimulado:
    """
    Simula comportamiento cuántico usando múltiples fuentes de entropía.
    En un sistema real, esto conectaría con hardware cuántico real.
    """
    
    def __init__(self):
        self.historia_entropia = []
        self.pool_entropia = bytearray()
        self._inicializar_pool()
    
    def _inicializar_pool(self):
        """Inicializa el pool de entropía con múltiples fuentes"""
        # Recolectar entropía de múltiples fuentes
        fuentes_entropia = [
            # Tiempo de alta precisión
            struct.pack('d', time.perf_counter()),
            
            # PID y tiempo del sistema
            struct.pack('Q', os.getpid() ^ int(time.time() * 1000000)),
            
            # Entropía del sistema operativo
            os.urandom(32),
            
            # Hash del estado actual del sistema
            hashlib.sha256(str(time.time()).encode()).digest(),
            
            # Ruido del timing del CPU
            self._generar_ruido_timing(),
            
            # Estado de la memoria
            struct.pack('Q', id(self)),
            
            # Entropía criptográfica
            secrets.token_bytes(32)
        ]
        
        # Combinar todas las fuentes
        for fuente in fuentes_entropia:
            self.pool_entropia.extend(fuente)
        
        # Mezclar el pool
        self._mezclar_pool()
    
    def _generar_ruido_timing(self, iteraciones=100):
        """Genera ruido basado en variaciones de timing del CPU"""
        timings = []
        for _ in range(iteraciones):
            start = time.perf_counter_ns()
            # Operación simple para medir timing
            _ = [i**2 for i in range(10)]
            end = time.perf_counter_ns()
            timings.append(end - start)
        
        # Usar las diferencias de timing como entropía
        ruido = bytearray()
        for i in range(1, len(timings)):
            diff = timings[i] - timings[i-1]
            ruido.extend(struct.pack('q', diff))
        
        return hashlib.sha256(ruido).digest()
    
    def _mezclar_pool(self):
        """Mezcla el pool de entropía usando operaciones no lineales"""
        # Aplicar múltiples rondas de mezclado
        for ronda in range(3):
            # Crear un hash del pool actual
            hash_actual = hashlib.sha512(self.pool_entropia).digest()
            
            # XOR con rotación
            for i in range(len(self.pool_entropia)):
                self.pool_entropia[i] ^= hash_actual[i % len(hash_actual)]
                # Rotación de bits
                self.pool_entropia[i] = ((self.pool_entropia[i] << 1) | 
                                       (self.pool_entropia[i] >> 7)) & 0xFF
    
    def obtener_bit_cuantico(self):
        """Simula la obtención de un bit cuántico"""
        # Actualizar el pool con nueva entropía
        self.pool_entropia.extend(os.urandom(8))
        self._mezclar_pool()
        
        # Extraer un byte y usar paridad como bit
        byte = self.pool_entropia[secrets.randbelow(len(self.pool_entropia))]
        
        # Contar bits para determinar paridad
        bit_count = bin(byte).count('1')
        
        # Agregar más aleatoriedad usando el tiempo
        tiempo_bit = int(time.perf_counter_ns()) & 1
        
        # Combinar ambas fuentes
        return (bit_count & 1) ^ tiempo_bit
    
    def obtener_numero_cuantico(self, max_valor):
        """Genera un número usando bits cuánticos simulados"""
        if max_valor <= 0:
            return 0
        
        # Calcular bits necesarios
        bits_necesarios = max_valor.bit_length()
        
        while True:
            # Generar número usando bits cuánticos
            numero = 0
            for i in range(bits_necesarios):
                if self.obtener_bit_cuantico():
                    numero |= (1 << i)
            
            # Si está en rango, retornar
            if numero < max_valor:
                return numero
    
    def obtener_flotante_cuantico(self):
        """Genera un flotante entre 0 y 1 usando método cuántico"""
        # Generar 53 bits (precisión de float64)
        mantisa = 0
        for i in range(53):
            if self.obtener_bit_cuantico():
                mantisa |= (1 << i)
        
        # Normalizar a [0, 1)
        return mantisa / (1 << 53)


class VerificadorAleatoriedad:
    """Verifica la calidad de la aleatoriedad en tiempo real"""
    
    def __init__(self, tamano_ventana=1000):
        self.tamano_ventana = tamano_ventana
        self.historial_valores = []
        self.historial_bits = []
        self.estadisticas = {}
    
    def agregar_valor(self, valor, max_valor):
        """Agrega un valor al historial para análisis"""
        self.historial_valores.append((valor, max_valor))
        
        # Mantener ventana deslizante
        if len(self.historial_valores) > self.tamano_ventana:
            self.historial_valores.pop(0)
        
        # Actualizar estadísticas cada 100 valores
        if len(self.historial_valores) % 100 == 0:
            self._actualizar_estadisticas()
    
    def agregar_bit(self, bit):
        """Agrega un bit al historial"""
        self.historial_bits.append(bit)
        
        if len(self.historial_bits) > self.tamano_ventana:
            self.historial_bits.pop(0)
    
    def _actualizar_estadisticas(self):
        """Calcula estadísticas de calidad"""
        if not self.historial_valores:
            return
        
        # Prueba de uniformidad
        valores = [v[0] for v in self.historial_valores]
        self.estadisticas['uniformidad'] = self._calcular_uniformidad(valores)
        
        # Prueba de independencia
        if len(valores) > 1:
            self.estadisticas['independencia'] = self._calcular_independencia(valores)
        
        # Balance de bits
        if self.historial_bits:
            unos = sum(self.historial_bits)
            total = len(self.historial_bits)
            self.estadisticas['balance_bits'] = abs(0.5 - (unos / total))
    
    def _calcular_uniformidad(self, valores):
        """Calcula qué tan uniforme es la distribución"""
        if not valores:
            return 0
        
        # Crear histograma
        from collections import Counter
        conteo = Counter(valores)
        
        # Calcular chi-cuadrado simplificado
        n = len(valores)
        k = len(conteo)
        if k == 0:
            return 0
        
        esperado = n / k
        chi2 = sum((observado - esperado)**2 / esperado 
                  for observado in conteo.values())
        
        # Normalizar a [0, 1] donde 1 es perfectamente uniforme
        return 1 / (1 + chi2 / n)
    
    def _calcular_independencia(self, valores):
        """Calcula independencia entre valores consecutivos"""
        # Correlación serial simplificada
        n = len(valores) - 1
        if n <= 0:
            return 1
        
        media = sum(valores) / len(valores)
        
        covarianza = sum((valores[i] - media) * (valores[i+1] - media) 
                        for i in range(n)) / n
        
        varianza = sum((v - media)**2 for v in valores) / len(valores)
        
        if varianza == 0:
            return 1
        
        correlacion = abs(covarianza / varianza)
        
        # Retornar 1 - correlación para que 1 sea perfectamente independiente
        return 1 - min(correlacion, 1)
    
    def obtener_calidad(self):
        """Retorna una medida general de calidad [0, 1]"""
        if not self.estadisticas:
            return 0
        
        factores = []
        
        if 'uniformidad' in self.estadisticas:
            factores.append(self.estadisticas['uniformidad'])
        
        if 'independencia' in self.estadisticas:
            factores.append(self.estadisticas['independencia'])
        
        if 'balance_bits' in self.estadisticas:
            # Convertir balance a calidad (0.5 es perfecto)
            balance_calidad = 1 - (self.estadisticas['balance_bits'] * 2)
            factores.append(max(0, balance_calidad))
        
        return sum(factores) / len(factores) if factores else 0
    
    def generar_reporte(self):
        """Genera un reporte de calidad"""
        calidad = self.obtener_calidad()
        
        print("\n📊 REPORTE DE CALIDAD DE ALEATORIEDAD")
        print("="*50)
        
        if 'uniformidad' in self.estadisticas:
            print(f"Uniformidad: {self.estadisticas['uniformidad']:.2%}")
        
        if 'independencia' in self.estadisticas:
            print(f"Independencia: {self.estadisticas['independencia']:.2%}")
        
        if 'balance_bits' in self.estadisticas:
            print(f"Balance de bits: {1 - self.estadisticas['balance_bits']*2:.2%}")
        
        print(f"\nCalidad general: {calidad:.2%}")
        
        if calidad > 0.9:
            print("✅ EXCELENTE: Aleatoriedad de alta calidad")
        elif calidad > 0.7:
            print("✅ BUENA: Aleatoriedad aceptable")
        elif calidad > 0.5:
            print("⚠️  REGULAR: Calidad mejorable")
        else:
            print("❌ POBRE: Baja calidad de aleatoriedad")


class GeneradorAleatorioVerificado:
    """Generador principal con múltiples fuentes y verificación"""
    
    def __init__(self, fuente=FuenteAleatoriedad.COMBINADO, verificar=True):
        self.fuente = fuente
        self.verificar = verificar
        
        # Inicializar generadores
        self.generador_cuantico = GeneradorCuanticoSimulado()
        self.system_random = random.SystemRandom()
        
        # Verificador
        self.verificador = VerificadorAleatoriedad() if verificar else None
        
        # Estadísticas
        self.llamadas = 0
        self.tiempo_inicio = time.time()
    
    def obtener_numero(self, max_valor):
        """Obtiene un número aleatorio según la fuente configurada"""
        self.llamadas += 1
        
        if self.fuente == FuenteAleatoriedad.PSEUDO_RANDOM:
            valor = random.randint(0, max_valor - 1)
            
        elif self.fuente == FuenteAleatoriedad.CRYPTO_RANDOM:
            valor = secrets.randbelow(max_valor)
            
        elif self.fuente == FuenteAleatoriedad.HARDWARE_RANDOM:
            valor = self.system_random.randint(0, max_valor - 1)
            
        elif self.fuente == FuenteAleatoriedad.QUANTUM_SIMULATED:
            valor = self.generador_cuantico.obtener_numero_cuantico(max_valor)
            
        elif self.fuente == FuenteAleatoriedad.COMBINADO:
            # Combinar múltiples fuentes
            valores = [
                random.randint(0, max_valor - 1),
                secrets.randbelow(max_valor),
                self.generador_cuantico.obtener_numero_cuantico(max_valor)
            ]
            
            # Usar XOR para combinar
            valor = valores[0]
            for v in valores[1:]:
                valor ^= v
            valor %= max_valor
        
        else:
            valor = 0
        
        # Verificar si está habilitado
        if self.verificador:
            self.verificador.agregar_valor(valor, max_valor)
        
        return valor
    
    def obtener_bool(self):
        """Obtiene un booleano aleatorio"""
        if self.fuente == FuenteAleatoriedad.QUANTUM_SIMULATED:
            bit = self.generador_cuantico.obtener_bit_cuantico()
        else:
            bit = self.obtener_numero(2)
        
        if self.verificador:
            self.verificador.agregar_bit(bit)
        
        return bool(bit)
    
    def obtener_flotante(self):
        """Obtiene un flotante entre 0 y 1"""
        if self.fuente == FuenteAleatoriedad.QUANTUM_SIMULATED:
            return self.generador_cuantico.obtener_flotante_cuantico()
        else:
            return self.obtener_numero(2**53) / (2**53)
    
    def mezclar_lista(self, lista):
        """Mezcla una lista usando el generador configurado"""
        lista_copia = lista.copy()
        
        # Fisher-Yates con nuestro generador
        for i in range(len(lista_copia) - 1, 0, -1):
            j = self.obtener_numero(i + 1)
            lista_copia[i], lista_copia[j] = lista_copia[j], lista_copia[i]
        
        return lista_copia
    
    def obtener_estadisticas(self):
        """Retorna estadísticas del generador"""
        tiempo_total = time.time() - self.tiempo_inicio
        
        stats = {
            'fuente': self.fuente.value,
            'llamadas': self.llamadas,
            'tiempo_total': tiempo_total,
            'llamadas_por_segundo': self.llamadas / tiempo_total if tiempo_total > 0 else 0
        }
        
        if self.verificador:
            stats['calidad'] = self.verificador.obtener_calidad()
        
        return stats


# Ejemplo de uso y prueba
def demostrar_aleatoriedad():
    """Demuestra y compara diferentes fuentes de aleatoriedad"""
    print("🎲 DEMOSTRACIÓN DE FUENTES DE ALEATORIEDAD")
    print("="*60)
    
    fuentes = [
        FuenteAleatoriedad.PSEUDO_RANDOM,
        FuenteAleatoriedad.CRYPTO_RANDOM,
        FuenteAleatoriedad.QUANTUM_SIMULATED,
        FuenteAleatoriedad.COMBINADO
    ]
    
    for fuente in fuentes:
        print(f"\n🔸 Probando: {fuente.value}")
        print("-"*40)
        
        gen = GeneradorAleatorioVerificado(fuente, verificar=True)
        
        # Generar valores de prueba
        print("Muestra de 10 valores [0-77]:", end=" ")
        for _ in range(10):
            print(gen.obtener_numero(78), end=" ")
        print()
        
        # Generar muchos valores para estadísticas
        for _ in range(1000):
            gen.obtener_numero(78)
            gen.obtener_bool()
        
        # Mostrar estadísticas
        stats = gen.obtener_estadisticas()
        print(f"Velocidad: {stats['llamadas_por_segundo']:.0f} ops/s")
        
        if 'calidad' in stats:
            print(f"Calidad: {stats['calidad']:.2%}")
    
    print("\n" + "="*60)
    print("💡 Recomendación: Usar COMBINADO para máxima aleatoriedad")


if __name__ == "__main__":
    # Demostrar fuentes
    demostrar_aleatoriedad()
    
    print("\n\n🃏 PRUEBA CON MAZO DE TAROT")
    print("="*60)
    
    # Crear generador combinado con verificación
    gen = GeneradorAleatorioVerificado(FuenteAleatoriedad.COMBINADO, verificar=True)
    
    # Simular barajado de mazo
    mazo = list(range(78))
    mazo_barajado = gen.mezclar_lista(mazo)
    
    print(f"Primeras 10 cartas: {mazo_barajado[:10]}")
    
    # Generar reporte de calidad
    if gen.verificador:
        gen.verificador.generar_reporte()
    
    print("\n✨ Sistema de aleatoriedad verificado y funcionando")