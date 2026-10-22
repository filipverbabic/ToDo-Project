from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DB_URL")
DEBUG = config("DEBUG", cast=bool, default=False)