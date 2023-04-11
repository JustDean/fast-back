from fastapi import FastAPI

from app.base.views import router as base_router
from app.user.views import router as user_router


app = FastAPI()

routers = [
    base_router,
    user_router,
]
for router in routers:
    app.include_router(router)
