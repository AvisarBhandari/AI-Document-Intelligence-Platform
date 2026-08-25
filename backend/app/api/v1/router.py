from app.api.v1 import auth, documents, user
from fastapi import APIRouter

api_v1_router = APIRouter()

# Register sub-routers with clean, logical endpoints
api_v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(user.router, prefix="/users", tags=["Users"])
api_v1_router.include_router(
    documents.router, prefix="/documents", tags=["RAG / Documents"]
)
