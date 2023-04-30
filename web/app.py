import os
from fastapi import FastAPI
from distutils.util import strtobool
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

from app.base.views import router as base_router
from app.user.views import router as user_router


DEBUG = strtobool(os.getenv("DEBUG", False))
USE_SENTRY = strtobool(os.getenv("USE_SENTRY", False))
SENTRY_DSN = os.getenv("SENTRY_DSN", "127.0.0.1")
SENTRY_ENV = os.getenv("SENTRY_ENV", "local")

if USE_SENTRY:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENV,
        integrations=[
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(transaction_style="endpoint"),
        ],
        debug=DEBUG,
    )


app = FastAPI()

routers = [
    base_router,
    user_router,
]
for router in routers:
    app.include_router(router)
