"""Analysis data models."""
from typing import List, Literal
from pydantic import BaseModel, HttpUrl

SentimentType = Literal["positive", "negative", "neutral"]

class Entity(BaseModel):
    """实体信息模型.
    
    Attributes:
        name: 实体名称
        type: 实体类型
        mentions: 提及次数
    """
    name: str
    type: str
    mentions: int = 1

class AnalysisResult(BaseModel):
    """分析结果模型.
    
    Attributes:
        title: 新闻标题
        url: 新闻链接
        sentiment: 情感倾向
        is_opinion: 是否为舆情
        companies: 相关机构
        people: 相关人物
        locations: 相关地点
        projects: 相关项目
        keywords: 关键词和新闻板块
        summary: 摘要
    """
    title: str
    url: HttpUrl
    pub_time: str = ""  # 发布时间
    source: str = ""    # 新闻来源
    sentiment: SentimentType
    is_opinion: bool
    companies: List[Entity]
    people: List[Entity]
    locations: List[Entity] = []
    projects: List[Entity] = []
    keywords: List[str]
    summary: str