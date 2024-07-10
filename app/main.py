from fastapi import FastAPI, Body, HTTPException, status, Response, Depends

from . import models
from .database import engine, SessionLocal
from .routers import post, user, auth, vote
from .config import Settings

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



#path operation

#decorator: modifies the behavior of a function or class
# a decorator takes a function as an argument to another function
#the first function is then called inside the wrapper function
#takes another function as an argument, adds some functionality, and returns a new function.
# It allows modifying or extending behavior of functions or methods.
# Turns the function into a path operation
#it allows users of our API to hit this endpoint 
#function

#async def (needed when we perform asynchronous tasks)
@app.get('/')
async def root():
    #FastAPI automatically converts this into JSON
    return {'message' : 'Welcome'}


