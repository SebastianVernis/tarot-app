"""
Configuración de la aplicación Flask
"""
import os
from datetime import timedelta

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tarot.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Freemium Limits
    FREE_DAILY_READINGS = 3
    FREE_ALLOWED_SPREADS = ['una_carta', 'tres_cartas']
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000', 'http://127.0.0.1:5000']
    
    # Pagination
    READINGS_PER_PAGE = 20
    
    # Google Gemini AI Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-pro')
    
    # Astrology Configuration
    ASTROLOGY_ENABLED = True
    FREE_ASTROLOGY_READINGS = 2  # Lecturas astrológicas gratuitas por día
    DEFAULT_HOUSE_SYSTEM = os.environ.get('DEFAULT_HOUSE_SYSTEM', 'P')  # Placidus por defecto
    INCLUDE_MINOR_ASPECTS = os.environ.get('INCLUDE_MINOR_ASPECTS', 'true').lower() == 'true'
