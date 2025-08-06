from supabase import create_client
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

supabase_url = 'https://ecsrlqvifparesxakokl.supabase.co' # Your Supabase project URL
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjc3JscXZpZnBhcmVzeGFrb2tsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ2NjczMDMsImV4cCI6MjA2MDI0MzMwM30.Zts7p1C3MNFqYYzp-wo3e0z-9MLfRDoY2YJ5cxSexHk'
   
supabase_client = create_client(supabase_url, supabase_key)

from fastapi import HTTPException

def handle_supabase_response(response, success_message="Operation successful"):
    """
    Handles Supabase responses and raises proper HTTP errors.
    """
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)

    if not response.data:
        raise HTTPException(status_code=404, detail="No data found")

    return {"status": "success", "message": success_message, "data": response.data}

       
