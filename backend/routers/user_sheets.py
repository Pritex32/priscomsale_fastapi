from fastapi import APIRouter, Depends, HTTPException
from models.user_sheets_model import UserSheetRequest
from supabase_service import supabase_client
from security import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

TABLE_NAME = "user_sheets"

# ✅ Create a new user sheet
@router.post("/create")
def create_user_sheet(sheet: UserSheetRequest):
    try:
        data = sheet.dict()
        response = supabase_client.table(TABLE_NAME).insert(data).execute()

        if response.data:
            return {"status": "success", "message": "User sheet created", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to insert user sheet")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch all sheets for a user
@router.get("/list/{user_id}")
def list_user_sheets(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch a single sheet by ID
@router.get("/{sheet_id}")
def get_user_sheet(sheet_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("id", sheet_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Sheet not found")
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
