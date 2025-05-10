from fastapi import FastAPI, Request
from mangum import Mangum
import math

app = FastAPI()
handler = Mangum(app)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your S3 site URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Big-O Visualizer API is running!"}

@app.get("/bigO/{type}")
def get_big_o(type: str, n: int = 100):
    n_values = list(range(1, n + 1))
    funcs = {
        "O(1)": lambda n: 1,
        "O(log n)": lambda n: math.log2(n),
        "O(n)": lambda n: n,
        "O(n log n)": lambda n: n * math.log2(n),
        "O(n^2)": lambda n: n**2,
        "O(2^n)": lambda n: 2**n if n < 20 else None,  # keep cap
    }

    if type not in funcs:
        return {"error": "Invalid type"}

    y_values = [funcs[type](i) for i in n_values if funcs[type](i) is not None]
    n_values = n_values[:len(y_values)]  # sync length

    return {"n": n_values, "y": y_values}