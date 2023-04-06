from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse # to return  HTML response
from fastapi.templating import Jinja2Templates  # to rendering HTML templates with Jinja2
from fastapi import  Form, Request # to create FastAPI application and handling requests
from passlib.context import CryptContext # to password hashing and verification
from fastapi.security import OAuth2,OAuth2PasswordBearer, OAuth2PasswordRequestForm # inbuilt class for authentication
#Oauth2requestform is inbuilt method to get request form login data
from fastapi import Depends, HTTPException, status
from datetime import timedelta, datetime
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.utils import get_authorization_scheme_param
import json
import random
import string
import datetime as dt
from typing import Dict, List, Optional
from dotenv import load_dotenv
from fastapi import Response
from models import *
from db import *
# creating router instance
router = APIRouter()

templates = Jinja2Templates(directory= "templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str):  
     return pwd_context.hash(password)
def verify_password(password: str, hashed_password: str):
     return pwd_context.verify(password, hashed_password)




@router.get("/", response_class= HTMLResponse)
def index_page(request: Request):
     return templates.TemplateResponse("index.html",{"request": request})


@router.get("/signup", response_class= HTMLResponse)
def inde_page(request: Request):
     return templates.TemplateResponse("index.html",{"request": request})


# To store the New user details in mongodb
@router.post("/signup", response_class=HTMLResponse, name="signup") 
async def signup(request: Request, Name: str = Form(...), Email: str = Form(...), Password: str = Form(...), Confirm_Password: str = Form(...)):
    hashed_password = hash_password(Password)
    print("ok")
    # mapping user details with database douments in mogodb to store in db.if it match values will store otherwise the data won't store.
    data = UserData(name=Name, email=Email, password=hashed_password,confirm_password = hashed_password) 
    users = db["users"].find_one({"email": Email})
    print(users)
    try:
        if not users:
            new_singup = db['users'].insert_one(dict(data))
            return templates.TemplateResponse("index.html", {'request': request, "message": "User signed up successfully"})
        else:
            return templates.TemplateResponse("index.html", {"request": request, "message": "user already exists go to login"})
    except Exception as e:
        print(e)
        

@router.get("/login",response_class=HTMLResponse)
async def login(request:Request):
    return templates.TemplateResponse("login.html",{"request": request})


@router.post('/dshboard', response_class=HTMLResponse, name="Login",)
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    Email = email
    userPassword = password
#     col = db["Users"]
    logindata = db["users"].find_one({"email": Email})

#     logindata = db["users"].find_one({"email": Email})
    print(logindata)
    if not logindata:
        print("no records")
        return templates.TemplateResponse('Invalid.html', {'message': "invalid email", 'request': request})
    else:
        if verify_password(userPassword,logindata['password']):
            return templates.TemplateResponse('dshboard.html', {'request': request, 'user': db})
        else:
            return templates.TemplateResponse('Invalid.html', {'message': 'invalid password', 'request': request})

@router.get("/dshboard",response_class=HTMLResponse)
async def dashboard(request:Request):
    return templates.TemplateResponse("dshboard.html",{"request": request})

@router.get('/createshipment', response_class=HTMLResponse, name="createshipment")
async def shipment(request: Request):
    return templates.TemplateResponse("createshipment.html", {"request": request})

@router.get("/Invalid",response_class=HTMLResponse)
async def dashboard(request:Request):
    return templates.TemplateResponse("Invalid.html",{"request": request})

@router.get("/devicedata",response_class=HTMLResponse)
async def dashboard(request:Request):
    return templates.TemplateResponse("datastream.html",{"request": request})

@router.get("/devicedata",response_class =HTMLResponse)  
def write_home(request: Request):
    shipments=[]
    shipments_all=request.app.database["sample_collection"].find({},{"_id":0})
    for j in shipments_all:
        shipments.append(j)    
    return templates.TemplateResponse("datastream.html",{"request":request, "shipments":shipments} )