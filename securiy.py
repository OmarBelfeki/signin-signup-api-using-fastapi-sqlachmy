from passlib.context import CryptContext
from jose import jwt

from models import UserModel

JWT_SECRET = "belfeki$$3423omar"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user: "UserModel"):
    try:
        payload={
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "active": user.is_active
        }
        return jwt.encode(payload, key=JWT_SECRET, algorithm=ALGORITHM)
    except Exception as e:
        print(str(e))
        raise e

def get_password_hash(password):
    return pwd_content.hash(password)
