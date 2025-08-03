from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = "12344567889sdfgg"

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
