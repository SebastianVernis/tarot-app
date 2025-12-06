"""
Modelos de base de datos para el sistema de Tarot
"""
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(db.Model):
    """Modelo de usuario"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Suscripción
    subscription_plan = db.Column(db.String(20), default='free')  # 'free' o 'premium'
    subscription_start = db.Column(db.DateTime, nullable=True)
    subscription_end = db.Column(db.DateTime, nullable=True)
    
    # Preferencias
    theme = db.Column(db.String(10), default='dark')  # 'dark' o 'light'
    language = db.Column(db.String(5), default='es')
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relaciones
    readings = db.relationship('Reading', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    usage_limits = db.relationship('UsageLimit', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Establece el hash de la contraseña"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def is_premium(self):
        """Verifica si el usuario tiene plan premium activo"""
        if self.subscription_plan != 'premium':
            return False
        
        if self.subscription_end and self.subscription_end < datetime.utcnow():
            return False
        
        return True
    
    def to_dict(self, include_email=False):
        """Convierte el usuario a diccionario"""
        data = {
            'id': self.id,
            'username': self.username,
            'subscription_plan': self.subscription_plan,
            'is_premium': self.is_premium(),
            'theme': self.theme,
            'language': self.language,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        if include_email:
            data['email'] = self.email
        
        if self.subscription_end:
            data['subscription_end'] = self.subscription_end.isoformat()
        
        return data


class Reading(db.Model):
    """Modelo de lectura de tarot"""
    __tablename__ = 'readings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Datos de la lectura
    spread_type = db.Column(db.String(50), nullable=False)  # tipo de tirada
    question = db.Column(db.Text, nullable=True)
    cards_data = db.Column(db.Text, nullable=False)  # JSON con las cartas
    interpretation = db.Column(db.Text, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_favorite = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    
    def set_cards(self, cards_list):
        """Guarda las cartas como JSON"""
        self.cards_data = json.dumps(cards_list, ensure_ascii=False)
    
    def get_cards(self):
        """Obtiene las cartas desde JSON"""
        return json.loads(self.cards_data) if self.cards_data else []
    
    def to_dict(self):
        """Convierte la lectura a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'spread_type': self.spread_type,
            'question': self.question,
            'cards': self.get_cards(),
            'interpretation': self.interpretation,
            'created_at': self.created_at.isoformat(),
            'is_favorite': self.is_favorite,
            'notes': self.notes
        }


class UsageLimit(db.Model):
    """Modelo para controlar límites de uso diario"""
    __tablename__ = 'usage_limits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Límites
    date = db.Column(db.Date, default=date.today, nullable=False, index=True)
    readings_count = db.Column(db.Integer, default=0)
    
    # Índice único para evitar duplicados
    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )
    
    def to_dict(self):
        """Convierte el límite a diccionario"""
        return {
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'readings_count': self.readings_count
        }


class Subscription(db.Model):
    """Modelo para historial de suscripciones"""
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Datos de suscripción
    plan = db.Column(db.String(20), nullable=False)  # 'free' o 'premium'
    status = db.Column(db.String(20), default='active')  # 'active', 'cancelled', 'expired'
    
    # Fechas
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    
    # Pago (para futuras integraciones)
    payment_method = db.Column(db.String(50), nullable=True)
    amount = db.Column(db.Float, nullable=True)
    currency = db.Column(db.String(3), default='USD')
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación
    user = db.relationship('User', backref='subscription_history')
    
    def to_dict(self):
        """Convierte la suscripción a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan': self.plan,
            'status': self.status,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'payment_method': self.payment_method,
            'amount': self.amount,
            'currency': self.currency,
            'created_at': self.created_at.isoformat()
        }


class AstrologyReading(db.Model):
    """Modelo para lecturas astrológicas y cartas natales"""
    __tablename__ = 'astrology_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Datos de nacimiento
    birth_date = db.Column(db.DateTime, nullable=False)
    birth_latitude = db.Column(db.Float, nullable=False)
    birth_longitude = db.Column(db.Float, nullable=False)
    birth_timezone = db.Column(db.String(50), nullable=True)
    birth_location_name = db.Column(db.String(200), nullable=True)
    
    # Tipo de lectura
    reading_type = db.Column(db.String(50), default='birth_chart')  # 'birth_chart', 'transit', 'compatibility'
    
    # Datos calculados (JSON)
    chart_data = db.Column(db.Text, nullable=False)  # JSON con posiciones planetarias completas
    
    # Interpretación generada por IA
    interpretation = db.Column(db.Text, nullable=True)
    
    # Resumen rápido
    sun_sign = db.Column(db.String(20), nullable=True)
    moon_sign = db.Column(db.String(20), nullable=True)
    rising_sign = db.Column(db.String(20), nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_favorite = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    
    # Relación
    user = db.relationship('User', backref='astrology_readings')
    
    def set_chart_data(self, chart_dict):
        """Guarda los datos de la carta como JSON"""
        self.chart_data = json.dumps(chart_dict, ensure_ascii=False)
    
    def get_chart_data(self):
        """Obtiene los datos de la carta desde JSON"""
        return json.loads(self.chart_data) if self.chart_data else {}
    
    def to_dict(self, include_full_chart=False):
        """Convierte la lectura astrológica a diccionario"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'birth_date': self.birth_date.isoformat(),
            'birth_location': {
                'latitude': self.birth_latitude,
                'longitude': self.birth_longitude,
                'timezone': self.birth_timezone,
                'name': self.birth_location_name
            },
            'reading_type': self.reading_type,
            'summary': {
                'sun_sign': self.sun_sign,
                'moon_sign': self.moon_sign,
                'rising_sign': self.rising_sign
            },
            'interpretation': self.interpretation,
            'created_at': self.created_at.isoformat(),
            'is_favorite': self.is_favorite,
            'notes': self.notes
        }
        
        if include_full_chart:
            data['chart_data'] = self.get_chart_data()
        
        return data
