"""Test cases for logger utilities."""
import json
import logging
import pytest
from src.utils.logger import (
    get_logger,
    JsonFormatter,
    with_logger,
    LoggerAdapter,
    setup_logger
)

def test_json_formatter():
    """测试JSON格式化器."""
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="test message",
        args=(),
        exc_info=None
    )
    
    # 格式化日志记录
    output = formatter.format(record)
    data = json.loads(output)
    
    # 验证字段
    assert data["name"] == "test"
    assert data["levelname"] == "INFO"
    assert data["message"] == "test message"
    assert "timestamp" in data

def test_logger_adapter():
    """测试日志适配器."""
    logger = logging.getLogger("test")
    extra = {"request_id": "123"}
    adapter = LoggerAdapter(logger, extra)
    
    # 验证额外字段
    assert adapter.extra == extra
    
    # 验证消息处理
    msg, kwargs = adapter.process("test message", {})
    assert msg == "test message"
    assert "extra" in kwargs
    assert kwargs["extra"]["request_id"] == "123"

def test_with_logger_decorator():
    """测试日志装饰器."""
    @with_logger
    def example_function(arg1, arg2=None):
        return f"{arg1}-{arg2}"
    
    # 验证装饰器添加的logger属性
    assert hasattr(example_function, "logger")
    assert isinstance(example_function.logger, logging.Logger)
    
    # 验证函数调用
    result = example_function("a", arg2="b")
    assert result == "a-b"

def test_get_logger():
    """测试获取日志器."""
    # 获取日志器
    logger = get_logger("test")
    
    # 验证日志器属性
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"
    assert logger.level == logging.INFO
    
    # 验证处理器
    handlers = logger.handlers
    assert len(handlers) > 0
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)

def test_setup_logger():
    """测试日志器设置."""
    # 设置日志器
    logger = setup_logger(
        name="test",
        level=logging.DEBUG,
        log_file="test.log",
        max_bytes=1024,
        backup_count=3,
        json_format=True
    )
    
    # 验证日志器属性
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"
    assert logger.level == logging.DEBUG
    
    # 验证处理器
    handlers = logger.handlers
    assert len(handlers) == 2  # 文件处理器和控制台处理器
    
    # 验证文件处理器
    file_handler = next(h for h in handlers if isinstance(h, logging.handlers.RotatingFileHandler))
    assert file_handler.baseFilename.endswith("test.log")
    assert file_handler.maxBytes == 1024
    assert file_handler.backupCount == 3
    assert isinstance(file_handler.formatter, JsonFormatter)
    
    # 验证控制台处理器
    stream_handler = next(h for h in handlers if isinstance(h, logging.StreamHandler))
    assert isinstance(stream_handler.formatter, JsonFormatter)

def test_logger_levels():
    """测试日志级别."""
    logger = get_logger("test")
    
    # 记录不同级别的日志
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    
    # 验证日志级别过滤
    assert logger.isEnabledFor(logging.INFO)
    assert logger.isEnabledFor(logging.WARNING)
    assert logger.isEnabledFor(logging.ERROR)
    assert logger.isEnabledFor(logging.CRITICAL)
    assert not logger.isEnabledFor(logging.DEBUG)  # 默认INFO级别

def test_logger_exception():
    """测试异常日志."""
    logger = get_logger("test")
    
    try:
        raise ValueError("test error")
    except ValueError:
        logger.exception("An error occurred")
    
    # 验证异常处理器
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)

def test_logger_with_context():
    """测试带上下文的日志."""
    logger = get_logger("test")
    adapter = LoggerAdapter(logger, {"context": "test"})
    
    # 记录带上下文的日志
    adapter.info("test message")
    adapter.error("test error")
    
    # 验证上下文传递
    assert adapter.extra["context"] == "test"