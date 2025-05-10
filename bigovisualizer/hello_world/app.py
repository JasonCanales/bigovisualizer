import math, os, json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Big-O Visualizer API is running!"}

@app.get("/bigO/{type}")
def get_big_o(type: str, n: int = Query(...)):
    funcs = {
        "O(1)": lambda n: 1,
        "O(log n)": lambda n: math.log2(n),
        "O(n)": lambda n: n,
        "O(n log n)": lambda n: n * math.log2(n),
        "O(n^2)": lambda n: n**2,
        "O(2^n)": lambda n: 2**n if n < 20 else None,
    }

    safe_name = type.replace(" ", "_").replace("^", "").replace("(", "").replace(")", "")
    file_path = f"/var/task/precomputed/{safe_name}_{n}.json"

    if os.path.exists(file_path):
        with open(file_path) as f:
            return json.load(f)

    if type not in funcs:
        return {"error": "Invalid type"}

    x = list(range(1, n + 1))
    y = [funcs[type](i) for i in x]
    return {"n": x, "y": y}