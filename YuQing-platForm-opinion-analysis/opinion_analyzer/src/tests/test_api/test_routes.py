"""Test cases for API routes."""
import os
import json
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from src.api.main import app
from src.crawler.models import NewsItem, NewsContent
from src.analyzer.models import Entity
from src.config import Settings

# 设置测试环境文件路径
os.environ["ENV_FILE"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test.env")

client = TestClient(app)

def test_analyze_news_success():
    """测试成功分析新闻."""
    # Mock爬虫结果
    mock_news_items = [
        NewsItem(
            title="测试新闻1",
            url="http://test.com/news1",
            summary="测试摘要1",
            pub_time="2024-03-19 10:00"
        )
    ]
    
    mock_news_content = NewsContent(
        title="测试新闻1",
        content="测试内容",
        pub_time="2024-03-19 10:00",
        url="http://test.com/news1"
    )
    
    # Mock API响应
    mock_api_response = {
        "is_yuqing": "是",
        "sentiment": "积极",
        "summary": "测试摘要",
        "entities": ["测试公司", "测试人物"]
    }
    
    with patch('src.api.routes.SinaCrawler') as MockCrawler, \
         patch('src.api.routes.OpinionAnalyzer._get_completion') as mock_get_completion:
        
        # 配置Mock
        mock_crawler = MockCrawler.return_value
        mock_crawler.search_news.return_value = mock_news_items
        mock_crawler.parse_news_content.return_value = mock_news_content
        
        mock_get_completion.return_value = json.dumps(mock_api_response)
        
        # 发送请求
        response = client.post(
            "/api/v1/analyze",
            json={
                "keyword": "测试",
                "limit": 1
            }
        )
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert data["keyword"] == "测试"
        assert data["total"] == 1
        assert data["opinion_count"] == 1
        assert len(data["news"]) == 1
        
        news = data["news"][0]
        assert news["title"] == "测试新闻1"
        assert news["sentiment"] == "positive"
        assert news["is_opinion"] is True
        assert len(news["companies"]) == 1
        assert len(news["people"]) == 1
        assert len(news["keywords"]) == 0
        assert news["summary"] == "测试摘要"

def test_analyze_news_crawler_error():
    """测试爬虫错误处理."""
    with patch('src.api.routes.SinaCrawler') as MockCrawler:
        mock_crawler = MockCrawler.return_value
        mock_crawler.search_news.side_effect = Exception("爬取失败")
        
        response = client.post(
            "/api/v1/analyze",
            json={
                "keyword": "测试",
                "limit": 1
            }
        )
        
        assert response.status_code == 500
        assert "爬取失败" in response.json()["detail"]

def test_analyze_news_analyzer_error():
    """测试分析器错误处理."""
    mock_news_items = [
        NewsItem(
            title="测试新闻1",
            url="http://test.com/news1",
            summary="测试摘要1"
        )
    ]
    
    mock_news_content = NewsContent(
        title="测试新闻1",
        content="测试内容",
        url="http://test.com/news1"
    )
    
    with patch('src.api.routes.SinaCrawler') as MockCrawler, \
         patch('src.api.routes.OpinionAnalyzer._get_completion') as mock_get_completion:
        
        mock_crawler = MockCrawler.return_value
        mock_crawler.search_news.return_value = mock_news_items
        mock_crawler.parse_news_content.return_value = mock_news_content
        
        mock_get_completion.side_effect = Exception("分析失败")
        
        response = client.post(
            "/api/v1/analyze",
            json={
                "keyword": "测试",
                "limit": 1
            }
        )
        
        assert response.status_code == 500
        assert "分析失败" in response.json()["detail"]