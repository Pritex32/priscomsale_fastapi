from fastapi import APIRouter, HTTPException, Depends
from models.employee_model import EmployeeRequest
from supabase_service import supabase_client
from security import verify_api_key
from datetime import datetime

router = APIRouter(dependencies=[Depends(verify_api_key)])

TABLE_NAME = "employees"

# ✅ Create new employee
@router.post("/create")
def create_employee(employee: EmployeeRequest):
    try:
        data = employee.dict()
        data["created_at"] = datetime.utcnow().isoformat()

        response = supabase_client.table(TABLE_NAME).insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Employee created", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to create employee")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get all employees for a user
@router.get("/list/{user_id}")
def get_employees(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get single employee by ID
@router.get("/{employee_id}")
def get_employee(employee_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("employee_id", employee_id).execute()
        if response.data:
            return {"status": "success", "data": response.data}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Update employee
@router.put("/update/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeRequest):
    try:
        data = employee.dict()
        data["created_at"] = datetime.utcnow().isoformat()

        response = supabase_client.table(TABLE_NAME).update(data).eq("employee_id", employee_id).execute()
        if response.data:
            return {"status": "success", "message": "Employee updated", "data": response.data}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete employee
@router.delete("/delete/{employee_id}")
def delete_employee(employee_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).delete().eq("employee_id", employee_id).execute()
        if response.data:
            return {"status": "success", "message": "Employee deleted"}
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
