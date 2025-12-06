# 🌟 Implementación de Cálculos Astrológicos Precisos

## Resumen

Se ha implementado exitosamente un sistema completo de cálculos astrológicos precisos con las siguientes características:

- ✅ Cálculo de posiciones planetarias exactas usando Swiss Ephemeris
- ✅ Generación de cartas natales completas con casas astrológicas
- ✅ Cálculo de aspectos planetarios
- ✅ Integración con Google Gemini AI para interpretaciones personalizadas
- ✅ API RESTful completa con autenticación JWT
- ✅ Almacenamiento persistente de lecturas astrológicas

## Archivos Creados/Modificados

### Nuevos Archivos

1. **`astrology_calculator.py`** - Módulo principal de cálculos astrológicos
   - Clase `AstrologyCalculator` con métodos para:
     - Cálculo de posiciones planetarias (10 planetas)
     - Cálculo de casas astrológicas (sistema Placidus)
     - Cálculo de aspectos planetarios
     - Conversión de coordenadas eclípticas a signos zodiacales
     - Detección de planetas retrógrados

2. **`gemini_service.py`** - Servicio de integración con Gemini AI
   - Clase `GeminiService` con métodos para:
     - Interpretación de cartas natales completas
     - Interpretación de posiciones planetarias
     - Horóscopo diario
     - Análisis de compatibilidad
     - Interpretación de tránsitos

3. **`routes/astrology_routes.py`** - Rutas API para astrología
   - Endpoints implementados:
     - `POST /api/astrology/calculate` - Calcular posiciones planetarias
     - `POST /api/astrology/birth-chart` - Generar carta natal completa
     - `GET /api/astrology/readings` - Obtener lecturas guardadas
     - `GET /api/astrology/readings/<id>` - Obtener lectura específica
     - `PUT /api/astrology/readings/<id>` - Actualizar lectura
     - `DELETE /api/astrology/readings/<id>` - Eliminar lectura
     - `POST /api/astrology/daily-horoscope` - Horóscopo diario
     - `POST /api/astrology/compatibility` - Análisis de compatibilidad
     - `GET /api/astrology/info` - Información del servicio

4. **`test_astrology_api.py`** - Script de pruebas automatizadas

### Archivos Modificados

1. **`requirements.txt`** - Agregadas dependencias:
   ```
   pyswisseph>=2.10.3.2
   timezonefinder>=6.2.0
   pytz>=2023.3
   google-generativeai>=0.3.0
   ```

2. **`models.py`** - Agregado modelo `AstrologyReading`:
   - Almacena datos de nacimiento
   - Guarda posiciones planetarias en JSON
   - Almacena interpretaciones generadas por IA
   - Incluye resumen rápido (Sol, Luna, Ascendente)

3. **`config.py`** - Agregadas configuraciones:
   - `GEMINI_API_KEY` - Clave API de Gemini
   - `ASTROLOGY_ENABLED` - Flag para habilitar/deshabilitar
   - `FREE_ASTROLOGY_READINGS` - Límite para usuarios gratuitos

4. **`.env.example`** - Agregada variable:
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

5. **`app.py`** - Registrado blueprint de astrología:
   - Importado `astrology_bp`
   - Registrado en la aplicación
   - Actualizada información de API

6. **`auth.py`** - Corregido manejo de identidad JWT:
   - Convertir user_id a string en tokens
   - Manejar conversión de string a int en decoradores

## Características Técnicas

### Cálculos Astronómicos

**Swiss Ephemeris**: Biblioteca de efemérides más precisa disponible
- Precisión: ±0.001° (3.6 segundos de arco)
- Rango temporal: 13000 BCE a 17000 CE
- Sistema: Geocéntrico, Zodíaco Tropical

**Planetas Calculados**:
1. Sol
2. Luna
3. Mercurio
4. Venus
5. Marte
6. Júpiter
7. Saturno
8. Urano
9. Neptuno
10. Plutón

**Puntos Importantes**:
- Ascendente (ASC)
- Medio Cielo (MC)
- Descendente (DSC)
- Fondo del Cielo (IC)

**Casas Astrológicas**:
- Sistema Placidus (más utilizado en astrología occidental)
- 12 casas con cúspides precisas

**Aspectos Planetarios**:
- Conjunción (0°, orbe 8°)
- Oposición (180°, orbe 8°)
- Trígono (120°, orbe 8°)
- Cuadratura (90°, orbe 8°)
- Sextil (60°, orbe 6°)
- Quincuncio (150°, orbe 3°)
- Semisextil (30°, orbe 3°)

### Integración con IA

**Google Gemini Pro**:
- Modelo: `gemini-pro`
- Temperatura: 0.9 (creatividad alta)
- Interpretaciones personalizadas y detalladas
- Manejo de errores con reintentos automáticos

**Tipos de Interpretaciones**:
1. Carta natal completa (800+ palabras)
2. Posiciones planetarias (300-500 palabras)
3. Horóscopo diario (200-300 palabras)
4. Compatibilidad (500-700 palabras)
5. Tránsitos (400-600 palabras)

## Uso de la API

### 1. Calcular Posiciones Planetarias

```bash
POST /api/astrology/calculate
Authorization: Bearer <token>
Content-Type: application/json

{
  "date": "1990-05-15T14:30:00",
  "latitude": 19.4326,
  "longitude": -99.1332,
  "timezone": "America/Mexico_City"  // opcional
}
```

**Respuesta**:
```json
{
  "success": true,
  "positions": {
    "date": "1990-05-15T14:30:00-06:00",
    "location": {
      "latitude": 19.4326,
      "longitude": -99.1332
    },
    "positions": {
      "sun": {
        "name": "Sol",
        "sign": "Tauro",
        "position": "Tauro 24° 44' 15\"",
        "degrees": 24,
        "minutes": 44,
        "retrograde": false
      },
      // ... más planetas
    }
  }
}
```

### 2. Generar Carta Natal Completa

```bash
POST /api/astrology/birth-chart
Authorization: Bearer <token>
Content-Type: application/json

{
  "birth_date": "1990-05-15T14:30:00",
  "latitude": 19.4326,
  "longitude": -99.1332,
  "location_name": "Ciudad de México",
  "generate_interpretation": true  // opcional, default: true
}
```

**Respuesta**:
```json
{
  "success": true,
  "message": "Carta natal generada exitosamente",
  "reading": {
    "id": 1,
    "birth_date": "1990-05-15T14:30:00",
    "birth_location": {
      "latitude": 19.4326,
      "longitude": -99.1332,
      "timezone": "America/Mexico_City",
      "name": "Ciudad de México"
    },
    "summary": {
      "sun_sign": "Tauro",
      "moon_sign": "Acuario",
      "rising_sign": "Virgo"
    },
    "interpretation": "Interpretación completa generada por IA...",
    "chart_data": {
      "planets": { /* ... */ },
      "houses": { /* ... */ },
      "aspects": [ /* ... */ ],
      "summary": { /* ... */ }
    }
  }
}
```

### 3. Obtener Lecturas Guardadas

```bash
GET /api/astrology/readings?page=1&per_page=20
Authorization: Bearer <token>
```

### 4. Horóscopo Diario

```bash
POST /api/astrology/daily-horoscope
Authorization: Bearer <token>
Content-Type: application/json

{
  "sun_sign": "Tauro",
  "date": "2024-01-01"  // opcional
}
```

### 5. Análisis de Compatibilidad

```bash
POST /api/astrology/compatibility
Authorization: Bearer <token>
Content-Type: application/json

{
  "person1": {
    "sun_sign": "Tauro",
    "moon_sign": "Acuario",
    "rising_sign": "Virgo"
  },
  "person2": {
    "sun_sign": "Escorpio",
    "moon_sign": "Piscis",
    "rising_sign": "Cáncer"
  }
}
```

## Configuración

### Variables de Entorno

Crear archivo `.env` basado en `.env.example`:

```bash
# Gemini API (requerido para interpretaciones)
GEMINI_API_KEY=your-gemini-api-key-here
```

Para obtener una clave API de Gemini:
1. Visitar: https://makersuite.google.com/app/apikey
2. Crear un nuevo proyecto o usar uno existente
3. Generar clave API
4. Copiar la clave al archivo `.env`

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### Inicializar Base de Datos

```bash
python3 init_db.py
```

## Pruebas

### Prueba Manual de Cálculos

```bash
python3 astrology_calculator.py
```

Esto ejecutará una prueba con fecha conocida (1 de enero de 2000) y mostrará:
- Posiciones planetarias
- Puntos importantes (ASC, MC)
- Resumen (signos, elementos, modalidades)
- Aspectos principales

### Prueba de API Completa

```bash
python3 test_astrology_api.py
```

Esto probará:
1. Registro de usuario
2. Endpoint de información
3. Cálculo de posiciones planetarias
4. Generación de carta natal
5. Obtención de lecturas guardadas

### Prueba con Gemini Service

```bash
# Configurar GEMINI_API_KEY primero
export GEMINI_API_KEY="your-key-here"

python3 gemini_service.py
```

## Ejemplo de Uso Completo

```python
from astrology_calculator import AstrologyCalculator
from gemini_service import GeminiService
from datetime import datetime
import pytz

# Inicializar calculadora
calc = AstrologyCalculator()

# Datos de nacimiento
birth_date = datetime(1990, 5, 15, 14, 30, 0, tzinfo=pytz.UTC)
latitude = 19.4326  # Ciudad de México
longitude = -99.1332

# Calcular carta natal
chart = calc.calculate_birth_chart(birth_date, latitude, longitude)

# Mostrar resumen
print(f"Signo Solar: {chart['summary']['sun_sign']}")
print(f"Signo Lunar: {chart['summary']['moon_sign']}")
print(f"Ascendente: {chart['summary']['rising_sign']}")

# Generar interpretación con IA (requiere GEMINI_API_KEY)
gemini = GeminiService()
interpretation = gemini.generate_birth_chart_interpretation(chart)
print(interpretation)
```

## Validación de Resultados

Los cálculos han sido validados contra:
- Astro.com (https://www.astro.com)
- AstroSeek (https://www.astroseek.com)
- Fecha de prueba: 1 de enero de 2000, 00:00 UTC, Ciudad de México

**Resultados Verificados**:
- Sol: Capricornio 9° 51' ✓
- Luna: Escorpio 7° 17' ✓
- Ascendente: Cáncer 8° 44' ✓
- Saturno retrógrado ✓

## Limitaciones y Consideraciones

1. **Gemini API**: Requiere clave API válida para interpretaciones
2. **Rate Limiting**: Gemini tiene límites de uso (60 requests/minuto)
3. **Precisión**: Swiss Ephemeris es extremadamente preciso pero requiere datos de entrada correctos
4. **Zona Horaria**: Es crucial proporcionar la zona horaria correcta o coordenadas precisas
5. **Usuarios Gratuitos**: Limitados a 2 lecturas astrológicas por día (configurable)

## Próximas Mejoras Sugeridas

1. **Tránsitos Planetarios**: Calcular tránsitos actuales sobre carta natal
2. **Progresiones**: Implementar progresiones secundarias
3. **Sinastría**: Análisis detallado de compatibilidad entre dos cartas
4. **Revolución Solar**: Carta para cumpleaños
5. **Nodos Lunares**: Incluir Nodo Norte y Sur
6. **Asteroides**: Agregar Quirón, Lilith, etc.
7. **Casas Derivadas**: Análisis de casas derivadas
8. **Aspectos Menores**: Quintil, biquintil, etc.
9. **Estrellas Fijas**: Conjunciones con estrellas fijas importantes
10. **Exportar PDF**: Generar PDF de la carta natal con gráfico

## Soporte y Documentación

- **Swiss Ephemeris**: https://www.astro.com/swisseph/
- **Gemini API**: https://ai.google.dev/docs
- **Astrología Básica**: https://www.astro.com/astrology/in_intro_e.htm

## Autor

Implementado como parte del Issue #3: [Astrología] Implementar cálculos precisos de posiciones planetarias

## Licencia

Este módulo utiliza Swiss Ephemeris que está disponible bajo licencia GPL o comercial.
Para uso comercial, consultar: https://www.astro.com/swisseph/swephinfo_e.htm
