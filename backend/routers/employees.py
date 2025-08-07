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
        
@router.get("/names/{user_id}")
def get_employee_names(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("employee_id, name").eq("user_id", user_id).execute()
        if response.data:
            # Return as dictionary: {name: employee_id}
            emp_dict = {emp["name"]: emp["employee_id"] for emp in response.data}
            return {"status": "success", "data": emp_dict}
        else:
            return {"status": "success", "data": {}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/employee-name")
def get_employee_name(user_id: int):
    try:
        emp_info = supabase_client.table("employees") \
            .select("name") \
            .eq("employee_id", user_id) \
            .single() \
            .execute()

        name = emp_info.data.get("name", "Unknown Employee") if emp_info.data else "Unknown Employee"
        return {"name": name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

