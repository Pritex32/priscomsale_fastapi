from fastapi import APIRouter, Depends, HTTPException
from models.admin_logs_model import AdminLogRequest
from supabase_service import supabase_client
from security import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

TABLE_NAME = "admin_logs"

# ✅ Create a new log entry
@router.post("/create")
def create_admin_log(log: AdminLogRequest):
    try:
        data = log.dict()
        response = supabase_client.table(TABLE_NAME).insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Log added", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to insert log")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch all logs for a specific user
@router.get("/user/{user_id}")
def get_logs_by_user(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).order("timestamp", desc=True).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch all logs (Admin overview)
@router.get("/all")
def get_all_logs():
    try:
        response = supabase_client.table(TABLE_NAME).select("*").order("timestamp", desc=True).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
