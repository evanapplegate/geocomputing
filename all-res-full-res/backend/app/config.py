from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str
    cloudflare_r2_access_key_id: str
    cloudflare_r2_secret_access_key: str
    cloudflare_r2_bucket_name: str
    cloudflare_r2_endpoint: str
    google_client_id: str
    google_client_secret: str
    github_client_id: str
    github_client_secret: str
    x_client_id: str
    x_client_secret: str
    secret_key: str
    email_api_key: Optional[str] = None
    email_from: str = "noreply@allresfullres.com"
    frontend_url: str = "http://localhost:3000"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
