from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

from config import settings
from rag.ingest import ingest_file
from rag.chroma_manager import get_vectorstore


router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    destination = Path(settings.upload_dir) / file.filename
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_result = ingest_file(str(destination))

    return {
        "filename": file.filename,
        "status": "uploaded",
        **ingest_result,
    }


@router.get("/files")
def list_files():
    files = []
    upload_path = Path(settings.upload_dir)
    if upload_path.exists():
        for p in upload_path.iterdir():
            if p.is_file():
                files.append({
                    "filename": p.name,
                    "size": p.stat().st_size,
                    "path": str(p),
                })
    return {"files": files}


@router.delete("/files/{filename}")
def delete_file(filename: str):
    target = Path(settings.upload_dir) / filename
    if not target.exists():
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    
    # Delete from filesystem
    try:
        target.unlink()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not delete file: {e}")
        
    # Delete from mock vectorstore
    vectorstore = get_vectorstore()
    vectorstore.delete_document(filename)
    
    return {
        "filename": filename,
        "status": "deleted",
    }

