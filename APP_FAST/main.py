from fastapi import FastAPI
from routers import posts

app = FastAPI(title="FastAPI Application")

# 라우터 등록
app.include_router(posts.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
