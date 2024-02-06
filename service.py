from http import HTTPStatus
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from model_dto import UserDTO, MagicWandDTO, UserCreateDTO, CustomException, MagicWandOutDTO, UserOwnerOut
from db_model import User, MagicWand


async def get_owner_username(owner_id: int, db: Session) -> UserOwnerOut:
    owner = db.query(User).filter(User.user_id == owner_id).first()
    return UserOwnerOut(username=owner.username)


async def get_specific_magic_wand(magic_wand_id: int, db: Session) -> MagicWandOutDTO:
    magic_wand = db.query(MagicWand).filter(MagicWand.wand_id == magic_wand_id).first()
    owner = await get_owner_username(magic_wand.owner_id, db)
    return MagicWandOutDTO(flexibility=magic_wand.flexibility, owner=owner, length=magic_wand.length,
                           wood=magic_wand.wood)


async def get_all_magic_wands_with_owner(db: Session):
    found_wands = db.query(MagicWand.owner_id, MagicWand.wood, User.username).join(User, MagicWand.owner_id == User.user_id).all()

    magic_wands_with_limited_info = [
        {"owner": username, "wood": wood} for owner_id, wood, username in found_wands
    ]
    return magic_wands_with_limited_info


async def create_new_magic_wand(new_magic_wand: MagicWandDTO, db: Session) -> MagicWandDTO:
    db_new_magic_wand = MagicWand(flexibility=new_magic_wand.flexibility, owner_id=new_magic_wand.owner,
                                  length=new_magic_wand.length, wood=new_magic_wand.wood)
    db.add(db_new_magic_wand)
    db.commit()
    db.refresh(db_new_magic_wand)
    return MagicWandDTO(flexibility=db_new_magic_wand.flexibility, owner=db_new_magic_wand.owner_id,
                        length=db_new_magic_wand.length, wood=db_new_magic_wand.wood)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hashing_password(password: str) -> str:
    return bcrypt_context.hash(password)


async def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(password, hashed_password)


async def create_user(user: UserCreateDTO, db: Session):
    found_user = db.query(User).filter(User.username == user.username).first()

    if found_user is not None:
        raise CustomException(
            HTTPStatus.NOT_FOUND, f"User with username {user.username} already exist."
        )

    hashed_password = await hashing_password(user.password)

    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserDTO(id=db_user.user_id, username=db_user.username)


async def login_user(user: UserCreateDTO, db: Session) -> UserDTO:
    found_user = db.query(User).filter(User.username == user.username).first()

    if found_user is None:
        raise CustomException(
            HTTPStatus.NOT_FOUND, f"User with username {user.username} does't exist."
        )

    if not await verify_password(user.password, found_user.password):
        raise CustomException(
            HTTPStatus.UNAUTHORIZED, f"Wrong password."
        )

    return UserDTO(id=found_user.user_id, username=found_user.username)
