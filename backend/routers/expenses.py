from fastapi import APIRouter, Depends, HTTPException
from models.expense_model import ExpenseRequest
from services.supabase_service import supabase_client
from security import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

# ✅ 1. Create a new expense
@router.post("/create")
def create_expense(expense: ExpenseRequest):
    try:
        data = expense.dict()
        response = supabase_client.table("expenses_master").insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Expense added", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to insert expense")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ 2. Get all expenses for a user
@router.get("/history/{user_id}")
def get_expense_history(user_id: int):
    try:
        response = supabase_client.table("expenses_master").select("*").eq("user_id", user_id).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ 3. Get expense by ID
@router.get("/{expense_id}")
def get_expense_by_id(expense_id: int):
    try:
        response = supabase_client.table("expenses_master").select("*").eq("expense_id", expense_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Expense not found")
        return {"status": "success", "data": response.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
