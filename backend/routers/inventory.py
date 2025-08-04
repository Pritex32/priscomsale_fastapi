from fastapi import APIRouter, HTTPException, Depends
from models.inventory_model import InventoryRequest
from supabase_service import supabase_client
from security import verify_api_key
from datetime import datetime

router = APIRouter(dependencies=[Depends(verify_api_key)])

TABLE_NAME = "inventory_master_log"

# ✅ Create Inventory Record
@router.post("/create")
def create_inventory_record(inventory: InventoryRequest):
    try:
        data = inventory.dict()
        # Add last_updated timestamp
        data["last_updated"] = datetime.utcnow().isoformat()

        response = supabase_client.table(TABLE_NAME).insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Inventory record created", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to create inventory record")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get Inventory by User
@router.get("/list/{user_id}")
def get_inventory_by_user(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Get Inventory by Item ID
@router.get("/item/{item_id}")
def get_inventory_by_item(item_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("item_id", item_id).execute()
        if response.data:
            return {"status": "success", "data": response.data}
        else:
            raise HTTPException(status_code=404, detail="Item not found in inventory")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Update Inventory Record
@router.put("/update/{user_id}")
def update_inventory(user_id: int, inventory: InventoryRequest):
    try:
        data = inventory.dict()
        data["last_updated"] = datetime.utcnow().isoformat()

        response = supabase_client.table(TABLE_NAME).update(data).eq("user_id", user_id).execute()

        if response.data:
            return {"status": "success", "message": "Inventory record updated", "data": response.data}
        else:
            raise HTTPException(status_code=404, detail="Inventory record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete Inventory Record
@router.delete("/delete/{id}")
def delete_inventory(id: int):
    try:
        response = supabase_client.table(TABLE_NAME).delete().eq("user_id", user_id).execute()
        if response.data:
            return {"status": "success", "message": "Inventory record deleted"}
        else:
            raise HTTPException(status_code=404, detail="Inventory record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
