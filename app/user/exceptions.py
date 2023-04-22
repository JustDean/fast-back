from fastapi import HTTPException

USER_ALREADY_EXISTS_EXCEPTION = HTTPException(
    status_code=400, detail="User with this name already exists"
)
INVALID_LOGIN_DATA_EXCEPTION = HTTPException(
    status_code=400, detail="Incorrect user data"
)
UNAUTHORIZED_EXCEPTION = HTTPException(status_code=401, detail="Unauthorized")
