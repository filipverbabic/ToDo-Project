from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DB_URL")
DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY")
TOKEN_EXPIRATION_HOURS = config("TOKEN_EXPIRATION_HOURS", cast=int, default=8)
REDIS_URL = config("REDIS_URL")