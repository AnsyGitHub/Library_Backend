from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import models, schemas
from database import engine
from sqlalchemy.orm import Session
from dependency import get_db
from routers.book import book_router
from routers.member import member_router
from routers.borrow import borrow_router
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from routers.user import user_router



models.Base.metadata.create_all(bind=engine)




SECRET_KEY = "a652a9b7fd648256b983af18f2e8e4e5ad48dd7c99c9c89dc1c5217f6ec5bca7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_username(username: str, db: Session = Depends(get_db)):
    return db.query(models.UserInDB).filter(models.UserInDB.username == username).first()


# Function to authenticate user
def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_username(username,db)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user    

def create_access_token(data: dict, expires_delta: timedelta | None = None, db: Session = Depends(get_db)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


app = FastAPI()
app.include_router(user_router)
app.include_router(book_router, tags=["Books"])
app.include_router(member_router)
app.include_router(borrow_router, tags=["Borrow"])



@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires, db=db
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.put("/create")
async def create_user_auth(user:schemas.User,password:str, db: Session = Depends(get_db)):
    hp = get_password_hash(password)
    new_user = schemas.UserInDB(**user.model_dump(), hashed_password= hp)
    db_user = models.UserInDB(**new_user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "User Added"

@app.get("/")
def HomePage():
    return {"Welcome to the Library"}







