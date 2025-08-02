"""Test cases for configuration module."""
import os
import pytest
from src.config import Settings, get_settings

def test_default_settings():
    """测试默认配置."""
    settings = Settings()
    
    # 验证默认值
    assert settings.debug is False
    assert settings.api_host == "127.0.0.1"
    assert settings.api_port == 8000
    assert settings.crawler_max_retries == 3
    assert settings.crawler_timeout == 10
    assert settings.crawler_delay_min == 1.0
    assert settings.crawler_delay_max == 3.0

def test_settings_from_env(monkeypatch):
    """测试从环境变量加载配置."""
    # 设置环境变量
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("API_HOST", "0.0.0.0")
    monkeypatch.setenv("API_PORT", "9000")
    monkeypatch.setenv("CRAWLER_MAX_RETRIES", "5")
    
    settings = Settings()
    
    # 验证环境变量值
    assert settings.debug is True
    assert settings.api_host == "0.0.0.0"
    assert settings.api_port == 9000
    assert settings.crawler_max_retries == 5
    
    # 未设置的值应保持默认值
    assert settings.crawler_timeout == 10
    assert settings.crawler_delay_min == 1.0
    assert settings.crawler_delay_max == 3.0

def test_settings_validation():
    """测试配置验证."""
    # 端口号范围验证
    with pytest.raises(ValueError):
        Settings(api_port=-1)
    
    with pytest.raises(ValueError):
        Settings(api_port=65536)
    
    # 爬虫延迟时间验证
    with pytest.raises(ValueError):
        Settings(crawler_delay_min=-1.0)
    
    with pytest.raises(ValueError):
        Settings(crawler_delay_max=0.0)
    
    with pytest.raises(ValueError):
        Settings(crawler_delay_min=3.0, crawler_delay_max=1.0)

def test_settings_from_env_file(tmp_path, monkeypatch):
    """测试从.env文件加载配置."""
    # 创建临时.env文件
    env_file = tmp_path / ".env"
    env_file.write_text("DEBUG=true\nAPI_HOST=0.0.0.0\nAPI_PORT=9000\nCRAWLER_MAX_RETRIES=5")
    
    # 修改环境变量
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("API_HOST", "0.0.0.0")
    monkeypatch.setenv("API_PORT", "9000")
    monkeypatch.setenv("CRAWLER_MAX_RETRIES", "5")
    
    # 创建设置实例
    settings = Settings()
    
    # 验证.env文件中的值
    assert settings.debug is True
    assert settings.api_host == "0.0.0.0"
    assert settings.api_port == 9000
    assert settings.crawler_max_retries == 5
    
    # 未在.env文件中设置的值应保持默认值
    assert settings.crawler_timeout == 10
    assert settings.crawler_delay_min == 1.0
    assert settings.crawler_delay_max == 3.0

def test_get_settings_cache():
    """测试配置缓存."""
    # 第一次调用
    settings1 = get_settings()
    
    # 修改环境变量（不应影响已缓存的配置）
    os.environ["API_PORT"] = "9000"
    
    # 第二次调用
    settings2 = get_settings()
    
    # 应该返回相同的实例
    assert settings1 is settings2
    assert settings1.api_port == 8000  # 应该保持默认值
    
    # 清除缓存
    get_settings.cache_clear()
    
    # 再次调用（应该使用新的环境变量）
    settings3 = get_settings()
    assert settings3.api_port == 9000