# 📈 Big-O Visualizer

An interactive web application that visualizes time complexity growth — from `O(1)` to `O(2ⁿ)` — using animated line charts and real-world input size examples.

Built for both technical and non-technical audiences to intuitively explore how algorithms scale with input.

---

## 🌐 Live Demo

👉 [View the Live App](https://dhb5rlzn2ipkx.cloudfront.net/)

---

## 🧰 Tech Stack

- **Backend**: Python, FastAPI, AWS Lambda, API Gateway
- **Frontend**: HTML, JavaScript (Chart.js), TailwindCSS
- **Infrastructure**: AWS S3 (static site hosting), CloudFront (HTTPS), SAM CLI
- **Deployment**: Manual AWS CLI

---

## 📊 Features

- Toggle between time complexities: `O(1)`, `O(log n)`, `O(n)`, `O(n log n)`, `O(n²)`, `O(2ⁿ)`
- Interactive slider to increase input size (n) up to 100,000; compare up to two complexities
- Contextual examples that explain what “n” represents in real-world terms
- Fully responsive UI with dark mode toggle
- Fast, globally accessible hosting via CloudFront CDN

---

## API data contract

`GET /bigO/{type}?n=100000` accepts the six complexity labels above and integer
input sizes from 1 through 100,000. Invalid input sizes return HTTP 422; unknown
complexity labels return HTTP 400.

The response remains `{ "n": [...], "y": [...] }`, with aligned arrays of at most
1,000 points. Ordinary curves include both endpoints, retain every input for
`n <= 1000`, and otherwise use evenly spaced integer inputs. Values are computed
only at those inputs, so calculation and response size are bounded. The frontend
plots the returned coordinates on a numeric x-axis without further downsampling.
These are illustrative operation counts, not measured algorithm runtimes.

For `O(2^n)`, every input through 19 is retained. Values at 20 and above are
`null`, preserving the existing display cutoff; the final input is still included.
Precomputed JSON datasets are no longer required.

### Local verification

From the repository root, in a virtual environment:

```bash
python -m pip install -r bigovisualizer/hello_world/requirements.txt -r bigovisualizer/tests/requirements.txt
PYTHONPATH=bigovisualizer python -m pytest bigovisualizer/tests/unit -q
```

The deployed smoke test requires AWS credentials and `AWS_SAM_STACK_NAME`:

```bash
PYTHONPATH=bigovisualizer python -m pytest bigovisualizer/tests/integration -q
```

### Local before/after measurement

For `O(n log n)` at `n=100000`, the response decreased from **2,428,075 bytes to
24,284 bytes** (about 99%). Median warm in-process request time decreased from
**162.54 ms to 2.42 ms** across 10 measured requests after one warm-up per version.
The comparison used Python 3.12.14, FastAPI TestClient, and the previous endpoint
reading its original precomputed file. These are local measurements, not deployed
Lambda latency, cold-start, or cost measurements.

### Deployment

Deploy the backend and frontend together: the frontend now consumes sampled
coordinates and requires the updated API. Create a fresh SAM build before deploying
to avoid reusing the repository's old build artifacts:

```bash
cd bigovisualizer
sam build --no-cached
sam deploy
cd ..
```

Then sync `frontend/` to the hosting bucket and invalidate CloudFront as in
`deploy.sh`. Run the deployed smoke test after deployment.

---

## 🧠 Why This Exists

Understanding Big-O isn’t just about asymptotic notation — it’s about intuition. This tool helps learners, interviewers, and product managers visualize the practical impact of input growth.

---

## 🧑‍💻 Built By

**Jason Canales**  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/jason-canales/)  
💻 [GitHub Projects](https://github.com/JasonCanales)

---

## 📂 License

MIT License. Free to use, fork, and expand.
