import pymongo   # to connect with  MongoDB
from fastapi.responses import HTMLResponse # to return an HTML response 
from fastapi.templating import Jinja2Templates   # to  rendering HTML templates with Jinja2
from pydantic import BaseModel # to create models for request and response data
from pymongo import MongoClient   # to connect with  MongoDB
from fastapi import FastAPI, Form, Request # to creating the FastAPI application and handling requests
from passlib.context import CryptContext  # to password hashing and verification my
from fastapi.staticfiles import StaticFiles
from routers import router
app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)