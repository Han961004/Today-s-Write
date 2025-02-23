from fastapi import FastAPI
from routers import posts
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="FastAPI Application")

# 라우터 등록
app.include_router(posts.router, prefix='/api/posts')  # /posts 경로는 라우터에서 처리

# Prometheus 모니터링
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app, endpoint="/api/metrics")  # Prometheus 메트릭 경로 설정

# 애플리케이션 시작 시 테이블 생성
@app.on_event("startup")
async def on_startup():
    from database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/api/")
def read_api():
    return {}  # 이 경로는 특별한 내용이 필요 없으므로 그냥 두기