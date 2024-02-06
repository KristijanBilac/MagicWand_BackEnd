from fastapi import APIRouter, Depends
from model_dto import MagicWandDTO, UserDTO, UserCreateDTO
from sqlalchemy.orm import Session
from database import get_db
from service import get_specific_magic_wand, create_new_magic_wand, login_user, create_user, \
    get_all_magic_wands_with_owner

router = APIRouter()


@router.get("/api/v1/magic_wand/{id}", tags=["magic_wand"])
async def get_magic_wand_details(wand_id: int, db: Session = Depends(get_db)):
    return await get_specific_magic_wand(wand_id, db)


@router.get("/api/v1/magic_wand", tags=["magic_wand"])
async def all_magic_wands(db: Session = Depends(get_db)):
    return await get_all_magic_wands_with_owner(db)


@router.post("/api/v1/magic_wand", response_model=MagicWandDTO, tags=["magic_wand"])
async def add_magic_wand(new_magic_wand: MagicWandDTO, db: Session = Depends(get_db)):
    return await create_new_magic_wand(new_magic_wand, db)


@router.post("/api/v1/user/sing-up", response_model=UserDTO, tags=["user"])
async def user_sing_up(user: UserCreateDTO, db: Session = Depends(get_db)):
    return await create_user(user, db)


@router.post("/api/v1/user/login", response_model=UserDTO, tags=["user"])
async def user_login(user: UserCreateDTO, db: Session = Depends(get_db)):
    return await login_user(user, db)