from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.accessors import user_accessor
from app.user.exceptions import (
    INVALID_LOGIN_DATA_EXCEPTION,
    UNAUTHORIZED_EXCEPTION,
    USER_ALREADY_EXISTS_EXCEPTION,
)
from app.user.forms import (
    UserCreateForm,
    UserNamePassForm,
    UserResponseForm,
)
from app.session.accessors import session_accessor
from web.postgres import get_session


router = APIRouter(
    prefix="/user",
    tags=["user"],
    # responses={400: {"description": "Not found"}},
)


@router.post("/signup", response_model=UserResponseForm)
async def signup(
    response: Response,
    user_data: UserCreateForm,
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        new_user = await user_accessor.create(db_session, user_data)
    except IntegrityError:
        raise USER_ALREADY_EXISTS_EXCEPTION

    user_session = await session_accessor.create(db_session, new_user)
    response.set_cookie("sessionid", user_session.id)
    return new_user.to_dict()


@router.post("/login", response_model=UserResponseForm)
async def login(
    response: Response,
    user_data: UserNamePassForm,
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    user = await user_accessor.get_by_name(db_session, user_data.name)
    if not user:
        raise INVALID_LOGIN_DATA_EXCEPTION

    is_correct = user.compare_passwords(user_data.password)
    if not is_correct:
        raise INVALID_LOGIN_DATA_EXCEPTION

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
        raise UNAUTHORIZED_EXCEPTION

    await session_accessor.delete(db_session, sessionid)
    response.delete_cookie("sessionid")
    return None


@router.get("/current", response_model=UserResponseForm)
async def current(
    db_session: AsyncSession = Depends(get_session),
    sessionid: str | None = Cookie(None),
) -> dict:
    if not sessionid:
        raise UNAUTHORIZED_EXCEPTION

    user_session = await session_accessor.get(db_session, sessionid)
    if not user_session:
        raise UNAUTHORIZED_EXCEPTION

    the_user = await user_accessor.get_by_id(db_session, user_session.user)
    return the_user.to_dict()
