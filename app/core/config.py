
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, PostgresDsn, validator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    DESCRIPTION: str
    # DEBUG: bool 
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # email server detals
    EMAIL_SERVER: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_TLS: bool

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    JWT_SETTINGS: Optional[Dict[str, Any]] = None
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_TOKEN_PREFIX: str
    JWT_AUDIENCE: str
    JWT_ISSUER: str
    
    @validator('JWT_SETTINGS', pre=True)
    def assemble_jwt_settings(cls, v: Optional[str], values: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(v, str):
            return v
        return {
            "SECRET_KEY": values.get("SECRET_KEY"),
            "JWT_ALGORITHM": values.get("JWT_ALGORITHM"),
            "ACCESS_TOKEN_EXPIRE_MINUTES": values.get("ACCESS_TOKEN_EXPIRE_MINUTES"),
            "JWT_TOKEN_PREFIX": values.get("JWT_TOKEN_PREFIX"),
            "JWT_AUDIENCE": values.get("JWT_AUDIENCE"),
            "JWT_ISSUER": values.get("JWT_ISSUER"),
        }
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()