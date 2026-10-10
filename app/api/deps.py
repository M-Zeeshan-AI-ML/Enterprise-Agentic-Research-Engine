from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.services.auth import verify_token
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
def current_user(token:Annotated[str,Depends(oauth2_scheme)]): return verify_token(token)
