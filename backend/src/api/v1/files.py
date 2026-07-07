from typing import Annotated

from fastapi import APIRouter, File, Form, Query, UploadFile
from fastapi.responses import FileResponse
from src.api.schemas import FileItem
from src.db.models import StoredFile
from src.services import files as files_service

router = APIRouter(prefix="/files", tags=["files"])


@router.get("", response_model=list[FileItem])
async def list_files(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[StoredFile]:
    return await files_service.list_files(limit, offset)


@router.get("/{file_id}", response_model=FileItem)
async def get_file(file_id: str) -> StoredFile:
    return await files_service.get_file(file_id)


@router.post("", response_model=FileItem, status_code=201)
async def create_file(
    file: Annotated[UploadFile, File()],
    title: Annotated[str, Form()] = "",
) -> StoredFile:
    return await files_service.create_file(title, file)


@router.delete("/{file_id}", status_code=204)
async def delete_file(file_id: str) -> None:
    await files_service.delete_file(file_id)


@router.get("/{file_id}/download")
async def download_file(file_id: str) -> FileResponse:
    file_item, path = await files_service.get_file_path(file_id)
    return FileResponse(
        path=path,
        filename=file_item.original_name,
        media_type=file_item.mime_type,
    )
