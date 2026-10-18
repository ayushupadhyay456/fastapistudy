from fastapi import FastAPI,Depends,HTTPException
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta

app=FastAPI()
secret_key='my-secret-key'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,secret_key,algorithm=ALGORITHM)






@app.post("/login")
def login(form:OAuth2PasswordRequestForm=Depends()):
    if form.username!="ayush" or form.password!="1234":
        raise HTTPException(status_code=401,detail="INVALID CREDENTIAL")
    token=create_access_token({"sub":form.username})
    return {"access_token":token,"token_type":"bearer"}

@app.get("/protected")

def get_user_date(token:str=Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token,secret_key,algorithms=ALGORITHM)
        user=payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401,detail="INVALID TOKEN")
    return {"message":f"The user name is {user}"}




