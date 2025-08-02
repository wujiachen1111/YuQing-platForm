"""Unit tests for the crawler module."""
import pytest
import requests_mock
from src.crawler.sina_crawler import SinaCrawler, search_cache, content_cache
from src.utils.exceptions import RequestError, ParseError

@pytest.fixture(autouse=True)
def clear_cache():
    """清空缓存."""
    search_cache.clear()
    content_cache.clear()

@pytest.fixture
def crawler():
    """创建爬虫实例."""
    return SinaCrawler()

def test_search_news_success(crawler, requests_mock):
    """测试成功搜索新闻."""
    # 模拟搜索结果
    requests_mock.get(
        "https://search.sina.com.cn/news?q=%E6%B5%8B%E8%AF%95&range=all&c=news",
        text="""
        <div class="box-result">
            <h2><a href="http://test.com/news1">测试新闻标题1</a></h2>
            <p class="content">测试新闻摘要1</p>
            <span class="fgray_time">2024-01-30 10:00</span>
            <span class="fgray_src">新浪财经</span>
        </div>
        <div class="box-result">
            <h2><a href="http://test.com/news2">测试新闻标题2</a></h2>
            <p class="content">测试新闻摘要2</p>
            <span class="fgray_time">2024-01-30 11:00</span>
            <span class="fgray_src">新浪科技</span>
        </div>
        """
    )
    
    # 执行搜索
    news_list = crawler.search_news("测试", limit=2)
    
    # 验证结果
    assert len(news_list) == 2
    assert news_list[0].title == "测试新闻标题1"
    assert news_list[0].url == "http://test.com/news1"
    assert news_list[0].summary == "测试新闻摘要1"
    assert news_list[0].pub_time == "2024-01-30 10:00"
    assert news_list[0].source == "新浪财经"
    
    assert news_list[1].title == "测试新闻标题2"
    assert news_list[1].url == "http://test.com/news2"
    assert news_list[1].summary == "测试新闻摘要2"
    assert news_list[1].pub_time == "2024-01-30 11:00"
    assert news_list[1].source == "新浪科技"

def test_search_news_request_error(crawler, requests_mock):
    """测试搜索请求失败."""
    # 模拟请求失败
    requests_mock.get(
        "https://search.sina.com.cn/news?q=%E6%B5%8B%E8%AF%95&range=all&c=news",
        status_code=500
    )
    
    # 验证异常
    with pytest.raises(RequestError):
        crawler.search_news("测试")

def test_search_news_parse_error(crawler, requests_mock):
    """测试搜索结果解析失败."""
    # 模拟无效的HTML响应
    requests_mock.get(
        "https://search.sina.com.cn/news?q=%E6%B5%8B%E8%AF%95&range=all&c=news",
        text="<invalid>html</invalid>"
    )
    
    # 验证结果为空列表（解析单个条目失败会被跳过）
    news_list = crawler.search_news("测试")
    assert len(news_list) == 0

def test_parse_news_content_success(crawler, requests_mock):
    """测试成功解析新闻内容."""
    # 模拟新闻页面
    requests_mock.get(
        "http://test.com/news1",
        text="""
        <div class="article">
            <h1 class="main-title">测试新闻标题</h1>
            <span class="date">2024-01-30 10:00</span>
            <span class="source">新浪财经</span>
            <p class="author">作者：张三</p>
            <p>第一段内容</p>
            <p>第二段内容</p>
            <p class="article-footer">责任编辑：李四</p>
        </div>
        """
    )
    
    # 解析内容
    content = crawler.parse_news_content("http://test.com/news1")
    
    # 验证结果
    assert content is not None
    assert content.title == "测试新闻标题"
    assert content.pub_time == "2024-01-30 10:00"
    assert content.source == "新浪财经"
    assert content.author == "作者：张三"
    assert content.content == "第一段内容\n第二段内容"

def test_parse_news_content_request_error(crawler, requests_mock):
    """测试解析新闻内容请求失败."""
    # 模拟请求失败
    requests_mock.get(
        "http://test.com/news1",
        status_code=404
    )
    
    # 验证异常
    with pytest.raises(RequestError):
        crawler.parse_news_content("http://test.com/news1")

def test_parse_news_content_no_article(crawler, requests_mock):
    """测试新闻页面没有文章内容."""
    # 模拟没有文章内容的页面
    requests_mock.get(
        "http://test.com/news1",
        text="""
        <div class="header">
            <h1>测试新闻标题</h1>
        </div>
        """
    )
    
    # 验证返回None
    content = crawler.parse_news_content("http://test.com/news1")
    assert content is None

def test_search_cache(crawler, requests_mock):
    """测试搜索结果缓存."""
    # 模拟搜索结果
    requests_mock.get(
        "https://search.sina.com.cn/news?q=%E6%B5%8B%E8%AF%95&range=all&c=news",
        text="""
        <div class="box-result">
            <h2><a href="http://test.com/news1">测试新闻标题1</a></h2>
            <p class="content">测试新闻摘要1</p>
        </div>
        """
    )
    
    # 第一次搜索
    news_list1 = crawler.search_news("测试")
    assert len(news_list1) == 1
    
    # 修改模拟响应
    requests_mock.get(
        "https://search.sina.com.cn/news?q=%E6%B5%8B%E8%AF%95&range=all&c=news",
        text="""
        <div class="box-result">
            <h2><a href="http://test.com/news2">测试新闻标题2</a></h2>
            <p class="content">测试新闻摘要2</p>
        </div>
        """
    )
    
    # 第二次搜索应该返回缓存结果
    news_list2 = crawler.search_news("测试")
    assert len(news_list2) == 1
    assert news_list2[0].title == news_list1[0].title

def test_content_cache(crawler, requests_mock):
    """测试新闻内容缓存."""
    # 模拟新闻页面
    requests_mock.get(
        "http://test.com/news1",
        text="""
        <div class="article">
            <h1>测试新闻标题1</h1>
            <p>测试内容1</p>
        </div>
        """
    )
    
    # 第一次解析
    content1 = crawler.parse_news_content("http://test.com/news1")
    assert content1 is not None
    
    # 修改模拟响应
    requests_mock.get(
        "http://test.com/news1",
        text="""
        <div class="article">
            <h1>测试新闻标题2</h1>
            <p>测试内容2</p>
        </div>
        """
    )
    
    # 第二次解析应该返回缓存结果
    content2 = crawler.parse_news_content("http://test.com/news1")
    assert content2 is not None
    assert content2.title == content1.title