# 🚀 Guía de Despliegue - Sistema de Tarot

> Guía completa para desplegar el Sistema de Lectura de Tarot en diferentes entornos.

## 📊 Índice

1. [Despliegue Local](#-despliegue-local)
2. [Servidor Web](#-servidor-web)
3. [Contenedores Docker](#-contenedores-docker)
4. [Servicios en la Nube](#-servicios-en-la-nube)
5. [Configuración de Producción](#-configuración-de-producción)
6. [Monitoreo y Mantenimiento](#-monitoreo-y-mantenimiento)

## 🖥️ Despliegue Local

### Desarrollo Rápido

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd tarot-app

# 2. Configurar entorno Python
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install numpy matplotlib scipy

# 4. Verificar instalación
python tarot_reader.py

# 5. Probar interfaz web
# Abrir tarot_web.html en navegador
```

### Servidor Local con Python

```bash
# Servidor HTTP simple
python -m http.server 8000
# Visitar: http://localhost:8000/tarot_web.html

# O con servidor más avanzado
python -m http.server 8000 --bind 127.0.0.1
```

### Configuración de Entorno

```bash
# .env (crear archivo)
TAROT_RANDOM_SOURCE=combinado
TAROT_DEBUG=false
TAROT_LOG_LEVEL=INFO
TAROT_DATA_DIR=./data
TAROT_WEB_PORT=8000
```

## 🌍 Servidor Web

### Apache HTTP Server

#### Configuración básica

```apache
# /etc/apache2/sites-available/tarot.conf
<VirtualHost *:80>
    ServerName tarot.example.com
    DocumentRoot /var/www/tarot
    
    <Directory /var/www/tarot>
        AllowOverride All
        Require all granted
    </Directory>
    
    # Habilitar CGI para Python (opcional)
    ScriptAlias /cgi-bin/ /var/www/tarot/cgi-bin/
    <Directory /var/www/tarot/cgi-bin>
        AllowOverride None
        Options +ExecCGI
        AddHandler cgi-script .py
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/tarot_error.log
    CustomLog ${APACHE_LOG_DIR}/tarot_access.log combined
</VirtualHost>
```

#### Instalación en Ubuntu/Debian

```bash
# 1. Instalar Apache
sudo apt update
sudo apt install apache2 python3-pip

# 2. Copiar archivos
sudo mkdir -p /var/www/tarot
sudo cp -r * /var/www/tarot/
sudo chown -R www-data:www-data /var/www/tarot

# 3. Configurar sitio
sudo cp tarot.conf /etc/apache2/sites-available/
sudo a2ensite tarot
sudo a2enmod cgi
sudo systemctl reload apache2

# 4. Instalar dependencias Python para www-data
sudo -u www-data pip3 install numpy matplotlib scipy
```

### Nginx + uWSGI

#### Configuración Nginx

```nginx
# /etc/nginx/sites-available/tarot
server {
    listen 80;
    server_name tarot.example.com;
    root /var/www/tarot;
    index tarot_web.html;
    
    # Servir archivos estáticos
    location / {
        try_files $uri $uri/ =404;
    }
    
    # API endpoints (opcional para futuro backend)
    location /api/ {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/tarot.sock;
    }
    
    # Logs
    access_log /var/log/nginx/tarot.access.log;
    error_log /var/log/nginx/tarot.error.log;
    
    # Configuración de seguridad
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
}
```

#### Backend Flask (Opcional)

```python
# app.py - API REST opcional
from flask import Flask, request, jsonify
import sys
sys.path.append('.')
from tarot_reader_enhanced import LectorTarot, TipoTirada

app = Flask(__name__)
lector = LectorTarot()

@app.route('/api/lectura', methods=['POST'])
def realizar_lectura():
    data = request.json
    tipo = TipoTirada(data.get('tipo', 'tres_cartas'))
    pregunta = data.get('pregunta', '')
    
    lectura = lector.realizar_lectura(tipo, pregunta)
    return jsonify(lectura)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

```bash
# Instalar Flask
pip install flask gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🐳 Contenedores Docker

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN useradd -m -s /bin/bash tarot
USER tarot
WORKDIR /home/tarot/app

# Copiar requirements
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Copiar aplicación
COPY --chown=tarot:tarot . .

# Exponer puerto
EXPOSE 8000

# Variables de entorno
ENV PYTHONPATH=/home/tarot/app
ENV PATH="/home/tarot/.local/bin:$PATH"

# Comando por defecto
CMD ["python", "-m", "http.server", "8000", "--bind", "0.0.0.0"]
```

### requirements.txt

```txt
numpy>=1.21.0
matplotlib>=3.5.0
scipy>=1.8.0
flask>=2.0.0
gunicorn>=20.1.0
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  tarot-web:
    build: .
    ports:
      - "8080:8000"
    volumes:
      - ./data:/home/tarot/app/data
    environment:
      - TAROT_RANDOM_SOURCE=combinado
      - TAROT_DEBUG=false
    restart: unless-stopped
    
  tarot-api:
    build: .
    command: ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
    ports:
      - "5000:5000"
    volumes:
      - ./data:/home/tarot/app/data
    environment:
      - TAROT_RANDOM_SOURCE=combinado
      - FLASK_ENV=production
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - tarot-web
      - tarot-api
    restart: unless-stopped
```

### Comandos Docker

```bash
# Construir imagen
docker build -t tarot-app .

# Ejecutar contenedor
docker run -d -p 8080:8000 --name tarot tarot-app

# Con Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f tarot-web

# Parar servicios
docker-compose down

# Actualizar
docker-compose pull && docker-compose up -d
```

## ☁️ Servicios en la Nube

### AWS (Amazon Web Services)

#### EC2 + Elastic Load Balancer

```bash
# 1. Crear instancia EC2
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --count 1 \
    --instance-type t3.micro \
    --key-name my-key-pair \
    --security-group-ids sg-0123456789abcdef0

# 2. Configurar security group
aws ec2 authorize-security-group-ingress \
    --group-id sg-0123456789abcdef0 \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

# 3. Conectar y configurar
ssh -i my-key-pair.pem ubuntu@ec2-ip-address.compute.amazonaws.com
```

#### S3 + CloudFront (Solo Frontend)

```bash
# 1. Crear bucket S3
aws s3 mb s3://tarot-app-bucket

# 2. Configurar para hosting estático
aws s3 website s3://tarot-app-bucket \
    --index-document tarot_web.html

# 3. Subir archivos
aws s3 sync . s3://tarot-app-bucket --exclude "*.py"

# 4. Crear distribución CloudFront
aws cloudfront create-distribution --distribution-config file://cloudfront-config.json
```

#### ECS (Elastic Container Service)

```json
{
  "family": "tarot-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "tarot-container",
      "image": "your-account.dkr.ecr.region.amazonaws.com/tarot-app:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/tarot-task",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### App Engine

```yaml
# app.yaml
runtime: python311

env_variables:
  TAROT_RANDOM_SOURCE: "combinado"
  TAROT_DEBUG: "false"

handlers:
- url: /static
  static_dir: static
  
- url: /.*
  script: auto
```

```bash
# Desplegar
gcloud app deploy
```

#### Cloud Run

```bash
# 1. Construir y subir imagen
gcloud builds submit --tag gcr.io/PROJECT-ID/tarot-app

# 2. Desplegar
gcloud run deploy tarot-service \
    --image gcr.io/PROJECT-ID/tarot-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Microsoft Azure

#### Azure App Service

```bash
# 1. Crear grupo de recursos
az group create --name tarot-rg --location "East US"

# 2. Crear plan de App Service
az appservice plan create \
    --name tarot-plan \
    --resource-group tarot-rg \
    --sku B1 \
    --is-linux

# 3. Crear Web App
az webapp create \
    --resource-group tarot-rg \
    --plan tarot-plan \
    --name tarot-app-unique \
    --deployment-container-image-name tarot-app:latest
```

### Heroku

```bash
# 1. Instalar Heroku CLI
# 2. Login
heroku login

# 3. Crear aplicación
heroku create tarot-app-unique

# 4. Configurar buildpack
heroku buildpacks:set heroku/python

# 5. Configurar variables
heroku config:set TAROT_RANDOM_SOURCE=combinado

# 6. Desplegar
git push heroku main
```

#### Procfile para Heroku

```
web: python -m http.server $PORT --bind 0.0.0.0
api: gunicorn app:app --bind 0.0.0.0:$PORT
```

## 🔧 Configuración de Producción

### Seguridad

#### HTTPS/SSL

```bash
# Certificado Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tarot.example.com
```

#### Headers de Seguridad

```nginx
# En Nginx
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options DENY;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';";
```

#### Rate Limiting

```nginx
# Nginx rate limiting
http {
    limit_req_zone $binary_remote_addr zone=tarot:10m rate=10r/m;
    
    server {
        location / {
            limit_req zone=tarot burst=5 nodelay;
        }
    }
}
```

### Variables de Entorno de Producción

```bash
# .env.production
TAROT_RANDOM_SOURCE=combinado
TAROT_DEBUG=false
TAROT_LOG_LEVEL=WARNING
TAROT_DATA_DIR=/var/lib/tarot/data
TAROT_LOG_DIR=/var/log/tarot
TAROT_MAX_LECTURAS_DIA=100
TAROT_CACHE_TIMEOUT=3600
```

### Logging Avanzado

```python
# logging_config.py
import logging
import logging.handlers
import os

def configure_logging():
    log_dir = os.getenv('TAROT_LOG_DIR', './logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configuración de logging
    logging.basicConfig(
        level=getattr(logging, os.getenv('TAROT_LOG_LEVEL', 'INFO')),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler(
                f'{log_dir}/tarot.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
```

### Base de Datos (Opcional)

#### SQLite para desarrollo

```python
# database.py
import sqlite3
import json
from datetime import datetime

class TarotDB:
    def __init__(self, db_path='tarot.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS lecturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tipo_tirada TEXT NOT NULL,
                pregunta TEXT,
                cartas TEXT NOT NULL,
                interpretacion TEXT,
                ip_address TEXT,
                user_agent TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def guardar_lectura(self, lectura, metadata=None):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT INTO lecturas 
            (tipo_tirada, pregunta, cartas, interpretacion, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            lectura['tipo_tirada'],
            lectura.get('pregunta', ''),
            json.dumps(lectura['cartas']),
            lectura.get('interpretacion', ''),
            metadata.get('ip') if metadata else None,
            metadata.get('user_agent') if metadata else None
        ))
        conn.commit()
        conn.close()
```

#### PostgreSQL para producción

```bash
# Instalar dependencias
pip install psycopg2-binary

# Variables de entorno
export DATABASE_URL="postgresql://user:password@localhost/tarot_db"
```

## 📊 Monitoreo y Mantenimiento

### Métricas de Sistema

```bash
# Script de monitoreo
#!/bin/bash
# monitor.sh

HOST="localhost"
PORT="8000"
LOG_FILE="/var/log/tarot/monitor.log"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Verificar servicio
    if curl -f http://$HOST:$PORT/tarot_web.html > /dev/null 2>&1; then
        STATUS="UP"
    else
        STATUS="DOWN"
    fi
    
    # Uso de CPU y memoria
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $1}' | awk -F'%' '{print $1}')
    MEMORY=$(free | grep Mem | awk '{printf "%.1f", $used/$2*100}')
    
    # Log
    echo "$TIMESTAMP - Status: $STATUS, CPU: $CPU%, Memory: $MEMORY%" >> $LOG_FILE
    
    sleep 60
done
```

### Alertas por Email

```python
# alerts.py
import smtplib
import os
from email.mime.text import MIMEText

def enviar_alerta(mensaje, asunto="Alerta Tarot App"):
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_to = os.getenv('ALERT_EMAIL')
    
    if not all([email_user, email_password, email_to]):
        print("Configuración de email incompleta")
        return
    
    msg = MIMEText(mensaje)
    msg['Subject'] = asunto
    msg['From'] = email_user
    msg['To'] = email_to
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        server.send_message(msg)
        server.quit()
        print("Alerta enviada")
    except Exception as e:
        print(f"Error enviando alerta: {e}")
```

### Backup Automático

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/tarot"
SOURCE_DIR="/var/www/tarot"
DATA_DIR="/var/lib/tarot/data"

mkdir -p $BACKUP_DIR

# Backup de archivos
tar -czf $BACKUP_DIR/tarot_files_$DATE.tar.gz -C $SOURCE_DIR .

# Backup de datos
cp -r $DATA_DIR $BACKUP_DIR/data_$DATE

# Limpiar backups antiguos (mantener 7 días)
find $BACKUP_DIR -name "tarot_*" -mtime +7 -delete

echo "Backup completado: $DATE"
```

### Cron Jobs

```bash
# crontab -e

# Backup diario a las 2 AM
0 2 * * * /opt/tarot/scripts/backup.sh

# Limpiar logs semanalmente
0 0 * * 0 find /var/log/tarot -name "*.log" -mtime +30 -delete

# Verificar salud cada 5 minutos
*/5 * * * * /opt/tarot/scripts/health_check.sh

# Reiniciar servicio semanalmente
0 3 * * 0 systemctl restart tarot-service
```

### Actualizaciones

```bash
#!/bin/bash
# update.sh

# Detener servicio
sudo systemctl stop tarot-service

# Backup
/opt/tarot/scripts/backup.sh

# Actualizar código
cd /var/www/tarot
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt --upgrade

# Verificar sintaxis
python -m py_compile *.py

# Reiniciar servicio
sudo systemctl start tarot-service

# Verificar salud
sleep 10
curl -f http://localhost:8000/tarot_web.html

echo "Actualización completada"
```

## 🚨 Resolución de Problemas

### Problemas Comunes

#### Servicio no responde
```bash
# Verificar logs
sudo journalctl -u tarot-service -f

# Verificar puertos
sudo netstat -tlnp | grep :8000

# Reiniciar servicio
sudo systemctl restart tarot-service
```

#### Alto uso de memoria
```bash
# Verificar procesos
top -p $(pgrep python)

# Verificar logs de memoria
dmesg | grep -i "killed process"

# Configurar swap si es necesario
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### Problemas de permisos
```bash
# Verificar permisos
ls -la /var/www/tarot

# Corregir permisos
sudo chown -R www-data:www-data /var/www/tarot
sudo chmod -R 755 /var/www/tarot
```

### Logs Útiles

```bash
# Logs del sistema
sudo journalctl -u tarot-service --since "1 hour ago"

# Logs de acceso web
sudo tail -f /var/log/nginx/tarot.access.log

# Logs de errores
sudo tail -f /var/log/nginx/tarot.error.log

# Logs de la aplicación
tail -f /var/log/tarot/tarot.log
```

---

✨ **¡Tu sistema de tarot está listo para iluminar el mundo!** ✨