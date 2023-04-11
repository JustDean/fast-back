from fastapi import HTTPException


NOT_FOUND_ERROR = HTTPException(status_code=404, detail="Not found error")
BAD_REQUEST_ERROR = HTTPException(status_code=400, detail="Bad request error")
