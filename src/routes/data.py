import aiofiles
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController
from models import ResponseSignal
import logging

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
    app_settings: Settings = Depends(get_settings)):

    # validate the file properties
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal},
        )

    filename = (file.filename or "").replace("\\", "/").rsplit("/", 1)[-1]
    if not filename or filename in {".", ".."} or "\x00" in filename:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": "invalid_filename"},
        )

    try:
        file_path = data_controller.generate_unique_filename(
            orig_file_name=file.filename,
            project_id=project_id
        )
    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": "invalid_project_id"},
        )
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while True:
                chunk = await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE)
                if not chunk:
                    break
                await f.write(chunk)
    except Exception as e:
         logger.error(f"Error While Uploading File: {e}")
         return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value},
                )
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value
        }
    )

