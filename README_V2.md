# 🔮 Sistema de Tarot Místico v2.0

> Sistema completo de lectura de tarot con autenticación, persistencia de sesiones y plan freemium

## 🆕 Nuevas Características

### ✨ Sistema de Autenticación
- **Login/Registro** con JWT
- **Sesiones persistentes** en múltiples dispositivos
- **Refresh tokens** automático
- **Recuperación de contraseña** (próximamente)

### 🎨 Persistencia de Temas
- **Tema claro/oscuro** con toggle
- **Sincronización** entre dispositivos
- **Guardado automático** en backend y localStorage
- **CSS variables** para transiciones suaves

### 💎 Sistema Freemium

#### Plan Gratuito
- ✅ 3 lecturas diarias
- ✅ Tiradas básicas (1 carta, 3 cartas)
- ✅ Historial limitado (últimas 10 lecturas)
- ✅ Interpretaciones básicas

#### Plan Premium ($9.99/mes)
- ✨ Lecturas ilimitadas
- ✨ Todas las tiradas disponibles
- ✨ Historial completo
- ✨ Interpretaciones detalladas
- ✨ Sin anuncios
- ✨ Exportar lecturas en PDF
- ✨ Soporte prioritario

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip
- Navegador web moderno

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
nano .env
```

### 3. Inicializar Base de Datos

```bash
python init_db.py
```

Esto creará:
- Base de datos SQLite (`tarot.db`)
- Tablas necesarias
- Usuarios de prueba:
  - **Gratuito**: `demo@tarot.com` / `demo123`
  - **Premium**: `premium@tarot.com` / `premium123`

### 4. Iniciar el Servidor

```bash
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

### 5. Abrir la Aplicación

Abre tu navegador y ve a: `http://localhost:5000/tarot_web_v2.html`

## 📁 Estructura del Proyecto

```
tarot-app/
├── app.py                      # Aplicación Flask principal
├── config.py                   # Configuración
├── models.py                   # Modelos de base de datos
├── auth.py                     # Sistema de autenticación JWT
├── middleware.py               # Middleware freemium
├── init_db.py                  # Script de inicialización
│
├── routes/                     # Endpoints REST
│   ├── auth_routes.py         # Login, registro, logout
│   ├── user_routes.py         # Perfil, configuraciones
│   ├── reading_routes.py      # Lecturas de tarot
│   └── subscription_routes.py # Gestión de suscripciones
│
├── tarot_web_v2.html          # Frontend mejorado
├── tarot_web_v2.js            # JavaScript con integración API
│
├── tarot_reader_enhanced.py   # Lector de tarot (CLI)
├── tarot_quantum_random.py    # Generador cuántico
├── tarot_randomness_test.py   # Suite de pruebas
│
├── requirements.txt           # Dependencias Python
├── .env.example              # Ejemplo de configuración
└── README_V2.md              # Este archivo
```

## 🔌 API Endpoints

### Autenticación (`/api/auth`)
- `POST /register` - Registrar nuevo usuario
- `POST /login` - Iniciar sesión
- `POST /refresh` - Refrescar token
- `GET /me` - Obtener usuario actual
- `POST /logout` - Cerrar sesión
- `POST /change-password` - Cambiar contraseña

### Usuario (`/api/user`)
- `GET /profile` - Obtener perfil completo
- `PUT /settings` - Actualizar configuraciones
- `PUT /theme` - Actualizar tema
- `GET /usage` - Obtener estadísticas de uso
- `GET /stats` - Estadísticas detalladas

### Lecturas (`/api/readings`)
- `POST /` - Crear nueva lectura
- `GET /` - Obtener todas las lecturas (paginado)
- `GET /:id` - Obtener lectura específica
- `PUT /:id` - Actualizar lectura
- `DELETE /:id` - Eliminar lectura
- `POST /:id/favorite` - Marcar como favorita
- `POST /check-access` - Verificar acceso a lectura

### Suscripciones (`/api/subscription`)
- `GET /plans` - Obtener planes disponibles
- `GET /current` - Suscripción actual
- `POST /upgrade` - Actualizar a premium
- `POST /cancel` - Cancelar suscripción
- `GET /history` - Historial de suscripciones
- `POST /demo-upgrade` - Upgrade demo (desarrollo)

## 🧪 Testing

### Probar la API

```bash
# Health check
curl http://localhost:5000/api/health

# Registrar usuario
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"test123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# Obtener perfil (requiere token)
curl http://localhost:5000/api/user/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Probar el Frontend

1. Abrir `http://localhost:5000/tarot_web_v2.html`
2. Hacer clic en "Registrarse"
3. Crear una cuenta
4. Probar cambio de tema
5. Seleccionar una tirada
6. Realizar una lectura
7. Verificar límites freemium

### Probar Upgrade a Premium

```bash
# Usando el endpoint de demo
curl -X POST http://localhost:5000/api/subscription/demo-upgrade \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🎮 Uso

### Como Usuario Gratuito

1. **Registrarse** o usar cuenta demo: `demo@tarot.com` / `demo123`
2. **Cambiar tema** con el toggle en el header
3. **Seleccionar tirada** (solo básicas disponibles)
4. **Realizar lectura** (máximo 3 por día)
5. **Ver historial** limitado

### Como Usuario Premium

1. **Registrarse** o usar cuenta premium: `premium@tarot.com` / `premium123`
2. **Acceso completo** a todas las tiradas
3. **Lecturas ilimitadas**
4. **Historial completo**
5. **Funciones avanzadas**

### Actualizar a Premium

1. Hacer clic en el botón de usuario
2. Seleccionar "Actualizar a Premium"
3. En desarrollo: usar endpoint demo
4. En producción: integrar con Stripe/PayPal

## 🔒 Seguridad

- **Contraseñas hasheadas** con Werkzeug
- **JWT tokens** con expiración
- **Refresh tokens** para sesiones largas
- **CORS configurado** para dominios permitidos
- **Validación de entrada** en todos los endpoints
- **Rate limiting** (próximamente)

## 🌐 Despliegue

### Desarrollo
```bash
FLASK_ENV=development python app.py
```

### Producción

1. **Configurar variables de entorno**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret
   export JWT_SECRET_KEY=your-jwt-secret
   ```

2. **Usar servidor WSGI**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Configurar base de datos PostgreSQL**
   ```bash
   export DATABASE_URL=postgresql://user:pass@localhost/tarot
   ```

4. **Configurar procesador de pagos**
   - Integrar Stripe o PayPal
   - Actualizar endpoint `/subscription/upgrade`

## 📊 Base de Datos

### Modelos

- **User**: Usuarios del sistema
- **Reading**: Lecturas de tarot
- **UsageLimit**: Límites de uso diario
- **Subscription**: Historial de suscripciones

### Migraciones

```bash
# Crear migración
flask db migrate -m "Descripción"

# Aplicar migración
flask db upgrade

# Revertir migración
flask db downgrade
```

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Database not found"
```bash
python init_db.py
```

### Error: "CORS policy"
- Verificar `CORS_ORIGINS` en `.env`
- Agregar tu dominio a la lista

### Error: "Token expired"
- El frontend debería refrescar automáticamente
- Si persiste, hacer logout y login nuevamente

## 🔄 Próximas Funcionalidades

- [ ] Recuperación de contraseña por email
- [ ] Integración con Stripe/PayPal
- [ ] Exportar lecturas a PDF
- [ ] Compartir lecturas en redes sociales
- [ ] Notificaciones push
- [ ] App móvil (React Native)
- [ ] Modo offline con Service Workers
- [ ] Análisis de patrones en lecturas
- [ ] Recomendaciones personalizadas

## 📝 Licencia

MIT License

## 🙏 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

---

*Que las cartas iluminen tu camino* ✨🔮
