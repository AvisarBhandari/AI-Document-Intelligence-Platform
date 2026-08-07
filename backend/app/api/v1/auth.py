from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
async def login():
    return("Login Successfull")

@router.post("/register")
async def register():
    return("Register Successfull")