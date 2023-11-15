import os 
import logging
from fastapi import APIRouter, HTTPException
from service.list_property import ListingService

service = ListingService()

router = APIRouter(prefix = "/list_property", tags = ["List Property"])

@router.get("")
@router.get("/")
def hello():
    return {"message": "Welcome to the listing property service!"}

@router.post("/process_query", status_code = 200)
def list_property(user_input: str):
    try:
        response = service.reply_to_list_property_inquiries(user_input)
        return {"message": response}
    except Exception as ex:
        logging.error(f"Error: {ex}")
        raise HTTPException(status_code=500, detail=f"Error: {ex}")

