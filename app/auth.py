from __future__ import annotations

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app import models, schemas, utils
from app.schemas import schemas
from app.deps import get_db




load_dotenv()
router = APIRouter(prefix="/auth", tags=["Authentication"])

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise ValueError("Missing CLIENT_ID or CLIENT_SECRET in environment variables")


OAUTH2_CLIENTS = {CLIENT_ID: CLIENT_SECRET}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(user_id)

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------
@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = utils.hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Optional client validation
    if form_data.client_id:
        secret = OAUTH2_CLIENTS.get(form_data.client_id)
        if not secret or secret != form_data.client_secret:
            raise HTTPException(status_code=401, detail="Invalid client credentials")

    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}



#@router.post("/token", response_model=schemas.Token)
# def login_for_access_token(
#     form_data: OAuth2PasswordRequestFormWithClient = Depends(),
#     db: Session = Depends(get_db)
# ):
#     print("Incoming data:", form_data.username, form_data.client_id, form_data.client_secret)
#
#     Validate client credentials
#     expected_secret = OAUTH2_CLIENTS.get(form_data.client_id)
#     if not expected_secret or expected_secret != form_data.client_secret:
#         raise HTTPException(status_code=401, detail="Invalid client credentials")
#
#     Validate user credentials
#     db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
#     if not db_user or not utils.verify_password(form_data.password, db_user.hashed_password):
#         raise HTTPException(status_code=401, detail="Incorrect username or password")
#
#     #Create access token
#     access_token = create_access_token(data={"sub": str(db_user.id)})
#     return {"access_token": access_token, "token_type": "bearer"}
#
# @router.post("/token", response_model=schemas.Token)
# def login_for_access_token(
#     form_data: OAuth2PasswordRequestFormWithClient = Depends(),
#     db: Session = Depends(get_db)
# ):
#     print("Incoming data:", form_data.username, form_data.client_id, form_data.client_secret)
#
#     #  Validate client credentials
#     expected_secret = OAUTH2_CLIENTS.get(form_data.client_id)
#     if not expected_secret or expected_secret != form_data.client_secret:
#         raise HTTPException(status_code=401, detail="Invalid client credentials")
#
#     #  Validate user credentials
#     db_user = db.query(models.User).filter(models.User.username == form_data.username).first()
#     if not db_user or not utils.verify_password(form_data.password, db_user.hashed_password):
#         raise HTTPException(status_code=401, detail="Incorrect username or password")
#
#     # Create access token
#     access_token = create_access_token(data={"sub": str(db_user.id)})
#     return {"access_token": access_token, "token_type": "bearer"}

