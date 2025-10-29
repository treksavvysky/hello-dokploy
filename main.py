import time
import psutil
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# --- State ---
start_time = time.time()
request_count = 0
total_latency = 0.0
# --- Middleware ---

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    global request_count, total_latency
    start_time_request = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time_request) * 1000

    # Update metrics
    request_count += 1
    total_latency += process_time

    return response

# --- Routes ---

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/metrics")
async def metrics():
    uptime_seconds = time.time() - start_time
    average_latency_ms = (total_latency / request_count) if request_count > 0 else 0

    data = {
        "uptime_seconds": uptime_seconds,
        "request_count": request_count,
        "average_latency_ms": average_latency_ms,
        "status": "healthy"
    }

    # Optional system metrics
    try:
        data["cpu_percent"] = psutil.cpu_percent(interval=None)
        data["memory_percent"] = psutil.virtual_memory().percent
    except Exception:
        # psutil not available or other issue
        pass

    return JSONResponse(content=data)

# --- Graceful Shutdown ---

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Application is starting up")
    yield
    # Shutdown
    print("Application is shutting down")

app.router.lifespan_context = lifespan

async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
