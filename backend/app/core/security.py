import bcrypt
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import JWT_SECRET,JWT_ALGO,JWT_ACCESS_TOKEN_EXPIRE_MINUTES

class ExpiredSignatureError(Exception):
    pass

class InvalidTokenError(Exception):
    pass


def hash_password(pwd: str) -> str:
    pwd_bytes=pwd.encode('utf-8')
    hashed_pwd=bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed_pwd.decode('utf-8')


def verify_password(pwd:str, hash:str) -> bool:
    pwd_bytes=pwd.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes,hash.encode('utf-8'))

def create_access_token(user_id: str) -> str:
    now=datetime.now(timezone.utc)

    expire=now+timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))

    payload= {
        "sub":user_id,
        "iat":now,
        "exp": expire,
        "token_type":"access"
    }

    token=jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGO)
    return token

def verify_access_token(token:str) -> str | None:
    try:
        payload=jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGO])
        user_id=payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except jwt.ExpiredSignatureError:
        raise ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid Token")
        