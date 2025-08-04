from fastapi import APIRouter, HTTPException, Depends
from models.customer_model import CustomerRequest
from supabase_service import supabase_client
from security import verify_api_key
from datetime import datetime

router = APIRouter(dependencies=[Depends(verify_api_key)])

TABLE_NAME = "customers"

# ✅ Create a new customer
@router.post("/create")
def create_customer(customer: CustomerRequest):
    try:
        data = customer.dict()
        data["created_at"] = datetime.utcnow().isoformat()

        response = supabase_client.table(TABLE_NAME).insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Customer created", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to create customer")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get all customers for a user
@router.get("/list/{user_id}")
def get_customers(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get single customer by ID
@router.get("/{customer_id}")
def get_customer(customer_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("customer_id", customer_id).execute()
        if response.data:
            return {"status": "success", "data": response.data[0]}
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Update customer details
@router.put("/update/{customer_id}")
def update_customer(customer_id: int, customer: CustomerRequest):
    try:
        data = customer.dict(exclude_unset=True)
        response = supabase_client.table(TABLE_NAME).update(data).eq("customer_id", customer_id).execute()

        if response.data:
            return {"status": "success", "message": "Customer updated", "data": response.data}
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete customer
@router.delete("/delete/{customer_id}")
def delete_customer(customer_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).delete().eq("customer_id", customer_id).execute()
        if response.data:
            return {"status": "success", "message": "Customer deleted"}
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
