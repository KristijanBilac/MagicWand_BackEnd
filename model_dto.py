from http.client import HTTPException
from typing import Optional

from pydantic import BaseModel
from enum import Enum


# DTO - data transfer object
class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str


class UserOwnerOut(BaseModel):
    username: str


class WoodType(str, Enum):
    alder = "alder"
    acacia = "acacia"
    apple = "apple"
    ash = "ash"
    blackthorn = "blackthorn"
    cherry = "cherry"


class MagicWandDTO(BaseModel):
    flexibility: str
    owner: int
    length: int
    wood: WoodType


class MagicWandOutDTO(BaseModel):
    flexibility: str
    owner: UserOwnerOut
    length: int
    wood: WoodType


class CustomException(HTTPException):
    def __init__(self, status_code, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class ErrorResponse(BaseModel):
    detail: str
    status_code: int


class Token(BaseModel):
    access_token: str
    token_type: str


class DataToken(BaseModel):
    id: Optional[str] = None
