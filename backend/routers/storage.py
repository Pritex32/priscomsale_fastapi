from fastapi import APIRouter, File, UploadFile, HTTPException
from supabase_service import supabase_client
from models.storage_model import FileUploadResponse

router = APIRouter(prefix="/api/storage", tags=["Storage"])

BUCKET_NAME = "salesinvoices"  # Ensure this bucket exists in Supabase

@router.post("/upload/{folder}/{filename}", response_model=FileUploadResponse)
async def upload_file(folder: str, filename: str, file: UploadFile = File(...)):
    try:
        # Path inside the bucket
        path_in_bucket = f"{folder}/{filename}"

        # Upload file to Supabase
        response = supabase_client.storage.from_(BUCKET_NAME).upload(
            path_in_bucket, file.file, {"content-type": file.content_type}
        )

        # Handle Supabase error
        if isinstance(response, dict) and response.get("error"):
            error_message = response["error"].get("message", "Upload failed")
            status_code = response["error"].get("statusCode", 500)
            raise HTTPException(status_code=status_code, detail=error_message)

        # Get public URL
        public_url = supabase_client.storage.from_(BUCKET_NAME).get_public_url(path_in_bucket)

        return FileUploadResponse(status="success", public_url=public_url)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
