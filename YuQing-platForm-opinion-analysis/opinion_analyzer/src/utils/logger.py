"""Logging utility module."""
import logging
import sys
import time
import json
from typing import Optional, Dict, Any
from pathlib import Path
from logging.handlers import RotatingFileHandler
from functools import wraps

class JsonFormatter(logging.Formatter):
    """JSON格式的日志格式化器.
    
    将日志记录格式化为JSON格式，便于后续分析。
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录.
        
        Args:
            record: 日志记录
            
        Returns:
            str: 格式化后的JSON字符串
        """
        # 基础字段
        message = {
            'timestamp': self.formatTime(record),
            'name': record.name,
            'levelname': record.levelname,
            'message': record.getMessage(),
        }
        
        # 添加异常信息
        if record.exc_info:
            message['exception'] = self.formatException(record.exc_info)
        
        # 添加额外字段
        if hasattr(record, 'extra_fields'):
            message['extra_fields'] = record.extra_fields
        
        return json.dumps(message, ensure_ascii=False)

def setup_logger(
    name: Optional[str] = None,
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
    json_format: bool = False
) -> logging.Logger:
    """配置并返回logger实例.
    
    Args:
        name: Logger名称，通常为__name__
        level: 日志级别
        log_file: 日志文件路径，如果提供则同时输出到文件
        max_bytes: 单个日志文件的最大大小
        backup_count: 保留的日志文件数量
        json_format: 是否使用JSON格式
        
    Returns:
        logging.Logger: 配置好的logger实例
    """
    logger = logging.getLogger(name or __name__)
    
    # 移除现有的处理器
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 配置格式
    formatter = (
        JsonFormatter() if json_format
        else logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    
    # 添加控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 如果提供了日志文件路径，添加文件输出
    if log_file:
        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 使用RotatingFileHandler进行日志轮转
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8',
            delay=False  # 立即打开文件
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # 写入一条测试日志以确保文件被创建
        logger.debug("Logger initialized")
    
    logger.setLevel(level)
    logger.propagate = False  # 避免日志重复
    
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """获取logger实例的快捷方式.
    
    Args:
        name: Logger名称
        
    Returns:
        logging.Logger: Logger实例
    """
    return setup_logger(
        name=name,
        level=logging.INFO,
        log_file='logs/opinion_analyzer.log',
        json_format=True
    )

class LoggerAdapter(logging.LoggerAdapter):
    """Logger适配器，用于添加额外字段."""
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """处理日志消息.
        
        Args:
            msg: 日志消息
            kwargs: 关键字参数
            
        Returns:
            tuple: (消息, 关键字参数)
        """
        extra = kwargs.get('extra', {})
        if not isinstance(extra, dict):
            extra = {}
        
        kwargs['extra'] = self.extra
        return msg, kwargs

def with_logger(func):
    """用于记录函数调用的装饰器.
    
    Args:
        func: 被装饰的函数
        
    Returns:
        装饰器函数
    """
    logger = get_logger(func.__module__)
    func.logger = logger
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func_name = func.__name__
            
        # 记录函数调用
        extra_fields = {
            'function': func_name,
            'args': str(args),
            'kwargs': str(kwargs)
        }
        
        logger.info(
            f"开始执行函数: {func_name}",
            extra={'extra_fields': extra_fields}
        )
        
        try:
            result = func(*args, **kwargs)
            
            # 记录执行时间
            execution_time = time.time() - start_time
            extra_fields.update({
                'execution_time': execution_time,
                'status': 'success'
            })
            
            logger.info(
                f"函数执行完成: {func_name}",
                extra={'extra_fields': extra_fields}
            )
            
            return result
            
        except Exception as e:
            # 记录异常
            execution_time = time.time() - start_time
            extra_fields.update({
                'execution_time': execution_time,
                'status': 'error',
                'error_type': type(e).__name__,
                'error_message': str(e)
            })
            
            logger.error(
                f"函数执行失败: {func_name}",
                exc_info=True,
                extra={'extra_fields': extra_fields}
            )
            raise
    return wrapper