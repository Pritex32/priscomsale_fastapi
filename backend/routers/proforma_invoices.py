from fastapi import APIRouter, Depends, HTTPException
from models.proforma_model import ProformaInvoiceRequest
from supabase_service import supabase_client
from security import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])

TABLE_NAME = "proforma_invoices"

# ✅ Create a new proforma invoice
@router.post("/create")
def create_proforma_invoice(entry: ProformaInvoiceRequest):
    try:
        data = entry.dict()
        response = supabase_client.table(TABLE_NAME).insert(data).execute()

        if response.data:
            return {"status": "success", "message": "Proforma invoice created", "data": response.data}
        else:
            raise HTTPException(status_code=400, detail="Failed to insert proforma invoice")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch all invoices for a user
@router.get("/list/{user_id}")
def list_proforma_invoices(user_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Fetch a single proforma invoice by ID
@router.get("/{proforma_id}")
def get_proforma_invoice(proforma_id: int):
    try:
        response = supabase_client.table(TABLE_NAME).select("*").eq("proforma_id", proforma_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Proforma invoice not found")
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
