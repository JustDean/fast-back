from aiobotocore.session import get_session, AioBaseClient
from app.attachment.exceptions import raise_s3_exception

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

    def get_file_url(self, filename: str) -> str:
        return f"{self.BASE_URL}/{filename}"

    async def get_s3_client(self) -> AioBaseClient:
        async with self.session.create_client(
            service_name=MINIO_SERVICE_NAME,
            endpoint_url=MINIO_HOST,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
        ) as s3_client:
            yield s3_client

    async def upload(
        self, s3_client: AioBaseClient, file: bytes, filename: str
    ) -> dict:
        try:
            return await s3_client.put_object(
                Bucket=MINIO_BUCKET_NAME, Key=filename, Body=file
            )
        except Exception as exc:
            raise raise_s3_exception(str(exc))

    async def get_object_info(
        self, s3_client: AioBaseClient, filename: str
    ) -> dict:
        try:
            return await s3_client.get_object_acl(
                Bucket=MINIO_BUCKET_NAME, Key=filename
            )
        except Exception as exc:
            raise raise_s3_exception(str(exc))


s3_accessor = S3Accessor()
