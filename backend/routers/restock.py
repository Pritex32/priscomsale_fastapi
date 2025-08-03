
from fastapi import APIRouter, Depends, HTTPException
from models.restock_model import RestockRequest
from services.supabase_service import supabase_client
from security import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

# ✅ Create a new restock (purchase entry)
@router.post("/create")
def create_restock(restock: RestockRequest):
    try:
        data = restock.dict()
        response = supabase_client.table("goods_bought_history").insert(data).execute()

        if response.data:
            return {"status": "success", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to insert restock record")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get all restocks for a user
@router.get("/history/{user_id}")
def get_restock_history(user_id: int):
    try:
        response = supabase_client.table("goods_bought_history").select("*").eq("user_id", user_id).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
