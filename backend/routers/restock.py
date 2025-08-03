from fastapi import APIRouter, Depends, HTTPException
from models.restock_model import RestockRequest
from services.supabase_service import supabase_client
from security import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

# ✅ Create a new restock entry in goods_bought
@router.post("/create")
def create_restock(restock: RestockRequest):
    try:
        data = restock.dict()
        response = supabase_client.table("goods_bought").insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Restock added", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to insert restock")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Fetch active restocks from goods_bought
@router.get("/active/{user_id}")
def get_active_restocks(user_id: int):
    try:
        response = supabase_client.table("goods_bought").select("*").eq("user_id", user_id).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Fetch historical restocks from goods_bought_history
@router.get("/history/{user_id}")
def get_restock_history(user_id: int):
    try:
        response = supabase_client.table("goods_bought_history").select("*").eq("user_id", user_id).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
