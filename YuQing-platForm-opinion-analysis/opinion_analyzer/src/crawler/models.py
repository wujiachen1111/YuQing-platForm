"""Crawler data models."""
from typing import Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class NewsItem(BaseModel):
    """新闻条目模型.
    
    Attributes:
        title: 新闻标题
        url: 新闻链接
        summary: 新闻摘要
        pub_time: 发布时间
        source: 新闻来源
    """
    title: str
    url: HttpUrl
    summary: Optional[str] = None
    pub_time: Optional[str] = None
    source: Optional[str] = None

class NewsContent(BaseModel):
    """新闻内容模型.
    
    Attributes:
        title: 新闻标题
        content: 新闻正文
        pub_time: 发布时间
        url: 新闻链接
        author: 作者
        source: 新闻来源
    """
    title: str
    content: str
    pub_time: Optional[str] = None
    url: HttpUrl
    author: Optional[str] = None
    source: Optional[str] = None