from fastapi import APIRouter

router = APIRouter()


@router.post("/upload", status_code=202)
async def upload_document():
    return("Upload","TEST")