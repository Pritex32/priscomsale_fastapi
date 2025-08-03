from fastapi import APIRouter, Depends, HTTPException
from models.payment_model import PaymentRequest
from supabase_service import supabase_client

from security import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

# ✅ 1. Create a new payment
@router.post("/create")
def create_payment(payment: PaymentRequest):
    try:
        data = payment.dict()
        response = supabase_client.table("payments").insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Payment added", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to insert payment")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ 2. Get all payments for a user
@router.get("/history/{user_id}")
def get_payment_history(user_id: int):
    try:
        response = supabase_client.table("payments").select("*").eq("user_id", user_id).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ 3. Get payment by payment_id
@router.get("/{payment_id}")
def get_payment_by_id(payment_id: int):
    try:
        response = supabase_client.table("payments").select("*").eq("payment_id", payment_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Payment not found")
        return {"status": "success", "data": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

