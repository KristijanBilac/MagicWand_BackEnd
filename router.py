from fastapi import APIRouter, Depends, Response
from authentication_handler import login_user_token, get_token
from model_dto import MagicWandDTO, UserOut, UserIn
from sqlalchemy.orm import Session
from database import get_db
from service import get_specific_magic_wand, create_new_magic_wand, create_user, \
    get_all_limited_magic_wands_with_owner, get_all_magic_wands_with_owner

router = APIRouter()


@router.get("/api/v1/magic_wand/{id}", tags=["magic_wand"])
async def get_magic_wand_details(id: int, token: str = Depends(get_token), db: Session = Depends(get_db)):
    return await get_specific_magic_wand(id, token, db)


@router.get("/api/v1/magic_wands", tags=["magic_wand"])
async def all_magic_wands(token: str = Depends(get_token), db: Session = Depends(get_db)):
    return await get_all_magic_wands_with_owner(token, db)


@router.get("/api/v1/magic_wands_limited", tags=["magic_wand"])
async def all_magic_wands(db: Session = Depends(get_db)):
    return await get_all_limited_magic_wands_with_owner(db)


@router.post("/api/v1/magic_wand", response_model=MagicWandDTO, tags=["magic_wand"])
async def add_magic_wand(new_magic_wand: MagicWandDTO, token: str = Depends(get_token), db: Session = Depends(get_db)):
    return await create_new_magic_wand(new_magic_wand, token, db)


@router.post("/api/v1/user/sing-up", response_model=UserOut, tags=["user"])
async def user_sing_up(user: UserIn, db: Session = Depends(get_db)):
    return await create_user(user, db)


@router.post("/api/v1/user/login", tags=["user"])
async def user_login(response: Response, user: UserIn, db: Session = Depends(get_db)):
    access_token = await login_user_token(user, db)
    response.set_cookie(key="session_token", value=f"Bearer {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}
