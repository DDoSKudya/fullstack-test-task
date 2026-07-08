from io import BytesIO

from sqlalchemy import delete
from src.db.models import Alert, StoredFile
from src.db.session import get_session, session_scope
from starlette.datastructures import Headers, UploadFile


def make_upload(data: bytes, filename: str = "test.txt") -> UploadFile:
    return UploadFile(
        file=BytesIO(data),
        filename=filename,
        headers=Headers({"content-type": "text/plain"}),
    )


async def reset_tables() -> None:
    async with session_scope():
        session = get_session()
        await session.execute(delete(Alert))
        await session.execute(delete(StoredFile))
