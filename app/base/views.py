from fastapi import APIRouter


router = APIRouter(
    tags=["base"],
)


@router.get("/ping")
async def pong() -> dict:
    return {"ping": "pong"}
