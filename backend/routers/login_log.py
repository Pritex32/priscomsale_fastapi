from fastapi import APIRouter, HTTPException
from models.login_log_model import LoginLogRequest
from supabase_service import supabase_client

router = APIRouter()
TABLE_NAME = "login_logs"  # change if your table name is different

# Create login log
@router.post("/create")
def create_login_log(log: LoginLogRequest):
    try:
        data = log.dict()
        response = supabase_client.table(TABLE_NAME).insert(data).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get all login logs (optionally by user_id)
@router.get("/list/{user_id}")
def get_login_logs(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).order("login_time", desc=True).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent_user_logins/{user_id}")
def get_recent_user_logins(user_id: int):
    try:
        logs = supabase_client.table("login_logs") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("login_time", desc=True) \
            .limit(5) \
            .execute()
        return {"status": "success", "data": logs.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/recent_global_logins")
def get_recent_global_logins():
    try:
        result = supabase_client.table("login_logs") \
            .select("user_id, login_time, role, ip_address, device, username") \
            .order("login_time", desc=True) \
            .limit(5) \
            .execute()
        return {"status": "success", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

