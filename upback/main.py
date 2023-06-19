from colorama import init, Fore, Back, Style
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form

from fastapi.middleware.cors import CORSMiddleware

# from simplex import call_simplex

import simplex as simplex
import vogel as vogel
import north_west as north_west

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/north-west")
def nw(file_str: str = Query(...), ):
    return north_west.call_northwest(file_str)

@app.get("/voguel")
def voguel(file_str: str = Query(...), ):
    return vogel.call_vogel(file_str)

@app.get("/simplex")
def simplx(a: str = Query(...), b: str = Query(...), c: str = Query(...),):
    return simplex.call_simplex(c, a, b)
