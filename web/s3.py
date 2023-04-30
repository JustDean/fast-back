import uuid
from secrets import token_hex
from aiobotocore.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.attachment.models import Attachment
from web.settings import (
    MINIO_HOST,
    MINIO_SERVICE_NAME,
    MINIO_BUCKET_NAME,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
)


class S3Accessor:
    BASE_URL = f"{MINIO_HOST}/{MINIO_BUCKET_NAME}"

    def __init__(self) -> None:
        self.session = get_session()

    # async def _get_session(self):
    #     async with self.session.create_client(
    #         service_name=MINIO_HOST,
    #         endpoint_url=MINIO_SERVICE_NAME,
    #         aws_access_key_id=MINIO_ACCESS_KEY,
    #         aws_secret_access_key=MINIO_SECRET_KEY,
    #     ) as s3_session:
    #         yield s3_session

    def get_file_url(self, filename: str) -> str:
        return f"{self.BASE_URL}/{filename}"

    async def upload(self, file: bytes, filename: str) -> Attachment:
        async with self.session.create_client(
            service_name=MINIO_SERVICE_NAME,
            endpoint_url=MINIO_HOST,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
        ) as s3_client:
            return await s3_client.put_object(
                Bucket=MINIO_BUCKET_NAME, Key=filename, Body=file
            )

    async def get_object_info(self, filename: str) -> dict:
        async with self.session.create_client(
            service_name=MINIO_SERVICE_NAME,
            endpoint_url=MINIO_HOST,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
        ) as s3_client:
            return await s3_client.get_object_acl(
                Bucket=MINIO_BUCKET_NAME, Key=filename
            )


s3_accessor = S3Accessor()
