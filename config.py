"""
Configuración de la aplicación Flask
"""
import os
from datetime import timedelta

class Config:
    """Configuración base"""
    # Detect if running on Vercel
    IS_VERCEL = os.environ.get('VERCEL') == '1'
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration - Optimized for Vercel
    # Vercel uses ephemeral filesystem, so we need to handle database carefully
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        # Use provided database URL (PostgreSQL recommended for production)
        if DATABASE_URL.startswith('postgres://'):
            # Fix for SQLAlchemy 1.4+ which requires postgresql:// instead of postgres://
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    elif IS_VERCEL:
        # On Vercel without DATABASE_URL, use in-memory SQLite (data won't persist)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    else:
        # Local development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///tarot.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before using
        'pool_recycle': 300,    # Recycle connections after 5 minutes
        'pool_size': 10 if not IS_VERCEL else 1,  # Smaller pool for serverless
        'max_overflow': 20 if not IS_VERCEL else 0
    }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Freemium Limits
    FREE_DAILY_READINGS = 3
    FREE_ALLOWED_SPREADS = ['una_carta', 'tres_cartas']
    
    # CORS - Allow Vercel domains
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',') if os.environ.get('CORS_ORIGINS') else [
        'http://localhost:3000',
        'http://localhost:5000',
        'http://127.0.0.1:5000',
        'https://*.vercel.app',  # Allow all Vercel preview deployments
    ]
    
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
    
    # Vercel-specific settings
    if IS_VERCEL:
        # Disable Flask debug mode in production
        DEBUG = False
        TESTING = False
        # Use JSON logging for better Vercel log integration
        JSON_LOGGING = True
