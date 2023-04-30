from fastapi import FastAPI
from distutils.util import strtobool
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

from web.settings import DEBUG, USE_SENTRY, SENTRY_DSN, SENTRY_ENV
from app.base.views import router as base_router
from app.user.views import router as user_router


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
