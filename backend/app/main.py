from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router

# import database
from app.core.database import Base, engine
from app.core.exceptions import setup_exception_handlers
from app.models.user import User

# to create SQLAlchemy to create all missing table in the database
Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Document Intelligence Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")
setup_exception_handlers(app)


@app.get("/")
async def root():
    return {"status": "healthy", "service": "RAG Document Intelligence Backend"}
