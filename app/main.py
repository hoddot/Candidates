import uvicorn
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
import os
from app.utils.response import success
from app.api.v1.routes import candidates

# โหลดค่าจากไฟล์ .env
load_dotenv()

PREFIX = "/api/v1"

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

app = FastAPI(title="API Candidates Project", version="1.0")

api_router = APIRouter()
api_router.include_router(candidates.router, prefix="/candidates", tags=["candidates"])

# app.mount(PREFIX, api_router)
app.include_router(api_router, prefix=PREFIX)

@app.get("/")
def get_root():
    return success("Welcome to FastAPI!")

@app.get("/health")
def health_check():
    return success("OK")

if __name__ == "__main__":
    print(f"----- APP START RUNNING ON PORT {PORT} -----")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
