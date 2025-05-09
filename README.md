# 📈 Big-O Visualizer

A dynamic, educational visualization of algorithmic time complexities — deployed fully serverlessly with AWS.

## 🔧 Stack

- **Frontend**: HTML + TailwindCSS + Chart.js
- **Backend**: FastAPI + Mangum, deployed to AWS Lambda via SAM
- **Infrastructure**: AWS API Gateway, Lambda, CloudFormation (SAM), S3 (planned)
- **Observability**: AWS X-Ray + CloudWatch
- **CI/CD**: Manual deployment via AWS SAM CLI

---

## 🔍 Live Demo

Frontend: [Coming Soon](#)  
API: [`/bigO/O(n^2)`](https://48doisfimg.execute-api.us-east-1.amazonaws.com/Prod/bigO/O(n^2))

---

## ✨ Features

- Choose between O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ)
- Auto-generated chart with animated transitions
- Toggle dark mode ☀️🌙
- Download chart as PNG
- API responds with JSON `{ n: [...], y: [...] }`
- Fully responsive, mobile-friendly UI
- Bookmarkable dropdown via query string (`?type=O(n^2)`)