from fastapi import APIRouter, Depends, UploadFile, status, File, Request
from fastapi.responses import JSONResponse
from typing import List
import aiofiles
import logging
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController,ProcessController
from models import ResponseSignal
from .schemes.data import ProcessRequest

from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk
from models.AssetModel import AssetModel
from models.db_schemes import DataChunk, Asset
from models.enums.AssetTypeEnum import AssetTypeEnum


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    request: Request,
    project_id: str,
    files: List[UploadFile] = File(...),
    app_settings: Settings = Depends(get_settings)
):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    data_controller = DataController()

    asset_model = await AssetModel.create_instance(
        db_client=request.app.db_client
    )

    uploaded_files = []

    for file in files:

        # validate
        is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

        if not is_valid:
            continue

        file_path, file_id = data_controller.generate_unique_filepath(
            orig_file_name=file.filename,
            project_id=project_id
        )

        try:
            async with aiofiles.open(file_path, "wb") as f:
                while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)

            asset_resource = Asset(
                asset_project_id=project.id,
                asset_type=AssetTypeEnum.FILE.value,
                asset_name=file_id,
                asset_size=os.path.getsize(file_path)
            )

            asset_record = await asset_model.create_asset(asset=asset_resource)

            uploaded_files.append({
                "asset_id": str(asset_record.id),
                "file_id": file_id,
                "file_name": file.filename,
                "file_size": os.path.getsize(file_path)
            })

        except Exception as e:
            logger.error(e)

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "total_files": len(uploaded_files),
            "uploaded_files": uploaded_files
        }
    )
    

@data_router.post("/process/{project_id}")
async def process_endpoint(
    request: Request,
    project_id: str,
    process_request: ProcessRequest
):
    # -------------------------------------------------------
    # Project
    # -------------------------------------------------------
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    asset_model = await AssetModel.create_instance(
        db_client=request.app.db_client
    )

    process_controller = ProcessController(
        project_id=project_id
    )

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    # -------------------------------------------------------
    # Reset chunks
    # -------------------------------------------------------
    if process_request.do_reset == 1:
        await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

    # -------------------------------------------------------
    # Get Assets
    # -------------------------------------------------------
    project_files = await asset_model.get_all_project_assets(
        asset_project_id=project.id,
        asset_type=AssetTypeEnum.FILE.value,
    )

    if process_request.file_id:
        project_files = [
            asset
            for asset in project_files
            if asset.asset_name == process_request.file_id
        ]

    if len(project_files) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.NO_FILES_ERROR.value
            }
        )

    inserted_chunks = 0
    processed_files = []

    print("=" * 60)
    print("Processing Files")
    print("=" * 60)

    # -------------------------------------------------------
    # Process every file
    # -------------------------------------------------------
    for asset in project_files:

        file_path = os.path.join(
            process_controller.project_path,
            asset.asset_name
        )

        # Skip missing files
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {asset.asset_name}")

            processed_files.append({
                "asset_id": str(asset.id),
                "file_id": asset.asset_name,
                "status": "missing"
            })
            continue

        try:

            file_content = process_controller.get_file_content(
                file_id=asset.asset_name
            )

            if not file_content:
                logger.warning(f"No content loaded: {asset.asset_name}")

                processed_files.append({
                    "asset_id": str(asset.id),
                    "file_id": asset.asset_name,
                    "status": "empty"
                })
                continue

            file_chunks = process_controller.process_file_content(
                file_content=file_content,
                file_id=asset.asset_name,
                chunk_size=process_request.chunk_size,
                overlap_size=process_request.overlap_size
            )

            if len(file_chunks) == 0:
                logger.warning(f"No chunks: {asset.asset_name}")

                processed_files.append({
                    "asset_id": str(asset.id),
                    "file_id": asset.asset_name,
                    "status": "no_chunks"
                })
                continue

            chunk_records = [
                DataChunk(
                    chunk_text=chunk.page_content,
                    chunk_metadata=chunk.metadata,
                    chunk_order=i + 1,
                    chunk_project_id=project.id,
                    chunk_asset_id=asset.id
                )
                for i, chunk in enumerate(file_chunks)
            ]

            inserted = await chunk_model.insert_many_chunks(
                chunks=chunk_records
            )

            inserted_chunks += inserted

            processed_files.append({
                "asset_id": str(asset.id),
                "file_id": asset.asset_name,
                "extension": os.path.splitext(asset.asset_name)[1],
                "documents_loaded": len(file_content),
                "chunks_generated": len(file_chunks),
                "inserted_chunks": inserted,
                "status": "success"
            })

            print(f"✓ {asset.asset_name} -> {inserted} chunks")

        except Exception as e:

            logger.exception(e)

            processed_files.append({
                "asset_id": str(asset.id),
                "file_id": asset.asset_name,
                "status": "failed",
                "error": str(e)
            })

    # -------------------------------------------------------
    # Response
    # -------------------------------------------------------
    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "project_id": project_id,
            "chunk_size": process_request.chunk_size,
            "overlap_size": process_request.overlap_size,
            "total_files": len(project_files),
            "processed_successfully": len(
                [x for x in processed_files if x["status"] == "success"]
            ),
            "inserted_chunks": inserted_chunks,
            "processed_files": processed_files
        }
    )