from app.user.models import User


def user_to_dict(user: User) -> dict:
    return {"id": user.id, "name": user.name}
