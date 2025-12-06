# 🔮 Guía Rápida - Tarot Místico v2.0

## ✅ Sistema Implementado

Se ha implementado exitosamente un sistema completo de Tarot con:

### 🎯 Funcionalidades Principales

1. **✨ Sistema de Autenticación JWT**
   - Registro de usuarios
   - Login/Logout
   - Tokens de acceso y refresh
   - Sesiones persistentes

2. **🎨 Persistencia de Temas**
   - Toggle claro/oscuro
   - Guardado en localStorage
   - Sincronización con backend
   - CSS variables para transiciones suaves

3. **💎 Sistema Freemium**
   - **Plan Gratuito**: 3 lecturas/día, tiradas básicas
   - **Plan Premium**: Lecturas ilimitadas, todas las tiradas
   - Middleware de verificación de límites
   - Upgrade demo disponible

4. **📊 Gestión de Lecturas**
   - Crear lecturas de tarot
   - Historial completo
   - Marcar favoritas
   - Filtros y paginación

## 🚀 Inicio Rápido

### 1. El servidor ya está corriendo en:
```
http://localhost:5000
```

### 2. Acceder a la aplicación:
```
http://localhost:5000/tarot_web_v2.html
```

### 3. Usuarios de Prueba

#### Usuario Gratuito
- **Email**: demo@tarot.com
- **Password**: demo123
- **Plan**: Free (3 lecturas/día)

#### Usuario Premium
- **Email**: premium@tarot.com
- **Password**: premium123
- **Plan**: Premium (ilimitado)

## 📝 Cómo Usar

### Registro de Nuevo Usuario

1. Abrir `http://localhost:5000/tarot_web_v2.html`
2. Hacer clic en "Registrarse"
3. Completar el formulario
4. ¡Listo! Ya puedes usar la aplicación

### Cambiar Tema

1. Hacer clic en el toggle de tema en el header
2. El tema se guarda automáticamente
3. Se sincroniza entre dispositivos

### Realizar una Lectura

1. Iniciar sesión
2. Seleccionar tipo de tirada
3. Escribir pregunta (opcional)
4. Hacer clic en "Comenzar Lectura"
5. Ver resultados y estadísticas actualizadas

### Actualizar a Premium

1. Intentar acceder a una tirada bloqueada
2. Hacer clic en "Actualizar a Premium"
3. En desarrollo: se activa automáticamente (demo)
4. En producción: integrar con Stripe/PayPal

## 🔌 API Endpoints

### Autenticación
```bash
# Registro
POST /api/auth/register
Body: {"email": "...", "username": "...", "password": "..."}

# Login
POST /api/auth/login
Body: {"email": "...", "password": "..."}

# Obtener usuario actual
GET /api/auth/me
Headers: Authorization: Bearer <token>
```

### Usuario
```bash
# Obtener perfil
GET /api/user/profile
Headers: Authorization: Bearer <token>

# Cambiar tema
PUT /api/user/theme
Headers: Authorization: Bearer <token>
Body: {"theme": "light" | "dark"}

# Estadísticas de uso
GET /api/user/usage
Headers: Authorization: Bearer <token>
```

### Lecturas
```bash
# Crear lectura
POST /api/readings/
Headers: Authorization: Bearer <token>
Body: {"spread_type": "...", "question": "...", "cards": [...]}

# Obtener lecturas
GET /api/readings/
Headers: Authorization: Bearer <token>

# Verificar acceso
POST /api/readings/check-access
Headers: Authorization: Bearer <token>
Body: {"spread_type": "..."}
```

### Suscripciones
```bash
# Ver planes
GET /api/subscription/plans

# Suscripción actual
GET /api/subscription/current
Headers: Authorization: Bearer <token>

# Upgrade a premium (demo)
POST /api/subscription/demo-upgrade
Headers: Authorization: Bearer <token>
```

## 🧪 Pruebas

### Probar con curl

```bash
# Health check
curl http://localhost:5000/api/health

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@tarot.com","password":"demo123"}'

# Obtener uso (reemplazar TOKEN)
curl http://localhost:5000/api/user/usage \
  -H "Authorization: Bearer TOKEN"
```

### Ejecutar suite de pruebas

```bash
cd /vercel/sandbox
python3 test_api.py
```

## 📂 Archivos Importantes

### Backend
- `app.py` - Aplicación Flask principal
- `models.py` - Modelos de base de datos
- `auth.py` - Sistema de autenticación
- `middleware.py` - Middleware freemium
- `config.py` - Configuración
- `routes/` - Endpoints REST organizados

### Frontend
- `tarot_web_v2.html` - Interfaz mejorada
- `tarot_web_v2.js` - JavaScript con integración API

### Base de Datos
- `tarot.db` - SQLite database
- `init_db.py` - Script de inicialización

### Documentación
- `README_V2.md` - Documentación completa
- `GUIA_RAPIDA.md` - Esta guía
- `.env.example` - Ejemplo de configuración

## 🎨 Características del Frontend

### Sistema de Temas
- **Tema Oscuro**: Fondo azul oscuro, texto claro
- **Tema Claro**: Fondo azul claro, texto oscuro
- **Transiciones suaves** entre temas
- **Persistencia** en localStorage y backend

### Componentes UI
- **Header** con logo, toggle de tema, info de usuario
- **Modales** de login/registro con validación
- **Indicador de uso** para usuarios free
- **Tiradas bloqueadas** con icono de candado
- **Notificaciones** de éxito/error
- **Animaciones** suaves y efectos visuales

### Responsive Design
- Adaptado para móviles, tablets y desktop
- Grid flexible para tiradas
- Modales centrados y responsivos

## 🔒 Seguridad

- ✅ Contraseñas hasheadas con Werkzeug
- ✅ JWT tokens con expiración
- ✅ Refresh tokens para sesiones largas
- ✅ CORS configurado
- ✅ Validación de entrada en todos los endpoints
- ✅ Protección contra inyección SQL (SQLAlchemy)

## 📊 Base de Datos

### Tablas
- **users**: Usuarios del sistema
- **readings**: Lecturas de tarot
- **usage_limits**: Límites de uso diario
- **subscriptions**: Historial de suscripciones

### Relaciones
- User → Readings (1:N)
- User → UsageLimits (1:N)
- User → Subscriptions (1:N)

## 🚀 Próximos Pasos

### Para Desarrollo
1. Integrar procesador de pagos (Stripe/PayPal)
2. Implementar recuperación de contraseña
3. Agregar exportación a PDF
4. Crear app móvil
5. Implementar notificaciones push

### Para Producción
1. Configurar base de datos PostgreSQL
2. Usar servidor WSGI (Gunicorn)
3. Configurar HTTPS
4. Implementar rate limiting
5. Agregar logging y monitoreo
6. Configurar backups automáticos

## 🐛 Troubleshooting

### El servidor no inicia
```bash
# Verificar que las dependencias estén instaladas
~/.local/bin/pip install -r requirements.txt

# Verificar que el puerto 5000 esté libre
lsof -i :5000

# Reiniciar el servidor
pkill -f "python3 app.py"
cd /vercel/sandbox && python3 app.py
```

### Error de base de datos
```bash
# Reinicializar la base de datos
rm tarot.db
python3 init_db.py
```

### Problemas con JWT
- Verificar que SECRET_KEY y JWT_SECRET_KEY estén configurados
- Asegurarse de que el token no haya expirado
- Hacer logout y login nuevamente

## 📞 Soporte

Para reportar bugs o solicitar funcionalidades:
1. Revisar la documentación completa en `README_V2.md`
2. Verificar los logs del servidor
3. Ejecutar `test_api.py` para diagnóstico

---

## ✨ Resumen de Logros

✅ **Backend Flask** completo con autenticación JWT
✅ **Base de datos** SQLite con 4 tablas relacionadas
✅ **Sistema freemium** con límites y verificación
✅ **Persistencia de temas** claro/oscuro
✅ **Frontend mejorado** con componentes de auth
✅ **API REST** con 20+ endpoints
✅ **Usuarios de prueba** pre-configurados
✅ **Suite de pruebas** automatizada
✅ **Documentación** completa

🎉 **¡El sistema está completamente funcional y listo para usar!**

---

*Que las cartas iluminen tu camino* 🔮✨
