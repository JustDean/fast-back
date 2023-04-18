from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.accessors import user_accessor
from app.user.forms import (
    UserCreateForm,
    UserNamePassForm,
    UserResponseForm,
)
from app.user.models import User
from app.session.accessors import session_accessor
from web.postgres import get_session


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/signup", response_model=UserResponseForm)
async def signup(
    response: Response,
    user_data: UserCreateForm,
    db_session: AsyncSession = Depends(get_session),
) -> User:
    try:
        new_user = await user_accessor.create(db_session, user_data)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="User with this name already exists"
        )
    user_session = await session_accessor.create(db_session, new_user)
    response.set_cookie("sessionid", user_session.id)

    return new_user.to_dict()


@router.post("/login", response_model=UserResponseForm)
async def login(
    response: Response,
    user_data: UserNamePassForm,
    db_session: AsyncSession = Depends(get_session),
) -> User:
    user = await user_accessor.get_by_name(db_session, user_data.name)
    is_correct = user.compare_passwords(user_data.password)
    if not is_correct:
        raise HTTPException(status_code=400, detail="Incorrect user data")

    user_session = await session_accessor.create(db_session, user)
    response.set_cookie("sessionid", user_session.id)

    return user.to_dict()


@router.post("/logout")
async def logout(
    response: Response,
    db_session: AsyncSession = Depends(get_session),
    sessionid: str | None = Cookie(None),
) -> None:
    if not sessionid:
        raise HTTPException(status_code=401, detail="Unauthorized")

    await session_accessor.delete(db_session, sessionid)
    response.delete_cookie("sessionid")

    return None


@router.get("/current", response_model=UserResponseForm)
async def current(
    db_session: AsyncSession = Depends(get_session),
    sessionid: str | None = Cookie(None),
) -> User:
    the_user = await user_accessor.get_by_cookie(db_session, sessionid)
    if not the_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return the_user.to_dict()
