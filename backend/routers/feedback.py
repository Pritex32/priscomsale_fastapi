from fastapi import APIRouter, Depends, HTTPException
from models.feedback_model import FeedbackRequest
from supabase_service import supabase_client
from security import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

TABLE_NAME = "feedback"

# ✅ Create new feedback
@router.post("/create")
def create_feedback(entry: FeedbackRequest):
    try:
        data = entry.dict()
        response = supabase_client.table(TABLE_NAME).insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Feedback submitted", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to insert feedback")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch all feedback for a user
@router.get("/user/{user_id}")
def get_feedback_by_user(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch all feedback (admin view)
@router.get("/all")
def get_all_feedback():
    try:
        response = supabase_client.table(TABLE_NAME).select("*").order("created_at", desc=True).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
