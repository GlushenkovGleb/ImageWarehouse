from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = 8090
    database_url: str = 'sqlite:///./isinstance/database.sqlite3'
    data_path: str = './isinstance/database.sqlite3'
    minio_url: str = 'minio:9000'
    minio_access_key: str = 'access_key'
    minio_secret_key: str = 'secret_key'
    minio_secure: bool = False

    jwt_algorithm: str = 'HS256'
    jwt_expire_minutes: int = 60
    jwt_secret_key: str = (
        'c76d0782090d6f7f49e50565e8c6a2e66db9f0707fc5dd065e5867a4c74d8f21'
    )


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
