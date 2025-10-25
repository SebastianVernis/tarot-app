# 🔮 Sistema de Lectura de Tarot

> Un sistema completo de lectura de tarot con múltiples capas de aleatorización y verificación de calidad.

## 📋 Descripción

Este proyecto implementa un sistema de lectura de tarot que simula la experiencia de una lectura real mediante:

- **Múltiples fuentes de aleatoriedad**: Pseudo-aleatoria, criptográfica, simulación cuántica
- **Verificación de calidad**: Sistema de análisis estadístico en tiempo real
- **Múltiples tipos de tiradas**: Una carta, tres cartas, Cruz Celta, Herradura, Relación
- **Interfaz web moderna**: Diseño místico con animaciones y efectos visuales
- **Mazo completo**: 78 cartas (22 Arcanos Mayores + 56 Arcanos Menores)

## 🚀 Características

### ✨ Funcionalidades Principales

- **Lecturas interactivas** con interpretaciones personalizadas
- **Sistema de aleatorización verificada** con múltiples algoritmos
- **Análisis estadístico** de la calidad de aleatoriedad
- **Interfaz web responsiva** con efectos visuales
- **Historial de lecturas** en formato JSON
- **Múltiples tipos de tirada** para diferentes consultas

### 🎲 Tipos de Aleatorización

- **Pseudo-random**: Generador estándar de Python
- **Crypto-random**: Módulo `secrets` para aleatoriedad criptográfica
- **Hardware-random**: `SystemRandom` usando entropía del OS
- **Quantum-simulated**: Simulación de comportamiento cuántico
- **Combinado**: Fusión de múltiples fuentes para máxima entropía

### 🃏 Tipos de Tiradas

1. **Una Carta del Día** - Guía diaria (1 carta)
2. **Pasado, Presente y Futuro** - Visión temporal (3 cartas)
3. **Cruz Celta** - Análisis completo (10 cartas)
4. **Herradura** - Situación y consejo (7 cartas)
5. **Lectura de Relación** - Análisis de vínculos (6 cartas)

## 📁 Estructura del Proyecto

```
tarot-app/
├── tarot_reader.py              # Lector básico de tarot
├── tarot_reader_enhanced.py     # Versión mejorada con alta aleatorización
├── tarot_quantum_random.py      # Generador cuántico simulado
├── tarot_randomness_test.py     # Suite de pruebas estadísticas
├── tarot_web.html              # Interfaz web principal
├── tarot_web.js                # Lógica JavaScript
├── README.md                   # Este archivo
├── CRUSH.md                    # Configuración para agentes de código
└── DEPLOYMENT.md               # Guía de despliegue
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8 o superior
- Navegador web moderno (para la interfaz web)

### Dependencias Python

```bash
pip install numpy matplotlib scipy
```

### Instalación Rápida

```bash
# Clonar el repositorio
git clone <repository-url>
cd tarot-app

# Instalar dependencias
pip install -r requirements.txt  # Si existe
# O instalar manualmente:
pip install numpy matplotlib scipy

# Verificar instalación
python tarot_reader.py
```

## 🎮 Uso

### Modo Consola

#### Lector Básico
```bash
python tarot_reader.py
```

#### Lector Mejorado (Recomendado)
```bash
python tarot_reader_enhanced.py
```

#### Generador Cuántico
```bash
python tarot_quantum_random.py
```

#### Pruebas de Calidad
```bash
python tarot_randomness_test.py
```

### Interfaz Web

1. Abrir `tarot_web.html` en un navegador
2. Seleccionar tipo de tirada
3. Opcional: Escribir una pregunta
4. Hacer clic en "Comenzar Lectura"
5. Esperar la animación de barajado
6. Revisar los resultados

## 🧪 Pruebas y Verificación

El sistema incluye múltiples pruebas estadísticas:

### Pruebas Implementadas

1. **Distribución Uniforme** - Chi-cuadrado
2. **Independencia Secuencial** - Correlación de Pearson
3. **Entropía de Shannon** - Medida de aleatoriedad
4. **Balance de Bits** - Prueba binomial
5. **Impredecibilidad** - Análisis de patrones
6. **Velocidad** - Benchmark de rendimiento
7. **Hardware** - Verificación de fuentes de entropía

### Ejecutar Pruebas

```bash
# Suite completa de pruebas
python tarot_randomness_test.py

# Genera archivos:
# - reporte_aleatoriedad.json
# - distribucion_cartas.png
# - comparacion_barajado.png
```

## 📊 Salida y Resultados

### Archivos Generados

- **lecturas_tarot.json**: Historial de lecturas guardadas
- **reporte_aleatoriedad.json**: Análisis estadístico detallado
- **distribucion_cartas.png**: Gráfico de distribución
- **comparacion_barajado.png**: Comparación de métodos de barajado

### Formato de Lectura

```json
{
  "fecha": "2024-10-25T...",
  "tipo_tirada": "Tres Cartas",
  "pregunta": "¿Cómo me va en el amor?",
  "cartas": [
    {
      "posicion": "Pasado",
      "carta": "El Sol",
      "invertida": false,
      "significado": "Alegría, éxito, celebración",
      "palabras_clave": ["alegría", "éxito"]
    }
  ],
  "interpretacion": "..."
}
```

## 🎨 Personalización

### Modificar Cartas

Editar las definiciones en:
- `tarot_reader.py` (líneas 49-421)
- `tarot_web.js` (objeto TAROT_DB)

### Nuevos Tipos de Tirada

1. Agregar al enum `TipoTirada`
2. Definir posiciones en `_definir_tiradas()`
3. Actualizar la interfaz web

### Algoritmos de Aleatorización

Implementar nuevos generadores en `GeneradorAleatorio` o `GeneradorCuanticoSimulado`.

## 🔧 Configuración Avanzada

### Variables de Entorno

```bash
# Configurar fuente de aleatoriedad por defecto
export TAROT_RANDOM_SOURCE="combinado"

# Habilitar modo debug
export TAROT_DEBUG="true"
```

### Parámetros del Verificador

```python
# En el código
verificador = VerificadorAleatoriedad(tamano_ventana=5000)  # Más muestras
```

## 🐛 Resolución de Problemas

### Errores Comunes

#### "ModuleNotFoundError: No module named 'numpy'"
```bash
pip install numpy matplotlib scipy
```

#### "Entropía baja del kernel"
```bash
# En Linux, instalar generador de entropía
sudo apt-get install rng-tools
sudo systemctl enable rngd
```

#### La interfaz web no carga
- Verificar que `tarot_web.js` esté en la misma carpeta
- Abrir las herramientas de desarrollador para ver errores
- Probar en modo servidor local

### Modo Debug

Activar logging detallado modificando las llamadas a `print()` por un sistema de logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Métricas de Calidad

### Interpretar Resultados

- **Calidad > 90%**: Excelente aleatoriedad
- **Calidad 70-90%**: Buena aleatoriedad 
- **Calidad 50-70%**: Regular, mejorable
- **Calidad < 50%**: Pobre, requiere ajustes

### Factores que Afectan la Calidad

- Entropía disponible del sistema
- Velocidad del procesador
- Carga del sistema
- Fuente de aleatoriedad seleccionada

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama para la característica (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de los cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Pautas de Contribución

- Seguir las convenciones de código en `CRUSH.md`
- Agregar pruebas para nuevas funcionalidades
- Documentar cambios en el README
- Mantener compatibilidad hacia atrás

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para detalles.

## 🙏 Agradecimientos

- Inspirado en los sistemas tradicionales de tarot
- Utiliza principios de aleatoriedad criptográfica
- Diseño web inspirado en la estética mística

## 📞 Soporte

Para reportar bugs o solicitar funcionalidades:

1. Crear un issue en el repositorio
2. Incluir información del sistema
3. Pasos para reproducir el problema
4. Logs relevantes

---

*Que las cartas iluminen tu camino* ✨