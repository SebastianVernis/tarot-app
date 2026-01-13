# 🚀 PENDIENTES PARA DESPLIEGUE COMPLETO

**Fecha:** 13 de enero de 2026  
**Estado:** ✅ Proyecto analizado y listo para acción

---

## ✅ COMPLETADO

- [x] Análisis completo del proyecto
- [x] Validación de sintaxis Python
- [x] Verificación de estructura de archivos
- [x] Revisión de configuración de Vercel
- [x] Creación de .gitignore
- [x] Documentación de análisis completo

---

## 🔴 CRÍTICO - HACER AHORA (15-30 minutos)

### 1. Limpiar archivos de cache de Git

```bash
# Eliminar directorios __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Agregar .gitignore al repositorio
git add .gitignore

# Commit
git commit -m "Add .gitignore and clean cache files"
```

### 2. Configurar Variables de Entorno en Vercel

```bash
# Login a Vercel
vercel login

# Agregar variables de entorno
vercel env add SECRET_KEY
# Cuando pregunte, pegar: (generar con: python3 -c "import secrets; print(secrets.token_urlsafe(32))")

vercel env add JWT_SECRET_KEY
# Cuando pregunte, pegar: (generar con: python3 -c "import secrets; print(secrets.token_urlsafe(32))")

vercel env add GEMINI_API_KEY
# Cuando pregunte, pegar tu API key de Google AI Studio
# Obtener en: https://makersuite.google.com/app/apikey
```

### 3. Desplegar a Vercel

```bash
# Desplegar a producción
vercel --prod

# Esperar a que termine el despliegue
# Vercel mostrará la URL de tu aplicación
```

### 4. Verificar Despliegue

```bash
# Reemplazar YOUR_APP_URL con tu URL de Vercel
export APP_URL="https://tu-app.vercel.app"

# Health check
curl $APP_URL/api/health

# Debería responder:
# {
#   "status": "healthy",
#   "service": "Tarot Místico API",
#   "version": "2.0.0",
#   ...
# }

# API info
curl $APP_URL/api/info

# Abrir en navegador
open $APP_URL
```

---

## 🟡 IMPORTANTE - HACER ESTA SEMANA (1-2 horas)

### 5. Configurar Base de Datos PostgreSQL

**⚠️ IMPORTANTE:** Sin esto, los datos no persisten entre despliegues.

**Opción A: Vercel Postgres (Recomendado)**

1. Ir a tu proyecto en Vercel Dashboard
2. Ir a la pestaña "Storage"
3. Click en "Create Database"
4. Seleccionar "Postgres"
5. Seguir el wizard
6. Copiar el `DATABASE_URL` que te proporciona
7. Agregar a variables de entorno:
   ```bash
   vercel env add DATABASE_URL
   # Pegar el URL de PostgreSQL
   ```
8. Redesplegar:
   ```bash
   vercel --prod
   ```

**Opción B: Supabase (Gratis)**

1. Ir a https://supabase.com
2. Crear cuenta y proyecto
3. Ir a Settings > Database
4. Copiar "Connection string" (URI)
5. Agregar a Vercel:
   ```bash
   vercel env add DATABASE_URL
   # Pegar: postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
   ```
6. Redesplegar:
   ```bash
   vercel --prod
   ```

**Opción C: Railway (Gratis)**

1. Ir a https://railway.app
2. Crear cuenta
3. New Project > Provision PostgreSQL
4. Copiar "Postgres Connection URL"
5. Agregar a Vercel:
   ```bash
   vercel env add DATABASE_URL
   ```
6. Redesplegar

### 6. Verificar Funcionalidad Completa

```bash
# Test de registro
curl -X POST $APP_URL/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "Test123456"
  }'

# Test de login
curl -X POST $APP_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456"
  }'

# Guardar el token que devuelve
export TOKEN="<access_token_aqui>"

# Test de lectura de tarot
curl -X POST $APP_URL/api/readings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "spread_type": "una_carta",
    "question": "¿Qué me depara el día de hoy?",
    "cards": [{"name": "El Loco", "position": "upright"}],
    "interpretation": "Nueva aventura te espera"
  }'
```

### 7. Decidir sobre Funcionalidad de Astrología

**Opción A: Habilitar Astrología Completa**

```bash
# Editar requirements.txt
echo "pyswisseph==2.10.3.2" >> requirements.txt

# Commit y push
git add requirements.txt
git commit -m "Add pyswisseph for full astrology support"
git push

# Redesplegar
vercel --prod
```

**Nota:** Esto agregará ~20-30 MB al tamaño del despliegue.

**Opción B: Deshabilitar Astrología Temporalmente**

```bash
# Editar config.py
# Cambiar: ASTROLOGY_ENABLED = True
# Por:     ASTROLOGY_ENABLED = False

# O agregar variable de entorno
vercel env add ASTROLOGY_ENABLED
# Valor: false

# Redesplegar
vercel --prod
```

---

## 🟢 OPCIONAL - MEJORAS DE PRODUCCIÓN (4-8 horas)

### 8. Implementar Rate Limiting

```bash
# Agregar a requirements.txt
echo "Flask-Limiter==3.5.0" >> requirements.txt

# Editar api/index.py para configurar limiter
# Ver documentación: https://flask-limiter.readthedocs.io/

git add requirements.txt api/index.py
git commit -m "Add rate limiting"
vercel --prod
```

### 9. Configurar Monitoreo con Sentry

```bash
# Agregar a requirements.txt
echo "sentry-sdk[flask]==1.40.0" >> requirements.txt

# Crear cuenta en sentry.io
# Obtener DSN

# Agregar a Vercel
vercel env add SENTRY_DSN

# Editar api/index.py para inicializar Sentry
# Ver: https://docs.sentry.io/platforms/python/guides/flask/

git add requirements.txt api/index.py
git commit -m "Add Sentry error tracking"
vercel --prod
```

### 10. Agregar Documentación de API (Swagger)

```bash
# Agregar a requirements.txt
echo "flasgger==0.9.7.1" >> requirements.txt

# Editar api/index.py para configurar Swagger
# Ver: https://github.com/flasgger/flasgger

git add requirements.txt api/index.py
git commit -m "Add Swagger API documentation"
vercel --prod

# Acceder a: https://tu-app.vercel.app/apidocs
```

### 11. Crear Tests Básicos

```bash
# Crear directorio de tests
mkdir -p tests

# Agregar pytest
echo "pytest==7.4.3" >> requirements.txt
echo "pytest-flask==1.3.0" >> requirements.txt

# Crear test básico
cat > tests/test_health.py << 'EOF'
def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
EOF

# Crear conftest.py
cat > tests/conftest.py << 'EOF'
import pytest
from api.index import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
EOF

# Ejecutar tests
pytest tests/

git add tests/ requirements.txt
git commit -m "Add basic tests"
```

### 12. Configurar CI/CD con GitHub Actions

```bash
# Crear directorio de workflows
mkdir -p .github/workflows

# Crear workflow de tests
cat > .github/workflows/test.yml << 'EOF'
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/
EOF

git add .github/
git commit -m "Add GitHub Actions CI"
git push
```

---

## 📋 CHECKLIST COMPLETO

### Pre-Despliegue

- [x] Código sin errores de sintaxis
- [x] Estructura de proyecto organizada
- [x] vercel.json configurado
- [x] requirements.txt optimizado
- [x] Documentación presente
- [x] .gitignore creado
- [ ] Variables de entorno configuradas en Vercel
- [ ] Gemini API key obtenida
- [ ] Base de datos de producción decidida

### Despliegue Inicial

- [ ] `vercel --prod` ejecutado
- [ ] Health check responde
- [ ] API info endpoint funciona
- [ ] Frontend carga
- [ ] Logs de Vercel revisados

### Funcionalidad Básica

- [ ] Registro de usuarios funciona
- [ ] Login funciona
- [ ] Lecturas de tarot funcionan
- [ ] Interpretaciones con IA funcionan (si GEMINI_API_KEY configurada)
- [ ] Sistema freemium funciona

### Base de Datos

- [ ] PostgreSQL configurado
- [ ] DATABASE_URL en Vercel
- [ ] Persistencia de datos verificada
- [ ] Usuarios persisten entre despliegues
- [ ] Lecturas persisten

### Astrología (Opcional)

- [ ] Decisión tomada (habilitar/deshabilitar)
- [ ] Si habilitada: pyswisseph agregado
- [ ] Cálculos de cartas natales funcionan
- [ ] Interpretaciones astrológicas funcionan

### Producción (Opcional)

- [ ] Rate limiting implementado
- [ ] Monitoreo de errores activo (Sentry)
- [ ] Documentación de API (Swagger)
- [ ] Tests básicos creados
- [ ] CI/CD configurado
- [ ] Dominio personalizado (opcional)

---

## 🎯 PRIORIDADES

### Prioridad 1 (CRÍTICO) - Hacer HOY

1. Limpiar cache de git
2. Configurar variables de entorno
3. Desplegar a Vercel
4. Verificar health check

**Tiempo:** 30 minutos  
**Resultado:** Aplicación desplegada y funcionando básicamente

### Prioridad 2 (IMPORTANTE) - Hacer ESTA SEMANA

1. Configurar PostgreSQL
2. Verificar funcionalidad completa
3. Decidir sobre astrología

**Tiempo:** 2-3 horas  
**Resultado:** Aplicación completamente funcional con persistencia

### Prioridad 3 (MEJORAS) - Hacer ESTE MES

1. Rate limiting
2. Monitoreo
3. Documentación API
4. Tests

**Tiempo:** 8-12 horas  
**Resultado:** Aplicación production-ready con calidad profesional

---

## 🆘 TROUBLESHOOTING

### Error: "Module not found"

```bash
# Verificar que todas las dependencias estén en requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
vercel --prod
```

### Error: "Database connection failed"

```bash
# Verificar DATABASE_URL
vercel env ls

# Si no está configurada
vercel env add DATABASE_URL

# Redesplegar
vercel --prod
```

### Error: "GEMINI_API_KEY not configured"

```bash
# Agregar API key
vercel env add GEMINI_API_KEY

# Redesplegar
vercel --prod
```

### Error: "Function timeout"

```bash
# Aumentar timeout en vercel.json
# "maxDuration": 30  ->  "maxDuration": 60

git add vercel.json
git commit -m "Increase function timeout"
vercel --prod
```

### Ver logs de errores

```bash
# Logs en tiempo real
vercel logs --follow

# Logs de función específica
vercel logs api/index.py

# Logs con filtro
vercel logs --since 1h
```

---

## 📞 RECURSOS

- **Documentación del proyecto:** `README.md`
- **Análisis completo:** `ANALISIS_PROYECTO.md`
- **Guía de despliegue:** `DEPLOYMENT.md`
- **Estado del despliegue:** `DEPLOYMENT_STATUS.md`
- **Validación:** `python3 validate.py`
- **Logs de Vercel:** `vercel logs`

---

## ✅ COMANDOS RÁPIDOS

```bash
# Generar secret keys
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Limpiar cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Desplegar
vercel --prod

# Ver logs
vercel logs --follow

# Health check
curl https://tu-app.vercel.app/api/health

# Test completo
./validate.py
```

---

**¡Éxito con el despliegue!** 🚀🔮

Si tienes problemas, revisa:
1. `ANALISIS_PROYECTO.md` - Análisis completo
2. `vercel logs` - Logs de errores
3. `python3 validate.py` - Validación local
