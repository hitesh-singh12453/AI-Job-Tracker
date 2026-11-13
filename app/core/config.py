from pydantic_settings import BaseSettings, SettingsConfigDict


# Read and validate application configuration from environment variables
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    # Default JWT configuration
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Tell Pydantic where to find environment variables
    model_config = SettingsConfigDict(env_file=".env")


# Create one settings object to use throughout the application
settings = Settings()


"""
Important:
1. DATABASE_URL and SECRET_KEY are required.
2. ALGORITHM and ACCESS_TOKEN_EXPIRE_MINUTES have default values.
3. Pydantic reads matching values from environment variables or .env.
4. Extra variables in .env do not need to be defined as Settings fields
   by default.
"""