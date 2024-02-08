from datetime import timezone, datetime
from http.client import HTTPException
from jose import jwt, JWTError
from fastapi import HTTPException, status

SECRET_KEY = "03d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3


def decodeJWT(token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        if decoded_token["expire"] <= datetime.now(timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S"
        ):
            raise credentials_exception

    except JWTError as e:
        print(e)
        raise credentials_exception

    return decoded_token
