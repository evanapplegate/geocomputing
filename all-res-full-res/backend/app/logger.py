import logging
import sys
from datetime import datetime
from typing import Optional

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("all_res_full_res")


def log_request(method: str, path: str, user_id: Optional[int] = None):
    """Log API request"""
    logger.info(f"REQUEST: {method} {path} | User: {user_id or 'Anonymous'}")


def log_response(method: str, path: str, status_code: int, user_id: Optional[int] = None):
    """Log API response"""
    logger.info(f"RESPONSE: {method} {path} | Status: {status_code} | User: {user_id or 'Anonymous'}")


def log_auth_event(event: str, user_id: Optional[int] = None, details: Optional[str] = None):
    """Log authentication events"""
    msg = f"AUTH: {event} | User: {user_id or 'Unknown'}"
    if details:
        msg += f" | {details}"
    logger.info(msg)


def log_upload(file_size: int, file_type: str, user_id: int, success: bool, error: Optional[str] = None):
    """Log file upload events"""
    size_mb = file_size / (1024 * 1024)
    status = "SUCCESS" if success else "FAILED"
    msg = f"UPLOAD: {status} | User: {user_id} | Size: {size_mb:.2f}MB | Type: {file_type}"
    if error:
        msg += f" | Error: {error}"
    logger.info(msg) if success else logger.error(msg)


def log_error(error: Exception, context: Optional[str] = None):
    """Log errors with stack trace"""
    msg = f"ERROR: {type(error).__name__}: {str(error)}"
    if context:
        msg = f"{context} | {msg}"
    logger.error(msg, exc_info=True)
