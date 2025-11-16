from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.logger import log_error, log_request, log_response
import time


async def logging_middleware(request: Request, call_next):
    """Middleware for request/response logging"""
    start_time = time.time()
    
    # Log request
    user_id = None
    if hasattr(request.state, 'user'):
        user_id = request.state.user.id if request.state.user else None
    
    log_request(request.method, request.url.path, user_id)
    
    try:
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        log_response(request.method, request.url.path, response.status_code, user_id)
        
        return response
    except HTTPException as e:
        log_response(request.method, request.url.path, e.status_code, user_id)
        raise
    except Exception as e:
        log_error(e, f"{request.method} {request.url.path}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
