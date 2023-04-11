from app.user.models import User


def serialize_user(user: User) -> dict:
    return {"id": user.id, "name": user.name}
