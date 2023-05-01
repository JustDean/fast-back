from fastapi import HTTPException


def raise_s3_exception(description: str | None = None) -> HTTPException:
    detail = (
        description
        if description
        else "Error occured while uploading file to s3 storage"
    )
    return HTTPException(status_code=500, detail=detail)
