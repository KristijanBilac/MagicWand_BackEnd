from http import HTTPStatus
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from token_handler import decodeJWT
from model_dto import UserOut, MagicWandDTO, UserIn, CustomException, UserOwnerOut, MagicWandOutDTO2
from db_model import User, MagicWand


async def get_owner_username(owner_id: int, db: Session) -> UserOwnerOut:
    owner = db.query(User).filter(User.user_id == owner_id).first()
    if owner is None:
        raise CustomException(HTTPStatus.NOT_FOUND, "Owner not found")
    return UserOwnerOut(username=owner.username)


async def get_specific_magic_wand(magic_wand_id: int, token: str, db: Session) -> MagicWandOutDTO2:
    decode_token = decodeJWT(token)
    if decode_token is None:
        raise CustomException(
            HTTPStatus.UNAUTHORIZED, "Token is invalid or expired. Please login again."
        )
    magic_wand = db.query(MagicWand).filter(MagicWand.wand_id == magic_wand_id).first()

    if magic_wand is None:
        raise CustomException(HTTPStatus.NOT_FOUND, "Magic wand not found")

    owner = await get_owner_username(magic_wand.owner_id, db)

    return MagicWandOutDTO2(flexibility=magic_wand.flexibility, owner=owner.username, length=magic_wand.length,
                            wood=magic_wand.wood)


async def get_all_limited_magic_wands_with_owner(db: Session):
    found_wands = db.query(MagicWand.owner_id, MagicWand.wood, User.username).join(User,
                                                                                   MagicWand.owner_id == User.user_id).all()

    if found_wands is None:
        raise CustomException(HTTPStatus.NOT_FOUND, "Empty list of Magic wands")

    magic_wands_with_limited_info = [
        {"owner": username, "wood": wood} for owner_id, wood, username in found_wands
    ]
    return magic_wands_with_limited_info


async def get_all_magic_wands_with_owner(token: str, db: Session):

    decode_token = decodeJWT(token)
    if decode_token is None:
        raise CustomException(
            HTTPStatus.UNAUTHORIZED, "Token is invalid or expired. Please login again."
        )

    found_wands = db.query(MagicWand.wand_id, MagicWand.flexibility, MagicWand.length, MagicWand.owner_id,
                           MagicWand.wood, User.username).join(User, MagicWand.owner_id == User.user_id).all()

    if found_wands is None:
        raise CustomException(HTTPStatus.NOT_FOUND, "Empty list of Magic wands")

    magic_wands_with_full_info = [
        {
            "id": wand_id,
            "flexibility": flexibility,
            "owner": username,
            "length": length,
            "wood": wood
        }
        for wand_id, flexibility, length, owner_id, wood, username,
        in found_wands
    ]
    return magic_wands_with_full_info


async def create_new_magic_wand(new_magic_wand: MagicWandDTO, token: str,  db: Session) -> MagicWandDTO:
    decode_token = decodeJWT(token)
    if decode_token is None:
        raise CustomException(
            HTTPStatus.UNAUTHORIZED, "Token is invalid or expired. Please login again."
        )
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


async def create_user(user: UserIn, db: Session):
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

    return UserOut(id=db_user.user_id, username=db_user.username)


async def user_verification(user: UserIn, db: Session) -> UserOut:
    found_user = db.query(User).filter(User.username == user.username).first()

    if found_user is None:
        raise CustomException(
            HTTPStatus.NOT_FOUND, f"User with username {user.username} does't exist."
        )

    if not await verify_password(user.password, found_user.password):
        raise CustomException(
            HTTPStatus.UNAUTHORIZED, "Incorrect password."
        )

    return UserOut(id=found_user.user_id, username=found_user.username)
