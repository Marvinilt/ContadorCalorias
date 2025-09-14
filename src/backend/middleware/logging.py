"""
Middleware de Logging
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
import json
from datetime import datetime

# Configurar logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("contador_calorias")

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para logging de requests y responses"""
    
    async def dispatch(self, request: Request, call_next):
        """Procesar request con logging"""
        
        start_time = time.time()
        
        # Información del request
        request_info = {
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("User-Agent", ""),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Log del request entrante
        logger.info(f"Request: {request.method} {request.url.path}")
        
        try:
            # Procesar request
            response = await call_next(request)
            
            # Calcular tiempo de procesamiento
            process_time = time.time() - start_time
            
            # Información del response
            response_info = {
                "status_code": response.status_code,
                "process_time_ms": round(process_time * 1000, 2),
                "response_size": len(response.body) if hasattr(response, 'body') else 0
            }
            
            # Log del response
            log_level = logging.INFO
            if response.status_code >= 400:
                log_level = logging.WARNING
            if response.status_code >= 500:
                log_level = logging.ERROR
            
            logger.log(
                log_level,
                f"Response: {response.status_code} - {process_time*1000:.2f}ms - {request.method} {request.url.path}"
            )
            
            # Log detallado para análisis
            if request.url.path.startswith("/api/v1/analyze"):
                self._log_analysis_request(request_info, response_info)
            
            # Agregar header de tiempo de procesamiento
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log de errores
            process_time = time.time() - start_time
            
            logger.error(
                f"Error processing request: {request.method} {request.url.path} - "
                f"Error: {str(e)} - Time: {process_time*1000:.2f}ms"
            )
            
            raise
    
    def _get_client_ip(self, request: Request) -> str:
        """Obtener IP del cliente"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    def _log_analysis_request(self, request_info: dict, response_info: dict):
        """Log específico para requests de análisis"""
        
        analysis_log = {
            "type": "image_analysis",
            "timestamp": request_info["timestamp"],
            "client_ip": request_info["client_ip"],
            "status_code": response_info["status_code"],
            "process_time_ms": response_info["process_time_ms"],
            "success": response_info["status_code"] < 400
        }
        
        logger.info(f"Analysis Request: {json.dumps(analysis_log)}")
    
    def _should_log_body(self, request: Request) -> bool:
        """Determinar si se debe loggear el body del request"""
        
        # No loggear bodies de imágenes (muy grandes)
        if request.url.path.startswith("/api/v1/analyze/image"):
            return False
        
        # No loggear passwords
        if request.url.path.startswith("/api/v1/auth"):
            return False
        
        return True