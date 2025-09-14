"""
Middleware y utilidades de autenticación
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Obtener usuario actual desde JWT token
    Dependency para proteger endpoints
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar JWT token
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "access":
            raise credentials_exception
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise credentials_exception
    
    # Buscar usuario en base de datos
    # En producción: user = db.query(User).filter(User.id == int(user_id)).first()
    
    # Simulación para MVP
    user = {
        "id": int(user_id),
        "email": "test@example.com",
        "profile": {
            "first_name": "Usuario",
            "last_name": "Test"
        },
        "is_active": True
    }
    
    if user is None or not user.get("is_active"):
        raise credentials_exception
        
    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    """
    Obtener usuario activo (wrapper adicional si se necesita)
    """
    if not current_user.get("is_active", True):
        raise HTTPException(
            status_code=400, 
            detail="Usuario inactivo"
        )
    return current_user

def verify_token(token: str) -> dict:
    """
    Verificar token JWT sin dependency
    Útil para verificaciones manuales
    """
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expirado"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )