from fastapi import Depends, FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import dotenv
import os
from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users
from .services import coe_scanner

app = FastAPI(dependencies=[Depends(get_query_token)])
dotenv.load_dotenv()
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

@app.post("/parse-coe")
async def parse_coe(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return {"error": "File must be a PDF"}
    
    return await coe_scanner.process_pdf(file.file)