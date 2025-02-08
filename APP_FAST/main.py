from fastapi import FastAPI
from routers import posts
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="FastAPI Application")

# 라우터 등록
app.include_router(posts.router)
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app, endpoint="/api/metrics")

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
