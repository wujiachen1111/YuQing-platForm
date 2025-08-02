"""Test cases for opinion analyzer."""
import json
import pytest
from unittest.mock import Mock, patch
import requests
from src.analyzer.opinion_analyzer import OpinionAnalyzer
from src.analyzer.models import Entity, AnalysisResult
from src.utils.exceptions import APIError

@pytest.fixture
def analyzer():
    """创建分析器实例."""
    return OpinionAnalyzer("test_key")

def mock_api_response(content: str):
    """创建模拟的API响应."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": content
                }
            }
        ]
    }
    return mock_response

def test_analyze_sentiment(analyzer):
    """测试情感分析."""
    with patch.object(analyzer, '_get_completion', return_value="积极"):
        sentiment = analyzer.analyze_sentiment("测试文本")
        assert sentiment == "positive"

def test_extract_entities(analyzer):
    """测试实体提取."""
    mock_response = '''
    {
        "companies": [
            {"name": "测试公司", "type": "company", "mentions": 2}
        ],
        "people": [
            {"name": "测试人物", "type": "person", "mentions": 1}
        ]
    }
    '''
    
    with patch('requests.post') as mock_post:
        mock_post.return_value = mock_api_response(mock_response)
        entities = analyzer.extract_entities("测试文本")
        
        assert len(entities["companies"]) == 1
        assert len(entities["people"]) == 1
        assert isinstance(entities["companies"][0], Entity)
        assert isinstance(entities["people"][0], Entity)
        assert entities["companies"][0].name == "测试公司"
        assert entities["people"][0].name == "测试人物"

def test_extract_keywords(analyzer):
    """测试关键词提取."""
    mock_keywords = """关键词1
关键词2
关键词3"""
    
    with patch('requests.post') as mock_post:
        mock_post.return_value = mock_api_response(mock_keywords)
        keywords = analyzer.extract_keywords("测试文本")
        
        assert len(keywords) == 3
        assert "关键词1" in keywords
        assert "关键词2" in keywords
        assert "关键词3" in keywords

def test_is_opinion_news(analyzer):
    """测试舆情判断."""
    with patch('requests.post') as mock_post:
        mock_post.return_value = mock_api_response("是")
        is_opinion = analyzer.is_opinion_news("测试文本")
        assert is_opinion is True

def test_generate_summary(analyzer):
    """测试摘要生成."""
    mock_summary = "这是一个测试摘要"
    
    with patch('requests.post') as mock_post:
        mock_post.return_value = mock_api_response(mock_summary)
        summary = analyzer.generate_summary("测试文本")
        assert summary == mock_summary

def test_analyze_non_opinion_news(analyzer):
    """测试非舆情新闻分析."""
    mock_response = {
        "is_yuqing": "否",
        "sentiment": "中性",
        "summary": "测试摘要",
        "entities": []
    }
    
    with patch.object(analyzer, '_get_completion', return_value=json.dumps(mock_response)):
        result = analyzer.analyze(
            title="测试新闻",
            url="http://test.com/news",
            content="测试内容"
        )
        
        assert isinstance(result, AnalysisResult)
        assert result.is_opinion is False
        assert result.sentiment == "neutral"
        assert len(result.companies) == 0
        assert len(result.people) == 0
        assert len(result.keywords) == 0

def test_analyze_opinion_news(analyzer):
    """测试舆情新闻分析."""
    mock_response = {
        "is_yuqing": "是",
        "sentiment": "积极",
        "summary": "测试摘要",
        "entities": ["测试公司", "测试人物"]
    }
    
    with patch.object(analyzer, '_get_completion', return_value=json.dumps(mock_response)):
        result = analyzer.analyze(
            title="测试新闻",
            url="http://test.com/news",
            content="测试内容"
        )
        
        assert isinstance(result, AnalysisResult)
        assert result.is_opinion is True
        assert result.sentiment == "positive"
        assert len(result.companies) == 1
        assert len(result.people) == 1
        assert len(result.keywords) == 0
        assert result.summary == "测试摘要"

def test_api_error_on_request_failure(analyzer):
    """测试API请求失败的错误处理."""
    with patch('requests.post', side_effect=requests.RequestException("请求失败")):
        with pytest.raises(APIError) as exc_info:
            analyzer._get_completion("测试文本")
        assert "API请求失败" in str(exc_info.value)

def test_api_error_on_invalid_response(analyzer):
    """测试API响应无效的错误处理."""
    with patch('requests.post') as mock_post:
        mock_post.return_value = Mock()
        mock_post.return_value.json.return_value = {}  # 返回空响应
        mock_post.return_value.raise_for_status = Mock()  # 不抛出HTTP错误
        
        with pytest.raises(APIError) as exc_info:
            analyzer._get_completion("测试文本")
        assert "API响应格式错误" in str(exc_info.value)