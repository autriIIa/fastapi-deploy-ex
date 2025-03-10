import sqlite3
from fastapi import FastAPI, Form
from typing import Annotated
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/login")
async def login():
    try:
        with sqlite3.connect("webpagecafe.db") as conn:
            cursor = conn.cursor()
            query = "SELECT id, user, password FROM Users"
            cursor.execute(query)
            data = cursor.fetchall()
            json_data = [{"id": row[0], "user": row[1],
                          "password": row[2]}for row in data]
            return JSONResponse(content=json_data)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")


@app.get("/menu")
async def menu():
    try:
        with sqlite3.connect("webpagecafe.db") as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Menu"
            cursor.execute(query)
            data = cursor.fetchall()
            return JSONResponse(content=data)
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
