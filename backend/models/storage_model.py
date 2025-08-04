from pydantic import BaseModel

class FileUploadResponse(BaseModel):
    status: str
    public_url: str
