from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.candidates import UserResponse, UserResponseDelete, UserResponseInterviews, UserResponseFeedback
from app.api.v1.services import candidates_service
from app.utils.response import success, bad_request, not_found, error
from app.models.candidates import UserRegister, FeedBack, UserStatus, ScheduleInterview
from fastapi.encoders import jsonable_encoder
from app.schemas.pagination import PaginationResponse, FirstResponse

router = APIRouter()

@router.get("/", response_model=PaginationResponse)
async def get_user_all(db: Session = Depends(get_db)):
    try:
        user = candidates_service.get_user_all(db)

        return success(jsonable_encoder(user))
    except Exception as e:
        return error(e)
    
@router.post("/", response_model=FirstResponse)
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        created_by="System"
        new_user = candidates_service.register_user(user_data, created_by, db)

        if new_user == "Email is already registered":
            return bad_request(f"Email {user_data.email} already registered", "Email already registered")

        return success(new_user)
    except Exception as e:
        return error(str(e))

@router.patch("/{id}", response_model=FirstResponse)
async def user_update(id: str, status: UserStatus, db: Session = Depends(get_db)):
    try:
        data_update = {
            "id": id,
            "status": status.status,
            "updated_by": "System"
        }

        if status.status not in ["applied", "interviewing", "hired", "rejected"]:
            return bad_request(f"Status : Only the word [applied, interviewing, hired, rejected] must be present.")
        
        update_user = candidates_service.update_user_by_id(data_update, db)

        if update_user == "User not found":
            return not_found(f"User with ID {id} not found", update_user)
        
        return success(update_user)
    except Exception as e:
        return error(e)

@router.delete("/{id}", response_model=UserResponseDelete)
async def user_delete(id: str, db: Session = Depends(get_db)):
    try:
        data_delete = {
            "id": id,
            "deleted_by": "System"
        }

        delete_user = candidates_service.delete_user_by_id(data_delete, db)

        if delete_user == "User not found":
            return not_found(f"User with ID {id} not found", delete_user)

        return success(delete_user)
    except Exception as e:
        return error(e)
    
@router.post("/{id}/interviews", response_model=UserResponseInterviews)
async def schedule_interview(id: str ,user_data: ScheduleInterview, db: Session = Depends(get_db)):
    try:
        data_update = {
            "id": id,
            "status": "interviewing",
            "interviewer": user_data.interviewer,
            "schedule_interview": user_data.schedule_interview,
            "updated_by": "System"
        }

        if user_data.schedule_interview is None:
            return not_found("Schedule interview not found")
        if user_data.interviewer is None:
            return not_found("Interviewer not found")
        
        new_user = candidates_service.update_interviewing_by_id(data_update, db)

        if new_user == "User not found":
            return not_found(f"User with ID {id} not found", new_user)

        return success(new_user)
    except Exception as e:
        return error(str(e))
    
@router.get("/{id}/interviews", response_model=PaginationResponse)
def get_user_interviews(id: str, db: Session = Depends(get_db)):
    try:
        user = candidates_service.get_user_interviews(id, db)

        if user == "User not found":
            return not_found(f"User with ID {id} not found", user)
        
        return success(jsonable_encoder(user))
    except Exception as e:
        return error(e)

@router.post("/{id}/feedback", response_model=UserResponseFeedback)
async def register_user(id: str ,user_data: FeedBack, db: Session = Depends(get_db)):
    try:
        data_update = {
            "id": id,
            "rating": user_data.rating,
            "updated_by": "System"
        }

        if data_update["rating"] is None:
            return not_found(f"rating not found")
        
        if data_update["rating"] < 1 or data_update["rating"] > 5:
            return bad_request(f"rating 1 to 5")
        
        new_user = candidates_service.update_feedback_by_id(data_update, db)

        if new_user == "Email is already registered":
            return bad_request(f"Email {user_data.email} already registered", "Email already registered")

        return success(new_user)
    except Exception as e:
        return error(str(e))
    
@router.get("/{id}/feedback", response_model=PaginationResponse)
def get_user_feedback(id: str, db: Session = Depends(get_db)):
    try:
        user = candidates_service.get_user_by_id(id, db)

        if user == "User not found":
            return not_found(f"User with ID {id} not found", user)
        
        return success(jsonable_encoder(user))
    except Exception as e:
        return error(e)