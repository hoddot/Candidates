from sqlalchemy.orm import Session, selectinload
from app.models.candidates import User, UserRegister, Interview, Feedback
from sqlalchemy import or_
from app.core.config import bangkok_now
from app.utils.response import error
import uuid
from datetime import datetime
from sqlalchemy import text, inspect, exc
from app.core.database import engine, Base

def init_and_ping():
    # 1) สร้างตารางทั้งหมด (ถ้ายังไม่มี)
    Base.metadata.create_all(bind=engine)

    # 2) ping แบบเร็ว ๆ
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ SQLite connection OK")

        # 3) แสดงรายชื่อตาราง
        tables = inspect(engine).get_table_names()
        print(f"Tables found: {tables}")
    except exc.SQLAlchemyError as e:
        print(f"❌ DB connection failed: {e}")

def get_user_all(db: Session):
    try:
        users = (
            db.query(User)
            .options(selectinload(User.interviews))
            .options(selectinload(User.feedbacks))
            .filter(User.active == 1)
            .all()
        )

        result_user = [
            {
                "id": u.id,
                "email": u.email,
                "name": u.name,
                "position": u.position,
                "status": u.status,
                "created_date": u.created_date.strftime("%Y-%m-%d %H:%M:%S") if u.created_date else None,
                "active": u.active,
                "interviews":
                    {
                        "interviewer": u.interviews[0].interviewer,
                        "scheduled_at": u.interviews[0].scheduled_at.strftime("%Y-%m-%d %H:%M:%S")
                        if u.interviews[0].scheduled_at else None
                    }
                if u.interviews else [],
                "feedbacks":
                    {
                        "rating": u.feedbacks[0].rating
                    }
                if u.feedbacks else []
            }
            for u in users
        ]

        result = {
            "users": result_user
        }
        return result
    except Exception as e:
        return {"message": str(e)}

def get_user_interviews(id: str, db: Session):
    try:
        users = (
            db.query(User)
            .join(User.interviews)
            .join(User.feedbacks)
            .filter(
                User.id == id,
                User.active == 1,
                Interview.interviewer.isnot(None)   # interviewer != NULL
            )
            .options(selectinload(User.interviews))
            .options(selectinload(User.feedbacks))
            .all()
        )

        if not users:
            return "User not found"
        
        result_user = [
            {
                "id": u.id,
                "email": u.email,
                "name": u.name,
                "position": u.position,
                "status": u.status,
                "created_date": u.created_date.strftime("%Y-%m-%d %H:%M:%S") if u.created_date else None,
                "active": u.active,
                "interviews":
                    {
                        "interviewer": u.interviews[0].interviewer,
                        "scheduled_at": u.interviews[0].scheduled_at.strftime("%Y-%m-%d %H:%M:%S")
                        if u.interviews[0].scheduled_at else None,
                    }
                if u.interviews else [],
                "feedbacks":
                    {
                        "rating": u.feedbacks[0].rating
                    }
                if u.feedbacks else []
            }
            for u in users
        ]

        result = {
            "users": result_user
        }
        return result
    except Exception as e:
        return {"message": str(e)}
    
def get_user_by_id(id: str, db: Session):
    try:
        users = (
            db.query(User)
            .join(User.interviews)
            .join(User.feedbacks)
            .filter(
                User.id == id,
                User.active == 1
            )
            .options(selectinload(User.interviews))
            .options(selectinload(User.feedbacks))
            .all()
        )

        if not users:
            return "User not found"
        
        result_user = [
            {
                "id": u.id,
                "email": u.email,
                "name": u.name,
                "position": u.position,
                "status": u.status,
                "created_date": u.created_date.strftime("%Y-%m-%d %H:%M:%S") if u.created_date else None,
                "active": u.active,
                "interviews":
                    {
                        "interviewer": u.interviews[0].interviewer,
                        "scheduled_at": u.interviews[0].scheduled_at.strftime("%Y-%m-%d %H:%M:%S")
                        if u.interviews[0].scheduled_at else None,
                    }
                if u.interviews else [],
                "feedbacks":
                    {
                        "rating": u.feedbacks[0].rating
                    }
                if u.feedbacks else []
            }
            for u in users
        ]

        result = {
            "users": result_user
        }
        return result
    except Exception as e:
        return {"message": str(e)}

def get_user_by_email(email: str, db: Session):
    try:
        user = db.query(User).filter(
            User.email == email,
            User.active == 1
        ).first()
        return user
    except Exception as e:
        return {"message": str(e)}

def register_user(user_obj: UserRegister, created_by: str, db: Session):
    try:
        existing_user = get_user_by_email(user_obj.email, db)
        if existing_user:
            return "Email is already registered"
        
        id_uuid4 = uuid.uuid4()
        user_candidate = User(
            id=str(id_uuid4),
            email=user_obj.email,
            name=user_obj.name,
            position=user_obj.position,
            status="applied",
            created_by=created_by
        )

        user_interview = Interview(
            candidate_id=str(id_uuid4),
        )

        user_feedback = Feedback(
            candidate_id=str(id_uuid4),
        )

        db.add(user_candidate)
        db.add(user_interview)
        db.add(user_feedback)
        db.commit()
        db.refresh(user_candidate) 

        user_interview = user_candidate.interviews[0] if user_candidate.interviews else None
        user_feedbacks = user_candidate.feedbacks[0]  if user_candidate.feedbacks  else None

        return {
                "id": user_candidate.id,
                "email": user_candidate.email,
                "name": user_candidate.name,
                "position": user_candidate.position,
                "status": user_candidate.status,
                "created_date": user_candidate.created_date.strftime("%Y-%m-%d %H:%M:%S") if user_candidate.created_date else None,
                "active": user_candidate.active,
                "interviews": {
                    "interviewer":  user_interview.interviewer if user_interview else None,
                    "scheduled_at": user_interview.scheduled_at if user_interview else None,
                } if user_interview else {},
                "feedbacks": {
                    "rating": user_feedbacks.rating if user_feedbacks else None,
                } if user_feedbacks else {}
        }
    except Exception as e:
        return error(exception=str(e))
    
def update_user_by_id(data_update: dict, db: Session):
    try:
        user_id = data_update["id"]
        
        user = db.query(User).filter(
            User.id == user_id, 
            User.active == 1
        ).first()
        
        if not user:
            return "User not found"

        if "status" in data_update and data_update["status"] is not None:
            user.status = data_update["status"]
            
        user.updated_by = data_update["updated_by"]
        db.commit()
        db.refresh(user)

        return {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "position": user.position,
                "status": user.status,
                "created_date": user.created_date.strftime("%Y-%m-%d %H:%M:%S") if user.created_date else None,
                "active": user.active
            }
    except Exception as e:
        return {"message": str(e)}

def update_interviewing_by_id(data_update: dict, db: Session):
    try:
        user_id = data_update["id"]
        
        user = db.query(User).filter(
            User.id == user_id, 
            User.active == 1
        ).first()
        
        if not user:
            return "User not found"
        
        interview = db.query(Interview).filter(
            Interview.candidate_id == user_id
        ).first()
        
        user.status = data_update["status"]
        user.updated_by = data_update["updated_by"]
        interview.interviewer = data_update["interviewer"]
        interview.scheduled_at = data_update["schedule_interview"]

        db.commit()
        db.refresh(user)

        return {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "position": user.position,
                "status": user.status,
                "interviewer": data_update["interviewer"],
                "schedule_interview": data_update["schedule_interview"].strftime("%Y-%m-%d %H:%M:%S") if user.created_date else None,
                "created_date": user.created_date.strftime("%Y-%m-%d %H:%M:%S") if user.created_date else None,
                "active": user.active
            }
    except Exception as e:
        return {"message": str(e)}

def update_feedback_by_id(data_update: dict, db: Session):
    try:
        user_id = data_update["id"]
        
        user = db.query(User).filter(
            User.id == user_id, 
            User.active == 1
        ).first()
        
        if not user:
            return "User not found"

        feedback = db.query(Feedback).filter(
            Feedback.candidate_id == user_id
        ).first()

        feedback.rating = data_update["rating"]

        db.commit()
        db.refresh(user)

        return {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "position": user.position,
                "status": user.status,
                "rating": data_update["rating"],
                "created_date": user.created_date.strftime("%Y-%m-%d %H:%M:%S") if user.created_date else None,
                "active": user.active
            }
    except Exception as e:
        return error({"message": str(e)})
    
def delete_user_by_id(data_delete: object, db: Session):
    try:
        user_id = data_delete["id"]

        user = db.query(User).filter(
            User.id == user_id, 
            User.active == 1
        ).first()
        
        if not user:
            return "User not found"

        # บันทึกผู้แก้ไขล่าสุด
        user.active = 0
        user.deleted_by = data_delete["deleted_by"]
        user.deleted_date = bangkok_now()

        db.commit()
        db.refresh(user)
        return {
                "id": user.id,
                "active": user.active
        }
    except Exception as e:
        return {"message": str(e)}
