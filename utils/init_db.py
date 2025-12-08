"""
Script para inicializar la base de datos con datos de prueba
"""
from app import create_app
from src.models import db, User, Subscription
from datetime import datetime, timedelta

def init_database():
    """Inicializa la base de datos con datos de prueba"""
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas...")
        db.create_all()
        print("✅ Tablas creadas")
        
        # Verificar si ya existen usuarios
        if User.query.count() > 0:
            print("⚠️  La base de datos ya contiene usuarios")
            return
        
        # Crear usuario de prueba gratuito
        print("\nCreando usuarios de prueba...")
        
        user_free = User(
            email='demo@tarot.com',
            username='demo',
            subscription_plan='free',
            theme='dark'
        )
        user_free.set_password('demo123')
        db.session.add(user_free)
        
        # Crear usuario premium de prueba
        user_premium = User(
            email='premium@tarot.com',
            username='premium',
            subscription_plan='premium',
            theme='light',
            subscription_start=datetime.utcnow(),
            subscription_end=datetime.utcnow() + timedelta(days=30)
        )
        user_premium.set_password('premium123')
        db.session.add(user_premium)
        
        # Crear suscripción para el usuario premium
        subscription = Subscription(
            user_id=2,  # El segundo usuario
            plan='premium',
            status='active',
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
            payment_method='demo',
            amount=9.99,
            currency='USD'
        )
        db.session.add(subscription)
        
        db.session.commit()
        
        print("✅ Usuarios de prueba creados:")
        print("\n📧 Usuario Gratuito:")
        print("   Email: demo@tarot.com")
        print("   Password: demo123")
        print("   Plan: Free (3 lecturas/día)")
        
        print("\n✨ Usuario Premium:")
        print("   Email: premium@tarot.com")
        print("   Password: premium123")
        print("   Plan: Premium (ilimitado)")
        
        print("\n🎉 Base de datos inicializada correctamente!")

if __name__ == '__main__':
    init_database()
