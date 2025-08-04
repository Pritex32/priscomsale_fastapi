from fastapi import APIRouter, HTTPException, Depends
from models.user_model import UserRequest
from supabase_service import supabase_client
from security import verify_api_key
from datetime import datetime
from utils.hashing import hash_password  # Custom utility for hashing

router = APIRouter(dependencies=[Depends(verify_api_key)])

TABLE_NAME = "users"

# ✅ Create User (Register)
@router.post("/create")
def create_user(user: UserRequest):
    try:
        data = user.dict()
        data["created_at"] = datetime.utcnow().isoformat()

        # ✅ Hash the password before storing
        if "password_hash" in data and data["password_hash"]:
            data["password_hash"] = hash_password(data["password_hash"])

        response = supabase_client.table(TABLE_NAME).insert(data).execute()

        if response.data:
            return {"status": "success", "message": "User created successfully", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get All Users
@router.get("/list")
def get_all_users():
    try:
        response = supabase_client.table(TABLE_NAME).select("*").execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get Single User by ID
@router.get("/{user_id}")
def get_user(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).execute()
        if response.data:
            return {"status": "success", "data": response.data}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Update User
@router.put("/update/{user_id}")
def update_user(user_id: int, user: UserRequest):
    try:
        data = user.dict(exclude_unset=True)

        # Update created_at only if not present
        if "created_at" not in data:
            data["created_at"] = datetime.utcnow().isoformat()

        # ✅ Hash password if updating it
        if "password_hash" in data and data["password_hash"]:
            data["password_hash"] = hash_password(data["password_hash"])

        response = supabase_client.table(TABLE_NAME).update(data).eq("user_id", user_id).execute()

        if response.data:
            return {"status": "success", "message": "User updated", "data": response.data}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete User (Soft Delete)
@router.delete("/delete/{user_id}")
def delete_user(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).update({"deleted": True}).eq("user_id", user_id).execute()
        if response.data:
            return {"status": "success", "message": "User deleted"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
