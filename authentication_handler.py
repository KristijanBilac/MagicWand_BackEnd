from datetime import timedelta, timezone, datetime, time
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from model_dto import UserOut, UserIn
from service import user_verification
from fastapi import Depends, Header, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


async def create_access_token(user: UserOut):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token_data = {
        "user_id": user.id,
        "user_mail": user.username,
        "expire": expire.strftime("%Y-%m-%d %H:%M:%S"),
    }
    # Pravljenje tokena od Token_data, potpisa i vrste algoritma
    encoded_jwt_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)

    return encoded_jwt_token


# Pravjenje tokeena prilikom logovanja
async def login_user_token(login_data: UserIn, db: Session = Depends(get_db)):
    user = await user_verification(login_data, db)
    return await create_access_token(user)


# Proverra tokena iz headera
def get_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.split("Bearer ")[1]



