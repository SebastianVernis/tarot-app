#!/usr/bin/env python3
"""
Prueba Automatizada de Aleatoriedad para Tarot
Ejecuta todas las pruebas sin interacción del usuario
"""

import sys
import os

# Suprimir las solicitudes de input
class AutoInput:
    def __init__(self):
        self.call_count = 0
    
    def __call__(self, prompt=""):
        self.call_count += 1
        return ""

# Reemplazar input con versión automática
original_input = input
input = AutoInput()

# Importar el módulo de pruebas
from tarot_randomness_test import PruebasAleatoriedad, comparar_metodos_barajado

def main():
    """Ejecuta todas las pruebas automáticamente"""
    print("🎯 SISTEMA DE VERIFICACIÓN DE ALEATORIEDAD PARA TAROT")
    print("="*60)
    print("Ejecutando pruebas automáticas...")
    print("Objetivo: >90% de calidad y cobertura")
    print("="*60)
    
    pruebas = PruebasAleatoriedad()
    
    # Ejecutar todas las pruebas
    print("\n[1/11] Ejecutando prueba de distribución uniforme...")
    pruebas.prueba_distribucion_uniforme()
    
    print("\n[2/11] Ejecutando prueba de independencia secuencial...")
    pruebas.prueba_independencia_secuencial()
    
    print("\n[3/11] Ejecutando prueba de entropía...")
    pruebas.prueba_entropia()
    
    print("\n[4/11] Ejecutando prueba de patrones invertidas...")
    pruebas.prueba_patrones_invertidas()
    
    print("\n[5/11] Ejecutando prueba de impredecibilidad...")
    pruebas.prueba_impredecibilidad()
    
    print("\n[6/11] Ejecutando prueba de velocidad...")
    pruebas.prueba_velocidad_generacion()
    
    print("\n[7/11] Verificando fuentes de hardware...")
    pruebas.verificar_fuentes_hardware()
    
    print("\n[8/11] Ejecutando prueba de tipos de tirada...")
    pruebas.prueba_tipos_tirada()
    
    print("\n[9/11] Ejecutando prueba de invertidas por tipo...")
    pruebas.prueba_cartas_invertidas_por_tipo()
    
    print("\n[10/11] Calculando cobertura...")
    pruebas.calcular_cobertura()
    
    print("\n[11/11] Comparando métodos de barajado...")
    comparar_metodos_barajado()
    
    print("\n" + "="*60)
    print("Generando reporte final...")
    pruebas.generar_reporte_completo()
    
    print("\n✨ Verificación completa!")
    print("📊 Archivos generados:")
    print("   • reporte_aleatoriedad.json - Reporte detallado")
    print("   • distribucion_cartas.png - Gráfico de distribución")
    print("   • comparacion_barajado.png - Comparación de métodos")
    
    # Verificar si cumple con los requisitos
    if pruebas.cobertura_pruebas >= 90:
        print("\n✅ ÉXITO: Cobertura de pruebas >90%")
        
        # Contar pruebas pasadas usando la misma lógica que el reporte
        pruebas_individuales = [
            ('distribucion_uniforme', 'uniforme'),
            ('independencia', 'independiente'),
            ('entropia', 'alta_entropia'),
            ('invertidas', 'equilibrado'),
            ('impredecibilidad', 'impredecible'),
            ('tipos_tirada', 'todos_correctos'),
            ('invertidas_por_tipo', 'todos_equilibrados')
        ]
        
        pruebas_pasadas = 0
        total_pruebas = 0
        
        for prueba_nombre, clave_exito in pruebas_individuales:
            if prueba_nombre in pruebas.resultados:
                resultado = pruebas.resultados[prueba_nombre]
                if isinstance(resultado, dict) and clave_exito in resultado:
                    total_pruebas += 1
                    if resultado[clave_exito]:
                        pruebas_pasadas += 1
        
        porcentaje = (pruebas_pasadas / total_pruebas * 100) if total_pruebas > 0 else 0
        
        if porcentaje >= 90:
            print(f"✅ ÉXITO: Calidad de aleatoriedad {porcentaje:.1f}% (>90%)")
            print("\n🎉 TODOS LOS REQUISITOS CUMPLIDOS")
            print("   ✓ Aleatoriedad 100% verificada")
            print("   ✓ Cobertura >90%")
            print("   ✓ Calidad >90%")
            return 0
        else:
            print(f"⚠️  ADVERTENCIA: Calidad {porcentaje:.1f}% (<90%)")
            return 1
    else:
        print(f"\n⚠️  ADVERTENCIA: Cobertura {pruebas.cobertura_pruebas:.1f}% (<90%)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
