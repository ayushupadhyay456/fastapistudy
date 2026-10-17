from fastapi import FastAPI
from jose import jwt


app=FastAPI



@app.get('/')

def home():
    return "This is home route"