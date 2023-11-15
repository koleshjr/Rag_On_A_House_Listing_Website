import os 
import logging
from fastapi import APIRouter, HTTPException
from service.rent_property import RentingService

service = RentingService()

router = APIRouter(prefix = "/rent_property", tags = ["Rent Property"])

@router.get("")
@router.get("/")
def hello():
    return {"message": "Welcome to the rent property service!"}

@router.post("/process_query", status_code = 200)
def rent_property(user_input: str):
    try:
        response = service.reply_to_rent_inquiries(user_input)
        return {"message": response}
    except Exception as ex:
        logging.error(f"Error: {ex}")
        raise HTTPException(status_code=500, detail=f"Error: {ex}")

