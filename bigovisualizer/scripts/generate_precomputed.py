import math, json, os

def get_funcs():
    return {
        "O(1)": lambda n: 1,
        "O(log n)": lambda n: math.log2(n),
        "O(n)": lambda n: n,
        "O(n log n)": lambda n: n * math.log2(n),
        "O(n^2)": lambda n: n**2,
    }

PRECOMPUTED_N = [100000, 1000000]
OUTPUT_DIR = "bigovisualizer/precomputed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for n in PRECOMPUTED_N:
    x = list(range(1, n + 1))
    for label, func in get_funcs().items():
        safe_name = label.replace(" ", "_").replace("^", "").replace("(", "").replace(")", "")
        y = [func(i) for i in x]
        with open(f"{OUTPUT_DIR}/{safe_name}_{n}.json", "w") as f:
            json.dump({"n": x, "y": y}, f)