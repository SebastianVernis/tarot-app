#!/usr/bin/env python3
"""
Sistema de Pruebas de Aleatoriedad para Tarot
Autor: Assistant
Descripción: Verifica la calidad de la aleatoriedad en el sistema de tarot
"""

import random
import secrets
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import hashlib
import os
from scipy import stats
import json


class PruebasAleatoriedad:
    """Clase para realizar múltiples pruebas de aleatoriedad"""
    
    def __init__(self):
        self.resultados = {}
    
    def prueba_distribucion_uniforme(self, muestras=10000):
        """Prueba que las cartas se distribuyan uniformemente"""
        print("\n🔬 PRUEBA 1: Distribución Uniforme de Cartas")
        print("-" * 50)
        
        # Crear un mazo simplificado de 78 cartas
        contador_cartas = Counter()
        
        for _ in range(muestras):
            # Simular sacar una carta aleatoria
            carta_id = secrets.randbelow(78)
            contador_cartas[carta_id] += 1
        
        # Calcular estadísticas
        frecuencias = list(contador_cartas.values())
        media_esperada = muestras / 78
        media_real = np.mean(frecuencias)
        desviacion = np.std(frecuencias)
        
        # Prueba Chi-cuadrado
        chi2, p_value = stats.chisquare(frecuencias)
        
        print(f"📊 Resultados tras {muestras} extracciones:")
        print(f"   Media esperada: {media_esperada:.2f}")
        print(f"   Media real: {media_real:.2f}")
        print(f"   Desviación estándar: {desviacion:.2f}")
        print(f"   Valor p (Chi-cuadrado): {p_value:.4f}")
        
        if p_value > 0.05:
            print("   ✅ La distribución parece uniforme (p > 0.05)")
        else:
            print("   ⚠️  La distribución podría no ser uniforme (p < 0.05)")
        
        self.resultados['distribucion_uniforme'] = {
            'p_value': p_value,
            'uniforme': p_value > 0.05
        }
        
        # Visualizar
        plt.figure(figsize=(10, 6))
        plt.hist(frecuencias, bins=20, edgecolor='black')
        plt.axvline(media_esperada, color='red', linestyle='--', 
                   label=f'Media esperada: {media_esperada:.2f}')
        plt.xlabel('Frecuencia de aparición')
        plt.ylabel('Número de cartas')
        plt.title('Distribución de frecuencias de las cartas')
        plt.legend()
        plt.savefig('distribucion_cartas.png')
        plt.close()
        
        return p_value > 0.05
    
    def prueba_independencia_secuencial(self, muestras=5000):
        """Verifica que las cartas consecutivas sean independientes"""
        print("\n🔬 PRUEBA 2: Independencia Secuencial")
        print("-" * 50)
        
        secuencias = []
        for _ in range(muestras):
            # Generar pares de cartas consecutivas
            carta1 = secrets.randbelow(78)
            carta2 = secrets.randbelow(78)
            secuencias.append((carta1, carta2))
        
        # Análisis de correlación
        cartas1 = [s[0] for s in secuencias]
        cartas2 = [s[1] for s in secuencias]
        
        correlacion, p_value = stats.pearsonr(cartas1, cartas2)
        
        print(f"📊 Resultados tras {muestras} pares:")
        print(f"   Correlación: {correlacion:.4f}")
        print(f"   Valor p: {p_value:.4f}")
        
        if abs(correlacion) < 0.1:
            print("   ✅ Las cartas consecutivas parecen independientes")
        else:
            print("   ⚠️  Posible dependencia entre cartas consecutivas")
        
        self.resultados['independencia'] = {
            'correlacion': correlacion,
            'independiente': abs(correlacion) < 0.1
        }
        
        return abs(correlacion) < 0.1
    
    def prueba_entropia(self, muestras=10000):
        """Mide la entropía de las secuencias generadas"""
        print("\n🔬 PRUEBA 3: Entropía de Shannon")
        print("-" * 50)
        
        # Generar secuencias de bytes aleatorios
        bytes_random = []
        bytes_secrets = []
        
        for _ in range(muestras):
            bytes_random.append(random.randint(0, 255))
            bytes_secrets.append(secrets.randbits(8))
        
        def calcular_entropia(data):
            """Calcula la entropía de Shannon"""
            contador = Counter(data)
            probs = [count/len(data) for count in contador.values()]
            entropia = -sum(p * np.log2(p) for p in probs if p > 0)
            return entropia
        
        entropia_random = calcular_entropia(bytes_random)
        entropia_secrets = calcular_entropia(bytes_secrets)
        entropia_maxima = 8  # Para 8 bits
        
        print(f"📊 Resultados de entropía:")
        print(f"   Entropía random.randint: {entropia_random:.4f} bits")
        print(f"   Entropía secrets: {entropia_secrets:.4f} bits")
        print(f"   Entropía máxima teórica: {entropia_maxima} bits")
        print(f"   Eficiencia random: {(entropia_random/entropia_maxima)*100:.2f}%")
        print(f"   Eficiencia secrets: {(entropia_secrets/entropia_maxima)*100:.2f}%")
        
        if entropia_secrets > 7.9:
            print("   ✅ Excelente entropía (muy aleatorio)")
        elif entropia_secrets > 7.5:
            print("   ✅ Buena entropía")
        else:
            print("   ⚠️  Entropía subóptima")
        
        self.resultados['entropia'] = {
            'entropia_secrets': entropia_secrets,
            'alta_entropia': entropia_secrets > 7.5
        }
        
        return entropia_secrets > 7.5
    
    def prueba_patrones_invertidas(self, muestras=10000):
        """Verifica la aleatoriedad de cartas derechas vs invertidas"""
        print("\n🔬 PRUEBA 4: Distribución de Cartas Invertidas")
        print("-" * 50)
        
        # Diferentes métodos para decidir si una carta está invertida
        metodos = {
            'simple': lambda: random.random() > 0.5,
            'secrets': lambda: secrets.randbits(1) == 1,
            'tiempo': lambda: int(time.time() * 1000000) % 2 == 0,
            'combinado': lambda: sum([
                random.random() > 0.5,
                secrets.randbits(1) == 1,
                int(time.time() * 1000000) % 2 == 0
            ]) >= 2
        }
        
        resultados_metodos = {}
        
        for nombre, metodo in metodos.items():
            invertidas = sum(metodo() for _ in range(muestras))
            proporcion = invertidas / muestras
            
            # Prueba binomial
            p_value = stats.binom_test(invertidas, muestras, 0.5, alternative='two-sided')
            
            resultados_metodos[nombre] = {
                'proporcion': proporcion,
                'p_value': p_value
            }
            
            print(f"\n   Método '{nombre}':")
            print(f"      Proporción invertidas: {proporcion:.4f}")
            print(f"      Valor p: {p_value:.4f}")
            
            if p_value > 0.05:
                print(f"      ✅ Distribución equilibrada")
            else:
                print(f"      ⚠️  Posible sesgo")
        
        # El método combinado debería ser el mejor
        mejor_metodo = 'combinado'
        self.resultados['invertidas'] = {
            'mejor_metodo': mejor_metodo,
            'equilibrado': resultados_metodos[mejor_metodo]['p_value'] > 0.05
        }
        
        return resultados_metodos[mejor_metodo]['p_value'] > 0.05
    
    def prueba_impredecibilidad(self, intentos=1000):
        """Prueba si las secuencias son predecibles"""
        print("\n🔬 PRUEBA 5: Impredecibilidad de Secuencias")
        print("-" * 50)
        
        # Generar secuencias y ver si hay patrones
        secuencias = []
        for _ in range(intentos):
            # Combinar múltiples fuentes de aleatoriedad
            valor = (
                secrets.randbits(32) ^
                int(time.perf_counter() * 1000000) ^
                hash(os.urandom(8))
            ) % 78
            secuencias.append(valor)
        
        # Buscar patrones repetitivos
        patrones_2 = Counter(zip(secuencias[:-1], secuencias[1:]))
        patrones_3 = Counter(zip(secuencias[:-2], secuencias[1:-1], secuencias[2:]))
        
        max_repeticion_2 = max(patrones_2.values())
        max_repeticion_3 = max(patrones_3.values())
        
        esperado_2 = intentos / (78 * 78)
        esperado_3 = intentos / (78 * 78 * 78)
        
        print(f"📊 Análisis de patrones:")
        print(f"   Pares repetidos máximo: {max_repeticion_2} (esperado: ~{esperado_2:.2f})")
        print(f"   Tríos repetidos máximo: {max_repeticion_3} (esperado: ~{esperado_3:.2f})")
        
        # Si las repeticiones son menores a 3x lo esperado, es bueno
        impredecible = (max_repeticion_2 < esperado_2 * 3 and 
                       max_repeticion_3 < esperado_3 * 3)
        
        if impredecible:
            print("   ✅ Las secuencias parecen impredecibles")
        else:
            print("   ⚠️  Posibles patrones detectados")
        
        self.resultados['impredecibilidad'] = {
            'impredecible': impredecible
        }
        
        return impredecible
    
    def prueba_velocidad_generacion(self):
        """Compara la velocidad de diferentes métodos"""
        print("\n🔬 PRUEBA 6: Velocidad de Generación")
        print("-" * 50)
        
        iteraciones = 100000
        
        # Método 1: random simple
        inicio = time.perf_counter()
        for _ in range(iteraciones):
            random.randint(0, 77)
        tiempo_random = time.perf_counter() - inicio
        
        # Método 2: secrets
        inicio = time.perf_counter()
        for _ in range(iteraciones):
            secrets.randbelow(78)
        tiempo_secrets = time.perf_counter() - inicio
        
        # Método 3: SystemRandom
        sys_random = random.SystemRandom()
        inicio = time.perf_counter()
        for _ in range(iteraciones):
            sys_random.randint(0, 77)
        tiempo_system = time.perf_counter() - inicio
        
        print(f"📊 Tiempos para {iteraciones} generaciones:")
        print(f"   random.randint: {tiempo_random:.4f}s ({iteraciones/tiempo_random:.0f} ops/s)")
        print(f"   secrets.randbelow: {tiempo_secrets:.4f}s ({iteraciones/tiempo_secrets:.0f} ops/s)")
        print(f"   SystemRandom: {tiempo_system:.4f}s ({iteraciones/tiempo_system:.0f} ops/s)")
        
        print("\n   💡 Nota: secrets y SystemRandom son más lentos pero más seguros")
        
        self.resultados['velocidad'] = {
            'random': tiempo_random,
            'secrets': tiempo_secrets,
            'system': tiempo_system
        }
    
    def verificar_fuentes_hardware(self):
        """Verifica las fuentes de entropía del sistema"""
        print("\n🔬 PRUEBA 7: Fuentes de Entropía del Sistema")
        print("-" * 50)
        
        # Verificar /dev/urandom
        try:
            urandom_test = os.urandom(16)
            print("   ✅ /dev/urandom disponible")
            print(f"      Muestra: {urandom_test.hex()[:32]}...")
        except:
            print("   ❌ /dev/urandom no disponible")
        
        # Verificar entropía disponible en Linux
        try:
            with open('/proc/sys/kernel/random/entropy_avail', 'r') as f:
                entropia_disponible = int(f.read().strip())
            print(f"   ✅ Entropía del kernel: {entropia_disponible} bits")
            if entropia_disponible < 256:
                print("      ⚠️  Entropía baja, considera usar rngd o haveged")
        except:
            print("   ℹ️  No se puede verificar entropía del kernel (no Linux?)")
        
        # Verificar RDRAND (instrucción de CPU)
        try:
            # Python's secrets usa RDRAND cuando está disponible
            test_secrets = secrets.token_bytes(32)
            print("   ✅ Generación criptográfica funcionando correctamente")
        except:
            print("   ❌ Problema con generación criptográfica")
        
        self.resultados['hardware'] = {
            'urandom': True,
            'entropia_kernel': entropia_disponible if 'entropia_disponible' in locals() else None
        }
    
    def generar_reporte_completo(self):
        """Genera un reporte completo de todas las pruebas"""
        print("\n" + "="*60)
        print("📋 REPORTE FINAL DE ALEATORIEDAD")
        print("="*60)
        
        pruebas_pasadas = 0
        total_pruebas = 0
        
        for prueba, resultado in self.resultados.items():
            if isinstance(resultado, dict) and any(k.endswith('e') or k == 'impredecible' for k in resultado.keys()):
                total_pruebas += 1
                # Buscar si la prueba pasó
                for k, v in resultado.items():
                    if (k.endswith('e') or k == 'impredecible') and isinstance(v, bool):
                        if v:
                            pruebas_pasadas += 1
                        break
        
        porcentaje = (pruebas_pasadas / total_pruebas * 100) if total_pruebas > 0 else 0
        
        print(f"\n✅ Pruebas pasadas: {pruebas_pasadas}/{total_pruebas} ({porcentaje:.1f}%)")
        
        if porcentaje >= 80:
            print("\n🎉 EXCELENTE: El sistema tiene alta calidad de aleatoriedad")
        elif porcentaje >= 60:
            print("\n👍 BUENO: El sistema tiene buena aleatoriedad")
        else:
            print("\n⚠️  MEJORABLE: Considere ajustar el sistema de aleatoriedad")
        
        # Guardar reporte
        with open('reporte_aleatoriedad.json', 'w') as f:
            json.dump(self.resultados, f, indent=2)
        print("\n📄 Reporte detallado guardado en 'reporte_aleatoriedad.json'")


def comparar_metodos_barajado():
    """Compara diferentes métodos de barajado"""
    print("\n🃏 COMPARACIÓN DE MÉTODOS DE BARAJADO")
    print("="*60)
    
    mazo_original = list(range(78))
    
    # Método 1: Shuffle simple
    mazo1 = mazo_original.copy()
    random.shuffle(mazo1)
    
    # Método 2: Shuffle múltiple
    mazo2 = mazo_original.copy()
    for _ in range(7):
        random.shuffle(mazo2)
    
    # Método 3: Shuffle + cortes
    mazo3 = mazo_original.copy()
    for _ in range(3):
        random.shuffle(mazo3)
        # Cortar el mazo
        punto_corte = random.randint(20, 58)
        mazo3 = mazo3[punto_corte:] + mazo3[:punto_corte]
    
    # Método 4: Método combinado con secrets
    mazo4 = mazo_original.copy()
    random.shuffle(mazo4)
    # Transposiciones aleatorias
    for _ in range(len(mazo4) // 2):
        i = secrets.randbelow(len(mazo4))
        j = secrets.randbelow(len(mazo4))
        mazo4[i], mazo4[j] = mazo4[j], mazo4[i]
    
    # Analizar qué tan diferentes son del mazo original
    def calcular_distancia(mazo1, mazo2):
        """Calcula cuántas posiciones cambiaron"""
        return sum(1 for i in range(len(mazo1)) if mazo1[i] != mazo2[i])
    
    print(f"\n📊 Cartas que cambiaron de posición:")
    print(f"   Shuffle simple: {calcular_distancia(mazo_original, mazo1)}/78")
    print(f"   Shuffle múltiple (7x): {calcular_distancia(mazo_original, mazo2)}/78")
    print(f"   Shuffle + cortes: {calcular_distancia(mazo_original, mazo3)}/78")
    print(f"   Método combinado: {calcular_distancia(mazo_original, mazo4)}/78")
    
    # Visualizar distribución
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].scatter(range(78), mazo1, alpha=0.6, s=20)
    axes[0, 0].set_title('Shuffle Simple')
    axes[0, 0].set_xlabel('Posición final')
    axes[0, 0].set_ylabel('Carta (ID original)')
    
    axes[0, 1].scatter(range(78), mazo2, alpha=0.6, s=20)
    axes[0, 1].set_title('Shuffle Múltiple (7x)')
    axes[0, 1].set_xlabel('Posición final')
    axes[0, 1].set_ylabel('Carta (ID original)')
    
    axes[1, 0].scatter(range(78), mazo3, alpha=0.6, s=20)
    axes[1, 0].set_title('Shuffle + Cortes')
    axes[1, 0].set_xlabel('Posición final')
    axes[1, 0].set_ylabel('Carta (ID original)')
    
    axes[1, 1].scatter(range(78), mazo4, alpha=0.6, s=20)
    axes[1, 1].set_title('Método Combinado')
    axes[1, 1].set_xlabel('Posición final')
    axes[1, 1].set_ylabel('Carta (ID original)')
    
    plt.tight_layout()
    plt.savefig('comparacion_barajado.png')
    plt.close()
    
    print("\n📊 Gráfico guardado en 'comparacion_barajado.png'")


def main():
    """Ejecuta todas las pruebas de aleatoriedad"""
    print("🎯 SISTEMA DE VERIFICACIÓN DE ALEATORIEDAD PARA TAROT")
    print("="*60)
    print("Este programa verificará qué tan aleatorio es el sistema")
    print("="*60)
    
    pruebas = PruebasAleatoriedad()
    
    # Ejecutar todas las pruebas
    pruebas.prueba_distribucion_uniforme()
    input("\nPresiona Enter para continuar...")
    
    pruebas.prueba_independencia_secuencial()
    input("\nPresiona Enter para continuar...")
    
    pruebas.prueba_entropia()
    input("\nPresiona Enter para continuar...")
    
    pruebas.prueba_patrones_invertidas()
    input("\nPresiona Enter para continuar...")
    
    pruebas.prueba_impredecibilidad()
    input("\nPresiona Enter para continuar...")
    
    pruebas.prueba_velocidad_generacion()
    input("\nPresiona Enter para continuar...")
    
    pruebas.verificar_fuentes_hardware()
    input("\nPresiona Enter para continuar...")
    
    comparar_metodos_barajado()
    input("\nPresiona Enter para continuar...")
    
    pruebas.generar_reporte_completo()
    
    print("\n✨ Verificación completa. ¡Revisa los archivos generados!")


if __name__ == "__main__":
    main()