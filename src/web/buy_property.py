import os 
import logging
from fastapi import APIRouter, HTTPException
from service.buy_property import BuyingService

service = BuyingService()

router = APIRouter(prefix = "/buy_property", tags = ["Buy Property"])

@router.get("")
@router.get("/")
def hello():
    return {"message": "Welcome to the buy property service!"}

@router.post("/process_query", status_code = 200)
def buy_property(user_input: str):
    try:
        response = service.reply_to_buy_property_queries(user_input)
        return {"message": response}
    except Exception as ex:
        logging.error(f"Error: {ex}")
        raise HTTPException(status_code=500, detail=f"Error: {ex}")

