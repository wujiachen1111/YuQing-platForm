"""API models module."""
from typing import List
from pydantic import BaseModel, Field, validator
from ..analyzer.models import AnalysisResult

class AnalyzeRequest(BaseModel):
    """分析请求模型.
    
    Attributes:
        keyword: 搜索关键词
        opinion_count: 需要分析的新闻数量
    """
    
    keyword: str = Field(
        ...,
        description="搜索关键词",
        example="特斯拉",
        min_length=1,
        max_length=50
    )
    opinion_count: int = Field(
        default=30,
        description="需要分析的新闻数量",
        example=30,
        ge=1,
        le=50
    )
    
    @validator("keyword")
    def validate_keyword(cls, v: str) -> str:
        """验证关键词.
        
        Args:
            v: 关键词
            
        Returns:
            str: 验证后的关键词
            
        Raises:
            ValueError: 当关键词无效时
        """
        v = v.strip()
        if not v:
            raise ValueError("关键词不能为空")
        return v
    
    @validator("opinion_count")
    def validate_opinion_count(cls, v: int) -> int:
        """验证新闻数量.
        
        Args:
            v: 新闻数量
            
        Returns:
            int: 验证后的新闻数量
            
        Raises:
            ValueError: 当新闻数量无效时
        """
        if v < 1:
            raise ValueError("新闻数量必须大于0")
        if v > 50:
            raise ValueError("新闻数量不能超过50")
        return v

class AnalyzeResponse(BaseModel):
    """分析响应模型.
    
    Attributes:
        keyword: 搜索关键词
        total_count: 搜索到的新闻总数
        opinion_count: 舆情新闻数量
        opinions: 舆情列表
    """
    
    keyword: str = Field(
        ...,
        description="搜索关键词",
        example="特斯拉"
    )
    total_count: int = Field(
        ...,
        description="搜索到的新闻总数",
        example=20,
        ge=0
    )
    opinion_count: int = Field(
        ...,
        description="舆情新闻数量",
        example=5,
        ge=0
    )
    opinions: List[AnalysisResult] = Field(
        ...,
        description="舆情列表"
    )
    
    class Config:
        """Pydantic配置."""
        json_schema_extra = {
            "example": {
                "keyword": "特斯拉",
                "total_count": 30,
                "opinion_count": 5,
                "opinions": [
                    {
                        "title": "特斯拉降价引发车主不满",
                        "url": "https://news.sina.com.cn/...",
                        "is_opinion": True,
                        "sentiment": "消极",
                        "summary": "特斯拉降价引发车主抗议",
                        "companies": ["特斯拉"],
                        "people": ["马斯克"]
                    }
                ]
            }
        }