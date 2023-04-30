import os
from distutils.util import strtobool


DEBUG = strtobool(os.getenv("DEBUG", "false"))
PORT = port = int(os.getenv("PORT", 8080))

USE_SENTRY = strtobool(os.getenv("USE_SENTRY", "false"))
SENTRY_DSN = os.getenv("SENTRY_DSN", "127.0.0.1")
SENTRY_ENV = os.getenv("SENTRY_ENV", "local")

DATABASE_HOST = os.getenv("DATABASE_HOST", "127.0.0.1")
DATABASE_PORT = os.getenv("DATABASE_PORT", 5432)
DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
DATABASE_TABLE = os.getenv("DATABASE_TABLE", "test")

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_DATABASE_INDEX = os.getenv("REDIS_DATABASE_INDEX", 7)
REDIS_USERNAME = os.getenv("REDIS_USERNAME", "user")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "password")
