from fastapi import FastAPI
from model_dto import CustomException
from exception_handler import exception_handler
from router import router


app = FastAPI()



app.add_exception_handler(CustomException, exception_handler)

app.include_router(router)
