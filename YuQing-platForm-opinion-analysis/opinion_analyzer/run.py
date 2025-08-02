"""Application entry point."""
import uvicorn
from src.config import get_settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

def start():
    """启动应用程序."""
    settings = get_settings()
    
    # 显示启动信息
    logger.info("正在启动舆情分析API服务...")
    logger.info(f"服务地址: http://{settings.api_host}:{settings.api_port}")
    logger.info(f"API文档地址: http://{settings.api_host}:{settings.api_port}/api/docs")
    logger.info(f"调试模式: {'开启' if settings.debug else '关闭'}")
    
    # 启动服务器
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="info" if settings.debug else "error",
        access_log=True
    )

if __name__ == "__main__":
    start()