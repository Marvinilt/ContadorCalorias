"""
Router de autenticación
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt

from database import get_db
from models.requests import UserRegisterRequest, UserLoginRequest
from models.responses import UserResponse, TokenResponse
from config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """Registrar nuevo usuario"""
    
    # Verificar si el email ya existe
    # existing_user = db.query(User).filter(User.email == user_data.email).first()
    # if existing_user:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="El email ya está registrado"
    #     )
    
    # Hash de la contraseña
    password_hash = bcrypt.hashpw(
        user_data.password.encode('utf-8'), 
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Crear usuario (simulado para MVP)
    user = {
        "id": 1,
        "email": user_data.email,
        "profile": user_data.profile or {},
        "created_at": datetime.utcnow()
    }
    
    # Generar tokens
    tokens = create_tokens(user["id"])
    
    return {
        "user": user,
        "tokens": tokens
    }

@router.post("/login", response_model=TokenResponse)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Iniciar sesión"""
    
    # Buscar usuario por email
    # user = db.query(User).filter(User.email == form_data.username).first()
    
    # Simulación para MVP
    if form_data.username == "test@example.com" and form_data.password == "password123":
        user = {
            "id": 1,
            "email": "test@example.com",
            "profile": {}
        }
        
        tokens = create_tokens(user["id"])
        
        return {
            "user": user,
            "tokens": tokens
        }
    
    raise HTTPException(
        status_code=401,
        detail="Credenciales inválidas"
    )

@router.post("/refresh", response_model=dict)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Renovar token de acceso"""
    
    try:
        # Verificar refresh token
        payload = jwt.decode(
            refresh_token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        # Generar nuevo access token
        access_token = create_access_token(user_id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def create_tokens(user_id: int) -> dict:
    """Crear access y refresh tokens"""
    
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

def create_access_token(user_id: int) -> str:
    """Crear access token JWT"""
    
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access"
    }
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    """Crear refresh token JWT"""
    
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh"
    }
    
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Obtener usuario actual desde JWT token"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Buscar usuario en base de datos
    # user = db.query(User).filter(User.id == int(user_id)).first()
    
    # Simulación para MVP
    user = {
        "id": int(user_id),
        "email": "test@example.com",
        "profile": {}
    }
    
    if user is None:
        raise credentials_exception
        
    return user