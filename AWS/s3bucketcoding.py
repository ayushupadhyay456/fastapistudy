import boto3
from fastapi import FastAPI,UploadFile,HTTPException

app=FastAPI()



AWS_BUCKET=''



@app.post('/upload')

def upload_data(file:UploadFile):
    if not file:
        raise HTTPException(
            status_code=401,
            detail='No file detected'
        )

    contents=file.read()
    
