import uvicorn
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
import os
from app.utils.response import success, not_found, error
from app.api.v1.routes import candidates
from app.api.v1.services import candidates_service
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException

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

candidates_service.init_and_ping()

@app.get("/")
def get_root():
    return success("Welcome to FastAPI!")

@app.get("/health")
def health_check():
    return success("OK")

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return not_found({
            "status_code": exc.status_code,
            "message": "The page you requested was not found. URL : " +str(request.url)
            }
        )
    return error({
        "status_code": exc.status_code,
        "message": exc.detail
        }
    )

if __name__ == "__main__":
    print(f"----- APP START RUNNING ON PORT {PORT} -----")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
