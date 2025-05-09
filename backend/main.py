from fastapi import FastAPI
from mangum import Mangum
import math

app = FastAPI()
handler = Mangum(app)

@app.api_route("/", methods=["GET", "POST"])
def root():
    return {"message": "Big-O Visualizer API is running!"}

@app.get("/bigO/{type}")
def get_big_o(type: str):
    n_values = list(range(1, 101))
    funcs = {
        "O(1)": lambda n: 1,
        "O(log n)": lambda n: math.log2(n),
        "O(n)": lambda n: n,
        "O(n log n)": lambda n: n * math.log2(n),
        "O(n^2)": lambda n: n**2,
        "O(2^n)": lambda n: 2**n if n < 20 else None,
    }

    if type not in funcs:
        return {"error": "Invalid type"}

    y_values = [funcs[type](n) for n in n_values]
    return {"n": n_values, "y": y_values}