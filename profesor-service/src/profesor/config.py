from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación leída desde variables de entorno o .env."""

    # URL de conexión a PostgreSQL. Formato: postgresql://usuario:password@host:puerto/bd
    database_url: str = "postgresql://profesor_user:profesor_pass@localhost:5432/profesor_db"
    app_name: str = "profesor-service"
    debug: bool = False

    # Lee primero las variables de entorno del sistema, luego el archivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Instancia global — se importa desde otros módulos
settings = Settings()
