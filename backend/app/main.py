from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.api import routes

# 创建应用
app = FastAPI(
    title=settings.APP_NAME,
    description="扫码点单微信小程序后端API",
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(routes.router, prefix="/api", tags=["API"])


@app.on_event("startup")
def startup_event():
    """启动时初始化数据库"""
    init_db()


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
