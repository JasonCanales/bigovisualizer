import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import math

app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can tighten this later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Big-O Visualizer API is running!"}

@app.get("/bigO/{type}")
def get_big_o(type: str, n: int = 100):
    x = np.arange(1, n + 1)

    funcs = {
        "O(1)": lambda x: np.ones_like(x),
        "O(log n)": lambda x: np.log2(x),
        "O(n)": lambda x: x,
        "O(n log n)": lambda x: x * np.log2(x),
        "O(n^2)": lambda x: x ** 2,
        "O(2^n)": lambda x: np.where(x < 21, 2 ** x, None)  # Avoid insane growth
    }

    if type not in funcs:
        return {"error": "Invalid type"}

    y = funcs[type](x)

    # Handle any None or NaN for types like O(2^n)
    if y is None or np.any(y == None):
        return {"n": x[x < 21].tolist(), "y": (2 ** x[x < 21]).tolist()}
    
    return {"n": x.tolist(), "y": y.tolist()}