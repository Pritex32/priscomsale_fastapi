from fastapi import APIRouter, HTTPException, Depends
from models.subscription_model import SubscriptionRequest
from supabase_service import supabase_client
from security import verify_api_key
from datetime import datetime

router = APIRouter(dependencies=[Depends(verify_api_key)])

TABLE_NAME = "subscription"

# ✅ Create a new subscription
@router.post("/create")
def create_subscription(sub: SubscriptionRequest):
    try:
        data = sub.dict()
        data["started_at"] = datetime.utcnow().isoformat()
        if not data.get("status"):
            data["status"] = "pending"

        response = supabase_client.table(TABLE_NAME).insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Subscription created", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to create subscription")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get all subscriptions for a user
@router.get("/list/{user_id}")
def get_subscriptions(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get active subscription for a user
@router.get("/active/{user_id}")
def get_active_subscription(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).eq("is_active", True).execute()
        if response.data:
            return {"status": "success", "data": response.data[0]}  # Return latest active subscription
        else:
            return {"status": "success", "data": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Update subscription status
@router.put("/update/{id}")
def update_subscription(id: int, sub: SubscriptionRequest):
    try:
        data = sub.dict(exclude_unset=True)
        response = supabase_client.table(TABLE_NAME).update(data).eq("id", id).execute()
        if response.data:
            return {"status": "success", "message": "Subscription updated", "data": response.data}
        else:
            raise HTTPException(status_code=404, detail="Subscription not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete subscription
@router.delete("/delete/{id}")
def delete_subscription(id: int):
    try:
        response = supabase_client.table(TABLE_NAME).delete().eq("id", id).execute()
        if response.data:
            return {"status": "success", "message": "Subscription deleted"}
        else:
            raise HTTPException(status_code=404, detail="Subscription not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
