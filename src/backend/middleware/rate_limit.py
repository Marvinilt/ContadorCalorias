"""
Middleware de Rate Limiting
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
import asyncio
from collections import defaultdict, deque
from config import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware para limitar requests por IP y endpoint"""
    
    def __init__(self, app):
        super().__init__(app)
        # Almacenar requests por IP y endpoint
        self.requests = defaultdict(lambda: defaultdict(deque))
        
        # Configuración de límites por endpoint
        self.limits = {
            "/api/v1/analyze/image": {"requests": 10, "window": 60},  # 10 req/min
            "/api/v1/auth/login": {"requests": 5, "window": 60},      # 5 req/min
            "/api/v1/auth/register": {"requests": 3, "window": 60},   # 3 req/min
            "/api/v1/foods/search": {"requests": 100, "window": 60},  # 100 req/min
            "default": {"requests": 60, "window": 60}                 # 60 req/min por defecto
        }
    
    async def dispatch(self, request: Request, call_next):
        """Procesar request con rate limiting"""
        
        # Obtener IP del cliente
        client_ip = self._get_client_ip(request)
        
        # Obtener endpoint
        endpoint = request.url.path
        
        # Verificar rate limit
        if not await self._check_rate_limit(client_ip, endpoint):
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Se ha excedido el límite de requests por minuto",
                        "retry_after": 60
                    }
                },
                headers={
                    "X-RateLimit-Limit": str(self._get_limit(endpoint)["requests"]),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time()) + 60),
                    "Retry-After": "60"
                }
            )
        
        # Continuar con el request
        response = await call_next(request)
        
        # Agregar headers de rate limiting
        limit_info = self._get_limit(endpoint)
        remaining = self._get_remaining_requests(client_ip, endpoint)
        
        response.headers["X-RateLimit-Limit"] = str(limit_info["requests"])
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time()) + limit_info["window"])
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """Obtener IP del cliente"""
        # Verificar headers de proxy
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # IP directa
        return request.client.host if request.client else "unknown"
    
    async def _check_rate_limit(self, client_ip: str, endpoint: str) -> bool:
        """Verificar si el request está dentro del límite"""
        
        current_time = time.time()
        limit_info = self._get_limit(endpoint)
        
        # Limpiar requests antiguos
        self._cleanup_old_requests(client_ip, endpoint, current_time, limit_info["window"])
        
        # Verificar límite
        request_count = len(self.requests[client_ip][endpoint])
        
        if request_count >= limit_info["requests"]:
            return False
        
        # Agregar request actual
        self.requests[client_ip][endpoint].append(current_time)
        
        return True
    
    def _get_limit(self, endpoint: str) -> dict:
        """Obtener configuración de límite para endpoint"""
        return self.limits.get(endpoint, self.limits["default"])
    
    def _cleanup_old_requests(self, client_ip: str, endpoint: str, current_time: float, window: int):
        """Limpiar requests fuera de la ventana de tiempo"""
        cutoff_time = current_time - window
        
        while (self.requests[client_ip][endpoint] and 
               self.requests[client_ip][endpoint][0] < cutoff_time):
            self.requests[client_ip][endpoint].popleft()
    
    def _get_remaining_requests(self, client_ip: str, endpoint: str) -> int:
        """Obtener requests restantes"""
        limit_info = self._get_limit(endpoint)
        current_count = len(self.requests[client_ip][endpoint])
        return max(0, limit_info["requests"] - current_count)