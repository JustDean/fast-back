from secrets import token_hex
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.attachment.accessors import attachment_accessor
from app.attachment.forms import AttachmentForm
from web.s3 import s3_accessor
from web.postgres import get_session


router = APIRouter(
    prefix="/attachment",
    tags=["attachment"],
    # responses={400: {"description": "Not found"}},
)


@router.post("/upload", response_model=AttachmentForm)
async def upload(
    file: UploadFile,
    db_session: AsyncSession = Depends(get_session),
) -> dict:
    file_data = await file.read()
    filename = f"{token_hex(6)}{file.filename}"
    await s3_accessor.upload(file_data, filename)
    file_url = s3_accessor.get_file_url(filename)
    attachment = await attachment_accessor.create(
        db_session, filename, file_url
    )
    return attachment.to_dict()
