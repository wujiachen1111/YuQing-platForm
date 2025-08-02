"""Configuration module."""
import os
from functools import lru_cache
from typing import Any
from pydantic import BaseModel, Field, field_validator
from pydantic import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """应用配置.
    
    Attributes:
        debug: 是否开启调试模式
        deepseek_api_key: Deepseek API密钥
        crawler_max_retries: 爬虫最大重试次数
        crawler_timeout: 爬虫请求超时时间
        crawler_delay_min: 爬虫请求最小延迟时间
        crawler_delay_max: 爬虫请求最大延迟时间
        api_host: API服务器主机地址
        api_port: API服务器端口
    """
    
    debug: bool = Field(default=False, description="是否开启调试模式")
    deepseek_api_key: str = "sk-08deec757a324aab94501cc2a880a565"
    
    # API服务器配置
    api_host: str = Field(default="127.0.0.1", description="API服务器主机地址")
    api_port: int = Field(default=8000, description="API服务器端口", ge=1, le=65535)
    
    # 爬虫配置
    crawler_max_retries: int = Field(default=3, description="爬虫最大重试次数", ge=1)
    crawler_timeout: int = Field(default=10, description="爬虫请求超时时间", ge=1)
    crawler_delay_min: float = Field(default=1.0, description="爬虫请求最小延迟时间", ge=0.0)
    crawler_delay_max: float = Field(default=3.0, description="爬虫请求最大延迟时间", gt=0.0)
    
    @field_validator("crawler_delay_max")
    def validate_delay_range(cls, v: float, info: ValidationInfo) -> float:
        """验证延迟时间范围.
        
        Args:
            v: 最大延迟时间
            info: 字段验证信息
            
        Returns:
            float: 验证后的最大延迟时间
            
        Raises:
            ValueError: 当最大延迟时间小于最小延迟时间时
        """
        values = info.data
        if "crawler_delay_min" in values and v < values["crawler_delay_min"]:
            raise ValueError("最大延迟时间必须大于最小延迟时间")
        return v
    
    @field_validator("debug", mode="before")
    def parse_debug(cls, v: Any) -> bool:
        """解析调试模式.
        
        Args:
            v: 调试模式值
            
        Returns:
            bool: 解析后的调试模式
        """
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return bool(v)
    
    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="",
        env_nested_delimiter="__"
    )

@lru_cache()
def get_settings() -> Settings:
    """获取应用配置.
    
    Returns:
        Settings: 应用配置
    """
    return Settings()