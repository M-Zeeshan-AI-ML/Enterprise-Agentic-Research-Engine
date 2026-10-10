from datetime import datetime,timedelta,timezone
from jose import JWTError,jwt
from fastapi import HTTPException,status
from app.config.settings import get_settings

def authenticate(username,password):
    s=get_settings(); return username==s.demo_username and password==s.demo_password

def create_access_token(username):
    s=get_settings(); exp=datetime.now(timezone.utc)+timedelta(minutes=s.access_token_expire_minutes)
    return jwt.encode({"sub":username,"exp":exp},s.jwt_secret_key,algorithm=s.jwt_algorithm)

def verify_token(token):
    s=get_settings(); err=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload=jwt.decode(token,s.jwt_secret_key,algorithms=[s.jwt_algorithm]); username=payload.get("sub")
        if not username: raise err
        return str(username)
    except JWTError as exc: raise err from exc
