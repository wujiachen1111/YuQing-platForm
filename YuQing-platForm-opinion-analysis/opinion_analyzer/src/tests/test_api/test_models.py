"""Test cases for API models."""
import pytest
from pydantic import ValidationError
from src.api.models import AnalyzeRequest, AnalyzeResponse
from src.analyzer.models import AnalysisResult, Entity

def test_analyze_request_valid():
    """测试有效的分析请求."""
    request = AnalyzeRequest(keyword="测试", opinion_count=20)
    assert request.keyword == "测试"
    assert request.opinion_count == 20

def test_analyze_request_default_opinion_count():
    """测试分析请求默认值."""
    request = AnalyzeRequest(keyword="测试")
    assert request.keyword == "测试"
    assert request.opinion_count == 20  # 默认值

def test_analyze_request_invalid_keyword():
    """测试无效的关键词."""
    with pytest.raises(ValidationError) as exc_info:
        AnalyzeRequest(keyword="")
    assert "ensure this value has at least 1 characters" in str(exc_info.value)
    
    with pytest.raises(ValidationError) as exc_info:
        AnalyzeRequest(keyword="   ")
    assert "关键词不能为空" in str(exc_info.value)
    
    with pytest.raises(ValidationError) as exc_info:
        AnalyzeRequest(keyword="a" * 51)
    assert "ensure this value has at most 50 characters" in str(exc_info.value)

def test_analyze_request_invalid_opinion_count():
    """测试无效的新闻数量."""
    with pytest.raises(ValidationError) as exc_info:
        AnalyzeRequest(keyword="测试", opinion_count=0)
    assert "ensure this value is greater than or equal to 1" in str(exc_info.value)
    
    with pytest.raises(ValidationError) as exc_info:
        AnalyzeRequest(keyword="测试", opinion_count=51)
    assert "ensure this value is less than or equal to 50" in str(exc_info.value)

def test_analyze_response_valid():
    """测试有效的分析响应."""
    response = AnalyzeResponse(
        keyword="测试",
        total_count=20,
        opinion_count=5,
        opinions=[
            AnalysisResult(
                title="测试新闻",
                url="http://test.com/news",
                content="测试内容",
                pub_time="2024-03-19 10:00",
                source="测试来源",
                sentiment="positive",
                is_opinion=True,
                companies=[Entity(name="测试公司", type="company", mentions=1)],
                people=[Entity(name="测试人物", type="person", mentions=1)],
                keywords=["关键词1", "关键词2"],
                summary="测试摘要"
            )
        ]
    )
    assert response.keyword == "测试"
    assert response.total_count == 20
    assert response.opinion_count == 5
    assert len(response.opinions) == 1
    
    opinion = response.opinions[0]
    assert opinion.title == "测试新闻"
    assert opinion.url == "http://test.com/news"
    assert opinion.is_opinion is True
    assert opinion.sentiment == "positive"
    assert len(opinion.companies) == 1
    assert len(opinion.people) == 1
    assert len(opinion.keywords) == 2
    assert opinion.summary == "测试摘要"

def test_analyze_response_invalid_counts():
    """测试无效的数量."""
    with pytest.raises(ValidationError) as exc_info:
        AnalyzeResponse(
            keyword="测试",
            total_count=-1,  # 无效的总数
            opinion_count=5,
            opinions=[]
        )
    assert "ensure this value is greater than or equal to 0" in str(exc_info.value)
    
    with pytest.raises(ValidationError) as exc_info:
        AnalyzeResponse(
            keyword="测试",
            total_count=20,
            opinion_count=-1,  # 无效的舆情数量
            opinions=[]
        )
    assert "ensure this value is greater than or equal to 0" in str(exc_info.value)

def test_analyze_response_serialization():
    """测试响应序列化."""
    response = AnalyzeResponse(
        keyword="测试",
        total_count=20,
        opinion_count=5,
        opinions=[
            AnalysisResult(
                title="测试新闻",
                url="http://test.com/news",
                content="测试内容",
                pub_time="2024-03-19 10:00",
                source="测试来源",
                sentiment="positive",
                is_opinion=True,
                companies=[Entity(name="测试公司", type="company", mentions=1)],
                people=[Entity(name="测试人物", type="person", mentions=1)],
                keywords=["关键词1", "关键词2"],
                summary="测试摘要"
            )
        ]
    )
    
    # 序列化为JSON
    json_data = response.json()
    
    # 反序列化
    restored = AnalyzeResponse.parse_raw(json_data)
    
    # 验证字段
    assert restored.keyword == response.keyword
    assert restored.total_count == response.total_count
    assert restored.opinion_count == response.opinion_count
    assert len(restored.opinions) == len(response.opinions)
    
    # 验证舆情字段
    restored_opinion = restored.opinions[0]
    original_opinion = response.opinions[0]
    assert restored_opinion.title == original_opinion.title
    assert restored_opinion.url == original_opinion.url
    assert restored_opinion.is_opinion == original_opinion.is_opinion
    assert restored_opinion.sentiment == original_opinion.sentiment
    assert len(restored_opinion.companies) == len(original_opinion.companies)
    assert len(restored_opinion.people) == len(original_opinion.people)
    assert len(restored_opinion.keywords) == len(original_opinion.keywords)
    assert restored_opinion.summary == original_opinion.summary