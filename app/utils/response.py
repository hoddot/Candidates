from datetime import datetime
import pytz
from fastapi.responses import JSONResponse
from starlette import status

def current_timestamp():
    bangkok_tz = pytz.timezone("Asia/Bangkok")
    return datetime.now(bangkok_tz).strftime("%Y-%m-%d %H:%M:%S")

def success(data=None, message="Success"):
    content = {
        "message": message,
        "data": data,
        "exception": None,
        "meta": {
            "timestamp": current_timestamp()
        }
    }
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content
    )

def error(exception=None, message="An error occurred", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    content = {
        "message": message,
        "data": None,
        "exception": exception,
        "meta": {
            "timestamp": current_timestamp()
        }
    }
    return JSONResponse(
        status_code=status_code,
        content=content
    )

def not_found(exception="Not found", message="Not Found"):
    return error(
        exception=exception, 
        message=message, 
        status_code=status.HTTP_404_NOT_FOUND
    )

def bad_request(exception="Bad request", message="Bad Request"):
    return error(
        exception=exception, 
        message=message, 
        status_code=status.HTTP_400_BAD_REQUEST
    )

def unauthorize(exception="Unauthorized", message="Unauthorized"):
    return error(
        exception=exception, 
        message=message, 
        status_code=status.HTTP_401_UNAUTHORIZED
    )

def forbidden(exception="Forbidden", message="Forbidden"):
    return error(
        exception=exception, 
        message=message, 
        status_code=status.HTTP_403_FORBIDDEN
    )