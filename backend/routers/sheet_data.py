from fastapi import APIRouter, Depends, HTTPException
from models.sheet_data_model import SheetDataRequest
from supabase_service import supabase_client
from security import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

TABLE_NAME = "sheet_data"

# ✅ Create a new sheet data entry
@router.post("/create")
def create_sheet_data(entry: SheetDataRequest):
    try:
        data = entry.dict()
        response = supabase_client.table(TABLE_NAME).insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Sheet data added", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to insert sheet data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch all data for a specific sheet by user_id
@router.get("/list/{user_id}/{sheet_name}")
def list_sheet_data(user_id: int, sheet_name: str):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).eq("sheet_name", sheet_name).order("created_at", desc=True).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch a single data record by ID
@router.get("/{record_id}")
def get_sheet_data(record_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("id", record_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
