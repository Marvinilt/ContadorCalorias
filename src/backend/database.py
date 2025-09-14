"""
Configuración de base de datos PostgreSQL
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import asyncpg
import asyncio
from config import settings

# SQLAlchemy setup
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()

async def init_db():
    """Inicializar base de datos y crear tablas"""
    try:
        # Crear tablas si no existen
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas de base de datos creadas/verificadas")
        
        # Verificar conexión
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ Conexión a PostgreSQL exitosa")
            
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        raise

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redis connection
import redis.asyncio as redis

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_redis():
    """Dependency para obtener cliente Redis"""
    return redis_client