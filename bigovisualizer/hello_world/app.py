import math
from fastapi import FastAPI, HTTPException, Query
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

MAX_INPUT = 100_000
MAX_POINTS = 1_000


def sample_inputs(n: int):
    """Evenly space integer inputs, retaining both endpoints without duplicates."""
    count = min(n, MAX_POINTS)
    if count == 1:
        return [1]
    return [1 + i * (n - 1) // (count - 1) for i in range(count)]


@app.get("/bigO/{type}")
def get_big_o(type: str, n: int = Query(..., ge=1, le=MAX_INPUT)):
    funcs = {
        "O(1)": lambda n: 1,
        "O(log n)": lambda n: math.log2(n),
        "O(n)": lambda n: n,
        "O(n log n)": lambda n: n * math.log2(n),
        "O(n^2)": lambda n: n**2,
        "O(2^n)": lambda n: 2**n if n < 20 else None,
    }

    if type not in funcs:
        raise HTTPException(status_code=400, detail="Invalid complexity type")

    if type == "O(2^n)":
        # Retain every visible exponential point and the null cutoff at 20.
        x = list(range(1, min(n, 20) + 1))
        if n > 20:
            x.append(n)
    else:
        x = sample_inputs(n)
    y = [funcs[type](i) for i in x]
    return {"n": x, "y": y}
