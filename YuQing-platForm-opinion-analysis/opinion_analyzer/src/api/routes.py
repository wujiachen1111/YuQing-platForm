"""API routes module."""
from typing import List
from fastapi import APIRouter, HTTPException
from ..crawler.sina_crawler import SinaCrawler
from ..analyzer.opinion_analyzer import OpinionAnalyzer
from ..analyzer.models import AnalysisResult
from ..utils.exceptions import RequestError, ParseError, APIError
from ..utils.logger import get_logger
from . import models

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1")

@router.post(
    "/analyze",
    response_model=models.AnalyzeResponse,
    summary="分析关键词相关新闻的舆情",
    description="""
    输入关键词，分析相关新闻的舆情。
    
    - 搜索新浪新闻获取相关新闻
    - 爬取新闻内容
    - 使用AI分析是否为舆情
    - 如果是舆情，分析情感倾向和关键实体
    """,
    response_description="舆情分析结果"
)
async def analyze_news(
    request: models.AnalyzeRequest
) -> models.AnalyzeResponse:
    """分析关键词相关新闻的舆情.
    
    Args:
        request: 分析请求
        
    Returns:
        AnalyzeResponse: 分析结果
        
    Raises:
        HTTPException: 当爬虫或分析失败时
    """
    try:
        # 初始化爬虫和分析器
        crawler = SinaCrawler()
        analyzer = OpinionAnalyzer()
        
        # 搜索新闻
        news_list = crawler.search_news(request.keyword)
        if not news_list:
            return models.AnalyzeResponse(
                keyword=request.keyword,
                total_count=0,
                opinion_count=0,
                opinions=[]
            )
            
        # 限制新闻数量
        news_list = news_list[:request.opinion_count]
        
        # 分析结果
        analysis_results: List[AnalysisResult] = []
        
        # 处理每条新闻
        for news in news_list:
            try:
                # 爬取新闻内容
                content = crawler.parse_news_content(news.url)
                if not content:
                    continue
                    
                # 分析新闻
                result = analyzer.analyze(
                    title=news.title,
                    url=news.url,
                    content=content.content,
                    pub_time=content.pub_time,
                    source=content.source
                )
                
                # 如果是舆情，添加到结果中
                if result.is_opinion:
                    analysis_results.append(result)
                        
            except (RequestError, ParseError, APIError) as e:
                # 记录错误但继续处理其他新闻
                print(f"处理新闻失败: {str(e)}")  # 临时使用 print 替代 logger
                continue
                
        # 构建响应
        response = models.AnalyzeResponse(
            keyword=request.keyword,
            total_count=len(news_list),
            opinion_count=len(analysis_results),
            opinions=analysis_results
        )
        
        # 在终端打印分析结果
        print("\n=== 舆情分析结果 ===")
        print(f"关键词: {request.keyword}")
        print(f"搜索到的新闻总数: {len(news_list)}")
        print(f"舆情新闻数量: {len(analysis_results)}")
        
        if analysis_results:
            print("\n具体舆情:")
            for i, result in enumerate(analysis_results, 1):
                print(f"\n[{i}] {result.title}")
                print(f"发布时间: {result.pub_time or '未知'}")
                print(f"来源: {result.source or '未知'}")
                print(f"链接: {result.url}")
                print(f"情感: {result.sentiment}")
                print(f"摘要: {result.summary}")
                if result.companies:
                    print("相关机构:", ", ".join(e.name for e in result.companies))
                if result.people:
                    print("相关人物:", ", ".join(e.name for e in result.people))
                if result.locations:
                    print("相关地点:", ", ".join(e.name for e in result.locations))
                if result.projects:
                    print("相关项目:", ", ".join(e.name for e in result.projects))
                if result.keywords:
                    print("关键词:", ", ".join(result.keywords))
        
        return response
        
    except (RequestError, ParseError, APIError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"分析失败: {str(e)}"
        )

