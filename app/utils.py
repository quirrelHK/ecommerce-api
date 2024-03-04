from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Which hashing algorithm to use

def hash(password: str):
    return pwd_context.hash(password)

def verfiry(palin_password: str, hashed_password: str):
    return pwd_context.verify(palin_password, hashed_password)