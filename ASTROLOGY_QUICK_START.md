# 🚀 Guía Rápida: API de Astrología

## Inicio Rápido

### 1. Configuración Inicial

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar Gemini API (opcional pero recomendado)
echo "GEMINI_API_KEY=tu-clave-aqui" >> .env

# Inicializar base de datos
python3 init_db.py

# Iniciar servidor
python3 app.py
```

### 2. Obtener Token de Autenticación

```bash
# Registrar usuario
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "username": "usuario",
    "password": "password123"
  }'

# Guardar el access_token de la respuesta
```

### 3. Calcular Carta Natal

```bash
# Reemplazar YOUR_TOKEN con el token obtenido
curl -X POST http://localhost:5000/api/astrology/birth-chart \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "birth_date": "1990-05-15T14:30:00",
    "latitude": 19.4326,
    "longitude": -99.1332,
    "location_name": "Ciudad de México",
    "generate_interpretation": true
  }'
```

## Ejemplos de Uso

### Ejemplo 1: Solo Posiciones Planetarias

```bash
curl -X POST http://localhost:5000/api/astrology/calculate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "date": "2000-01-01T00:00:00",
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

### Ejemplo 2: Carta Natal Sin Interpretación IA

```bash
curl -X POST http://localhost:5000/api/astrology/birth-chart \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "birth_date": "1985-03-20T10:00:00",
    "latitude": 51.5074,
    "longitude": -0.1278,
    "location_name": "Londres",
    "generate_interpretation": false
  }'
```

### Ejemplo 3: Horóscopo Diario

```bash
curl -X POST http://localhost:5000/api/astrology/daily-horoscope \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "sun_sign": "Aries",
    "date": "2024-01-15"
  }'
```

### Ejemplo 4: Compatibilidad

```bash
curl -X POST http://localhost:5000/api/astrology/compatibility \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "person1": {
      "sun_sign": "Aries",
      "moon_sign": "Leo",
      "rising_sign": "Sagitario"
    },
    "person2": {
      "sun_sign": "Libra",
      "moon_sign": "Acuario",
      "rising_sign": "Géminis"
    }
  }'
```

## Coordenadas de Ciudades Comunes

| Ciudad | Latitud | Longitud |
|--------|---------|----------|
| Ciudad de México | 19.4326 | -99.1332 |
| Buenos Aires | -34.6037 | -58.3816 |
| Madrid | 40.4168 | -3.7038 |
| Barcelona | 41.3851 | 2.1734 |
| Bogotá | 4.7110 | -74.0721 |
| Lima | -12.0464 | -77.0428 |
| Santiago | -33.4489 | -70.6693 |
| Caracas | 10.4806 | -66.9036 |
| Miami | 25.7617 | -80.1918 |
| Los Ángeles | 34.0522 | -118.2437 |
| Nueva York | 40.7128 | -74.0060 |
| Londres | 51.5074 | -0.1278 |
| París | 48.8566 | 2.3522 |
| Roma | 41.9028 | 12.4964 |
| Tokio | 35.6762 | 139.6503 |

## Signos Zodiacales

| Signo | Fechas Aproximadas | Elemento | Modalidad |
|-------|-------------------|----------|-----------|
| Aries | 21 Mar - 19 Abr | Fuego | Cardinal |
| Tauro | 20 Abr - 20 May | Tierra | Fijo |
| Géminis | 21 May - 20 Jun | Aire | Mutable |
| Cáncer | 21 Jun - 22 Jul | Agua | Cardinal |
| Leo | 23 Jul - 22 Ago | Fuego | Fijo |
| Virgo | 23 Ago - 22 Sep | Tierra | Mutable |
| Libra | 23 Sep - 22 Oct | Aire | Cardinal |
| Escorpio | 23 Oct - 21 Nov | Agua | Fijo |
| Sagitario | 22 Nov - 21 Dic | Fuego | Mutable |
| Capricornio | 22 Dic - 19 Ene | Tierra | Cardinal |
| Acuario | 20 Ene - 18 Feb | Aire | Fijo |
| Piscis | 19 Feb - 20 Mar | Agua | Mutable |

## Formato de Fechas

La API acepta fechas en formato ISO 8601:

```
YYYY-MM-DDTHH:MM:SS
```

Ejemplos:
- `2000-01-01T00:00:00` - 1 de enero de 2000, medianoche
- `1990-05-15T14:30:00` - 15 de mayo de 1990, 2:30 PM
- `1985-12-25T08:45:00` - 25 de diciembre de 1985, 8:45 AM

## Códigos de Respuesta

| Código | Significado |
|--------|-------------|
| 200 | Éxito |
| 201 | Creado exitosamente |
| 400 | Solicitud inválida |
| 401 | No autorizado (token inválido) |
| 403 | Prohibido (límite alcanzado) |
| 404 | No encontrado |
| 500 | Error del servidor |

## Solución de Problemas

### Error: "Missing Authorization Header"
**Solución**: Incluir el header `Authorization: Bearer YOUR_TOKEN`

### Error: "Subject must be a string"
**Solución**: Reiniciar el servidor después de actualizar el código

### Error: "Servicio de interpretación no configurado"
**Solución**: Configurar `GEMINI_API_KEY` en el archivo `.env`

### Error: "Formato de fecha inválido"
**Solución**: Usar formato ISO 8601: `YYYY-MM-DDTHH:MM:SS`

### Error: "Latitud y longitud requeridas"
**Solución**: Proporcionar coordenadas válidas (-90 a 90 para latitud, -180 a 180 para longitud)

## Pruebas Automatizadas

```bash
# Ejecutar suite de pruebas
python3 test_astrology_api.py

# Probar solo cálculos
python3 astrology_calculator.py

# Probar Gemini (requiere API key)
python3 gemini_service.py
```

## Recursos Adicionales

- **Documentación Completa**: Ver `ASTROLOGY_IMPLEMENTATION.md`
- **Obtener Coordenadas**: https://www.latlong.net/
- **Gemini API Key**: https://makersuite.google.com/app/apikey
- **Swiss Ephemeris**: https://www.astro.com/swisseph/

## Soporte

Para reportar problemas o sugerencias, crear un issue en el repositorio.
