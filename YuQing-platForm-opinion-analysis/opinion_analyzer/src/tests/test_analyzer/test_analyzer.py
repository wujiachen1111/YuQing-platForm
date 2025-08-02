"""Test analyzer functionality."""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.crawler.sina_crawler import SinaCrawler
from src.analyzer.opinion_analyzer import OpinionAnalyzer

def test_analyzer():
    """Test the analyzer with real news."""
    # 确保设置了API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请设置OPENAI_API_KEY环境变量")
        return
        
    # 创建爬虫和分析器实例
    crawler = SinaCrawler()
    analyzer = OpinionAnalyzer(api_key)
    
    # 获取新闻数据
    keyword = "特斯拉"
    results = crawler.search_news(keyword, limit=3)
    
    print(f"\n分析关键词 '{keyword}' 的新闻：")
    
    for idx, result in enumerate(results, 1):
        print(f"\n{idx}. {result['title']}")
        print(f"URL: {result['url']}")
        
        # 获取完整新闻内容
        if content := crawler.parse_news_content(result['url']):
            # 判断是否为舆情新闻
            is_opinion = analyzer.is_opinion_news(content['content'])
            print(f"是否为舆情新闻: {'是' if is_opinion else '否'}")
            
            if is_opinion:
                # 分析情感倾向
                sentiment = analyzer.analyze_sentiment(content['content'])
                print(f"情感倾向: {sentiment}")
                
                # 提取实体
                entities = analyzer.extract_entities(content['content'])
                print("\n提取的实体信息：")
                print(f"相关公司: {', '.join(entities['companies'])}")
                print(f"相关人物: {', '.join(entities['people'])}")
                print(f"关键词: {', '.join(entities['keywords'])}")
            
        print("-" * 80)

if __name__ == "__main__":
    test_analyzer()