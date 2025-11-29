from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as news_router

# 项目实例创建
app = FastAPI(
    title="新闻 API 服务",
    description="新闻列表和详情接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS解决跨域请求问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(news_router)

@app.get("/", description="news api 服务运行状态")
def health_check():
    """
    服务健康检查接口
    功能：验证服务是否正常运行，返回基本状态信息
    """
    return {"status": "success", "message": "news api 服务运行中", "docs_url": "/docs"}

# 运行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )