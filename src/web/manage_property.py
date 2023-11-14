import os 
import logging
from fastapi import APIRouter, HTTPException
from service.manage_property import PropertyManagementService

service = PropertyManagementService()

router = APIRouter(prefix = "/manage_property", tags = ["Manage Property"])

@router.get("")
@router.get("/")
def hello():
    return {"message": "Welcome to the Manage property service!"}

@router.post("/process_query", status_code = 200)
def buy_property(user_input: str):
    try:
        response = service.reply_to_manage_property_inquiries(user_input)
        return {"message": response}
    except Exception as ex:
        logging.error(f"Error: {ex}")
        raise HTTPException(status_code=500, detail=f"Error: {ex}")

