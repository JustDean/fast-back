from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.attachment.models import Attachment


class AttachmentAccessor:
    async def create(
        self, db_session: AsyncSession, filename: str, file_url: str
    ) -> Attachment:
        try:
            new_attachment = Attachment(name=filename, url=file_url)
            db_session.add(new_attachment)
            await db_session.commit()

            await db_session.refresh(new_attachment)
            return new_attachment
        except IntegrityError as exc:
            raise exc


attachment_accessor = AttachmentAccessor()
