from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.vectorize import api_bert

router = APIRouter()

@router.post("/vectorize/bert")
async def vectorize(request: api_bert.ApiBertRequest):
    return api_bert.handle(request)
