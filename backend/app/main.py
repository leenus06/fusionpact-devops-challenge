from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, Counter, Histogram, REGISTRY
import time

app = FastAPI(title="Fusionpact Backend API")

# CORS middleware MUST be added before any routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency in seconds')

@app.get("/")
async def root():
    return {"message": "Fusionpact Backend API", "status": "healthy", "version": "1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "backend"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(REGISTRY), media_type="text/plain")

@app.get("/api/data")
async def get_data():
    return {"data": [1, 2, 3, 4, 5], "source": "backend"}

@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    REQUEST_LATENCY.observe(process_time)
    REQUEST_COUNT.labels(
        method=request.method,  # Fixed: added comma and proper indentation
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
