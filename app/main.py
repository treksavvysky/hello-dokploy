from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/api/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/api/metrics")
async def metrics():
    return {"metrics": "some_metrics"}

@app.get("/healthy")
async def healthy_root():
    return PlainTextResponse("ok", status_code=200)