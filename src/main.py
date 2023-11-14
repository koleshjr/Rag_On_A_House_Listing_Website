from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web import buy_property,list_property, manage_property, rent_property

app = FastAPI()

#specifies what the backend trusts
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


app.include_router(rent_property.router)
app.include_router(buy_property.router)
app.include_router(manage_property.router)
app.include_router(list_property.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload= True)