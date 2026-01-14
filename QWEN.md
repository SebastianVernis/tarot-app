# 🎯 QWEN.md - tarot-app

## 📋 Información General

| Campo | Valor |
|-------|-------|
| **Nombre del Proyecto** | tarot-app |
| **Versión** | 1.0.0 |
| **Estado** | ✅ PRODUCCIÓN |
| **Tipo** | Aplicación Web Interactiva |
| **Categoría** | Sistema de Lectura de Tarot |
| **Fecha de Análisis** | 2026-01-09 |

---

## 🎯 Propósito del Proyecto

Sistema de lectura de tarot con 78 cartas, 9 tipos de tiradas, múltiples fuentes de aleatoriedad (crypto, cuántica simulada) y verificación estadística (>90% calidad). Interfaz web mística con historial de lecturas.

**Filosofía:** "Aleatoriedad verificada para lecturas auténticas"

---

## 🏗️ Arquitectura Técnica

### Stack Tecnológico

**Backend:**
- Python 3.8+
- Flask (Web framework)
- secrets (Crypto random)
- hashlib (Hashing)

**Frontend:**
- HTML5/CSS3/JavaScript
- Vanilla JS (Sin frameworks)
- CSS Animations
- LocalStorage (Historial)

**Aleatoriedad:**
- secrets.SystemRandom (Crypto)
- Cuántica simulada (Algoritmo propietario)
- Verificación estadística
- Chi-squared test

**Deployment:**
- Flask development server
- Puerto 5000 (default)
- Hosting simple (VPS, PythonAnywhere)

---

## ✨ Características Principales

### 1. 78 Cartas Completas

**22 Arcanos Mayores:**
- El Loco, El Mago, La Sacerdotisa, La Emperatriz, El Emperador
- El Hierofante, Los Enamorados, El Carro, La Fuerza, El Ermitaño
- La Rueda de la Fortuna, La Justicia, El Colgado, La Muerte
- La Templanza, El Diablo, La Torre, La Estrella, La Luna
- El Sol, El Juicio, El Mundo

**56 Arcanos Menores:**
- **Bastos** (14 cartas): As-10, Sota, Caballero, Reina, Rey
- **Copas** (14 cartas): As-10, Sota, Caballero, Reina, Rey
- **Espadas** (14 cartas): As-10, Sota, Caballero, Reina, Rey
- **Oros** (14 cartas): As-10, Sota, Caballero, Reina, Rey

### 2. 9 Tipos de Tiradas

1. **Tirada de 1 Carta** - Respuesta rápida
2. **Tirada de 3 Cartas** - Pasado, Presente, Futuro
3. **Cruz Celta** (10 cartas) - Análisis completo
4. **Herradura** (7 cartas) - Situación específica
5. **Estrella de 7 Puntas** - Chakras y energía
6. **Árbol de la Vida** (10 cartas) - Kabbalah
7. **Tirada del Sí/No** - Respuesta directa
8. **Tirada del Amor** (5 cartas) - Relaciones
9. **Tirada Personalizada** - Configuración libre

### 3. Múltiples Fuentes de Aleatoriedad

**Nivel 1: Crypto Random**
```python
import secrets
card = secrets.choice(deck)
```

**Nivel 2: Cuántica Simulada**
```python
# Algoritmo propietario
# Simula comportamiento cuántico
# Basado en timestamp + entropy
```

**Nivel 3: Híbrido**
```python
# Combina crypto + cuántica
# Máxima aleatoriedad
# Verificación estadística
```

### 4. Verificación Estadística (>90% Calidad)
- Chi-squared test
- Distribución uniforme
- Independencia de eventos
- Reporte de calidad

### 5. Interfaz Web Mística
- Diseño oscuro y místico
- Animaciones de cartas
- Efectos de volteo
- Sonidos (opcional)
- Responsive design

### 6. Historial de Lecturas
- Guardado en LocalStorage
- Fecha y hora
- Tipo de tirada
- Cartas obtenidas
- Interpretación
- Exportar/Importar

---

## 📂 Estructura del Proyecto

```
tarot-app/
├── app.py                     # Flask application
├── tarot/
│   ├── __init__.py
│   ├── cards.py               # Definición de cartas
│   ├── spreads.py             # Tipos de tiradas
│   ├── randomness.py          # Fuentes de aleatoriedad
│   └── interpretation.py      # Interpretaciones
├── static/
│   ├── css/
│   │   ├── main.css
│   │   └── cards.css
│   ├── js/
│   │   ├── app.js
│   │   ├── cards.js
│   │   └── history.js
│   ├── images/
│   │   └── cards/             # 78 imágenes de cartas
│   └── sounds/                # Efectos de sonido
├── templates/
│   ├── index.html
│   ├── reading.html
│   └── history.html
├── tests/
│   ├── test_randomness.py
│   └── test_spreads.py
└── requirements.txt
```

---

## 🚀 Deployment

### Desarrollo
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py

# Acceder
http://localhost:5000
```

### Producción (PythonAnywhere)
```bash
# Upload files
# Configure WSGI
# Set Python version 3.8+
# Reload web app
```

### Producción (VPS)
```bash
# Usar Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# O con systemd service
sudo systemctl start tarot-app
```

---

## 🔧 Configuración

### Variables de Entorno

```bash
# Flask
FLASK_APP="app.py"
FLASK_ENV="production"
SECRET_KEY="tu_secret_key_aqui"

# Tarot
RANDOMNESS_SOURCE="hybrid"  # crypto, quantum, hybrid
ENABLE_SOUNDS="true"
ENABLE_HISTORY="true"
MAX_HISTORY_ITEMS="100"
```

### Configuración de Cartas

```python
# tarot/cards.py
CARDS = {
    'major_arcana': [...],  # 22 cartas
    'minor_arcana': {
        'wands': [...],     # 14 cartas
        'cups': [...],      # 14 cartas
        'swords': [...],    # 14 cartas
        'pentacles': [...]  # 14 cartas
    }
}
```

---

## 📊 Métricas del Proyecto

### Contenido
- **Cartas Totales:** 78
- **Arcanos Mayores:** 22
- **Arcanos Menores:** 56
- **Tipos de Tiradas:** 9
- **Interpretaciones:** 78+ (por carta)

### Calidad de Aleatoriedad
- **Chi-squared Test:** >90% pass
- **Distribución:** Uniforme verificada
- **Independencia:** Verificada
- **Entropía:** Alta

### Performance
- **Respuesta:** <100ms
- **Generación de Tirada:** <50ms
- **Carga de Imágenes:** Lazy loading
- **Tamaño Total:** ~10MB (con imágenes)

---

## 🎮 Funcionalidades Principales

### Para Usuarios
1. **Realizar Lectura**
   - Seleccionar tipo de tirada
   - Mezclar cartas (animación)
   - Seleccionar cartas
   - Ver interpretación

2. **Historial**
   - Ver lecturas pasadas
   - Filtrar por fecha
   - Exportar a JSON
   - Importar lecturas

3. **Configuración**
   - Fuente de aleatoriedad
   - Sonidos on/off
   - Tema (claro/oscuro)
   - Idioma (ES/EN)

### Para Desarrolladores
- API REST (futuro)
- Código fuente abierto
- Tests de aleatoriedad
- Fácil de extender

---

## 📚 Documentación Disponible

### Técnica
- README.md
- Documentación de API (futuro)
- Tests de aleatoriedad
- Comentarios en código

### Usuario
- Guía de uso
- Significado de cartas
- Tipos de tiradas
- FAQ

---

## 🔗 Enlaces y Recursos

- **Producción:** http://localhost:5000
- **Repositorio:** (Local)
- **Licencia:** MIT

---

## ⚠️ Notas Importantes

### Dependencias Críticas
- Python 3.8+ requerido
- Flask para servidor
- secrets module (built-in)

### Limitaciones
- Historial en LocalStorage (límite del navegador)
- Imágenes de cartas (10MB total)
- Sin backend de usuarios (futuro)

### Disclaimer
**Este sistema es para entretenimiento y reflexión personal.**
- No sustituye asesoría profesional
- Interpretaciones son generales
- Aleatoriedad verificada pero no "mágica"

---

## 🎯 Estado del Proyecto

| Aspecto | Estado | Notas |
|---------|--------|-------|
| **Desarrollo** | ✅ Completo | v1.0.0 estable |
| **Testing** | ✅ Completo | Tests de aleatoriedad |
| **Documentación** | ✅ Completa | README detallado |
| **Producción** | ✅ Ready | Funcional |
| **Mantenimiento** | 🟢 Activo | Estable |

---

## 🔄 Relación con Otros Proyectos

**Proyectos Relacionados:** Ninguno (único en el portfolio)

**Tecnologías Compartidas:**
- Python (con Bet-Copilot, Numeros_Primos)
- Flask (con Numeros_Primos)
- Vanilla JS (con DragNDrop, vanilla-editor)
- LocalStorage (con varios proyectos frontend)

**Diferenciadores:**
- Único sistema de tarot
- Único con aleatoriedad cuántica simulada
- Único con verificación estadística
- Único con 9 tipos de tiradas
- Único enfocado en misticismo

---

## 📈 Próximos Pasos / Roadmap

- [ ] Sistema de usuarios (registro/login)
- [ ] Compartir lecturas (social)
- [ ] Más tipos de tiradas (15+ total)
- [ ] Interpretaciones personalizadas con IA
- [ ] App móvil nativa (iOS/Android)
- [ ] Modo offline completo (PWA)
- [ ] Consultas con tarotistas reales
- [ ] Comunidad de usuarios
- [ ] Diario de tarot
- [ ] Estadísticas personales
- [ ] Integración con calendario lunar
- [ ] Realidad aumentada (AR cards)
- [ ] Multiplayer (lecturas grupales)

---

**Última Actualización:** 2026-01-09  
**Analizado por:** Blackbox AI  
**Versión QWEN:** 1.0
