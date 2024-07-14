from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.vectorize import api_bert
from api.llm import api_gemma2

router = APIRouter()

@router.post("/vectorize/bert")
async def vectorize(request: api_bert.ApiBertRequest):
    return api_bert.handle(request)

@router.post("/llm/gemma2")
async def vectorize(request: api_bert.ApiBertRequest):
    return api_gemma2.handle(request)