"""Main FastAPI application."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from .routes import router
from ..config import get_settings

settings = get_settings()

# 创建FastAPI应用
app = FastAPI(
    title="舆情分析API",
    description="""
    提供新闻舆情分析服务。
    
    功能：
    - 根据关键词搜索新闻
    - 分析新闻是否为舆情
    - 分析舆情的情感倾向
    - 提取相关实体（公司、人物）
    - 存储舆情数据
    
    注意：
    - 每次请求最多分析50条新闻
    - 使用缓存减少重复分析
    - 支持跨域请求
    """,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    debug=settings.debug
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加请求处理时间中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """添加请求处理时间头.
    
    Args:
        request: 请求对象
        call_next: 下一个处理函数
        
    Returns:
        Response: 响应对象
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器.
    
    Args:
        request: 请求对象
        exc: 异常对象
        
    Returns:
        JSONResponse: JSON响应
    """
    return JSONResponse(
        status_code=500,
        content={"detail": f"服务器错误: {str(exc)}"}
    )

# 包含API路由
app.include_router(router)