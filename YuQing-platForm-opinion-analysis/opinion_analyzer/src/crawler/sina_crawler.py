"""Sina news crawler module."""
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from ..utils.logger import get_logger
from ..utils.exceptions import RequestError, ParseError
from ..utils.cache import Cache, cached
from ..config import get_settings
from .models import NewsItem, NewsContent

logger = get_logger(__name__)

# 创建缓存实例
search_cache = Cache(ttl=3600)  # 搜索结果缓存1小时
content_cache = Cache(ttl=7200)  # 新闻内容缓存2小时

class SinaCrawler:
    """新浪新闻爬虫.
    
    该类负责从新浪新闻搜索页面获取新闻列表，并解析新闻内容。
    包含请求重试、随机延迟等反爬虫机制。
    
    Attributes:
        base_url: 新浪新闻搜索基础URL
        session: 请求会话对象
        settings: 配置对象
    """
    
    def __init__(self, base_url: str = "https://search.sina.com.cn/"):
        """初始化爬虫实例.
        
        Args:
            base_url: 新浪新闻搜索基础URL
        """
        self.base_url = base_url
        self.settings = get_settings()
        
        # 配置会话
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=self.settings.crawler_max_retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
        )
        
        # 配置适配器
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 配置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
    
    def _random_delay(self) -> None:
        """添加随机延迟，避免请求过于频繁."""
        delay = random.uniform(
            self.settings.crawler_delay_min,
            self.settings.crawler_delay_max
        )
        time.sleep(delay)
    
    @cached(search_cache, key_prefix="search")
    def search_news(self, keyword: str, limit: int = 20) -> List[NewsItem]:
        """搜索新闻.
        
        Args:
            keyword: 搜索关键词
            limit: 返回结果数量限制
            
        Returns:
            List[NewsItem]: 新闻条目列表
            
        Raises:
            RequestError: 请求失败
            ParseError: 解析失败
        """
        try:
            encoded_keyword = quote(keyword)
            search_url = f"{self.base_url}news?q={encoded_keyword}&range=all&c=news"
            
            self._random_delay()
            response = self.session.get(
                search_url,
                timeout=self.settings.crawler_timeout
            )
            response.encoding = 'utf-8'
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = []
            
            # 查找所有新闻条目
            results = soup.find_all('div', class_='box-result')
            
            for result in results[:limit]:
                try:
                    # 提取标题和链接
                    title_elem = result.find('h2')
                    if not title_elem:
                        continue
                        
                    link_elem = title_elem.find('a')
                    if not link_elem:
                        continue
                        
                    title = link_elem.get_text(strip=True)
                    url = link_elem.get('href', '')
                    
                    # 提取摘要
                    summary_elem = result.find('p', class_='content')
                    summary = summary_elem.get_text(strip=True) if summary_elem else ""
                    
                    # 提取发布时间和来源
                    time_elem = result.find('span', class_='fgray_time')
                    pub_time = time_elem.get_text(strip=True) if time_elem else ""
                    
                    source_elem = result.find('span', class_='fgray_src')
                    source = source_elem.get_text(strip=True) if source_elem else ""
                    
                    news_items.append(
                        NewsItem(
                            title=title,
                            url=url,
                            summary=summary,
                            pub_time=pub_time,
                            source=source
                        )
                    )
                    
                except Exception as e:
                    logger.warning(f"解析新闻条目失败: {e}")
                    continue
            
            return news_items
            
        except requests.RequestException as e:
            raise RequestError(f"请求搜索页面失败: {e}")
        except Exception as e:
            raise ParseError(f"解析搜索结果失败: {e}")
    
    @cached(content_cache, key_prefix="content")
    def parse_news_content(self, url: str) -> Optional[NewsContent]:
        """解析新闻内容.
        
        Args:
            url: 新闻URL
            
        Returns:
            Optional[NewsContent]: 新闻内容对象，解析失败返回None
            
        Raises:
            RequestError: 请求失败
            ParseError: 解析失败
        """
        try:
            self._random_delay()
            
            response = self.session.get(
                url,
                timeout=self.settings.crawler_timeout
            )
            response.encoding = 'utf-8'
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 处理不同类型的新闻页面
            article = (
                soup.find('div', class_='article') or
                soup.find('div', id='artibody') or
                soup.find('div', class_='article-content-left') or
                soup.find('div', class_='news_content')
            )
            
            if not article:
                logger.warning(f"未找到文章内容容器: {url}")
                return None
                
            # 获取标题
            title = (
                soup.find('h1', class_='main-title') or
                soup.find('h1', class_='article-title') or
                soup.find('h1')
            )
            title_text = title.get_text(strip=True) if title else ""
            
            # 获取发布时间
            time_elem = (
                soup.find('span', class_='date') or
                soup.find('span', class_='time-source') or
                soup.find('span', class_='time') or
                soup.find('div', class_='date-source') or
                soup.find('div', class_='date')
            )
            pub_time = time_elem.get_text(strip=True) if time_elem else ""
            
            # 获取作者
            author_elem = (
                soup.find('p', class_='author') or
                soup.find('span', class_='author') or
                soup.find('div', class_='author')
            )
            author = author_elem.get_text(strip=True) if author_elem else ""
            
            # 获取来源
            source_elem = (
                soup.find('span', class_='source') or
                soup.find('a', class_='source') or
                soup.find('span', class_='source-box') or
                soup.find('div', class_='source') or
                soup.find('a', class_='media_name')
            )
            source = source_elem.get_text(strip=True) if source_elem else ""
            
            # 清理时间和来源字符串
            pub_time = pub_time.replace("年", "-").replace("月", "-").replace("日", "")
            if "来源：" in pub_time:
                parts = pub_time.split("来源：")
                pub_time = parts[0].strip()
                if not source and len(parts) > 1:
                    source = parts[1].strip()
            
            if "来源：" in source:
                source = source.replace("来源：", "").strip()
            
            # 获取正文段落
            paragraphs = []
            for p in article.find_all(['p', 'div'], class_=lambda x: x != 'article-footer'):
                text = p.get_text(strip=True)
                if text and not any(skip in text.lower() for skip in [
                    '责任编辑', '声明：', '关注我们：', '微信扫一扫', '新浪声明',
                    '作者：', '来源：', '编辑：'
                ]):
                    paragraphs.append(text)
            
            content = '\n'.join(paragraphs)
            
            if not content:
                logger.warning(f"未提取到文章内容: {url}")
                return None
            
            return NewsContent(
                title=title_text,
                content=content,
                pub_time=pub_time,
                url=url,
                author=author,
                source=source
            )
            
        except requests.RequestException as e:
            raise RequestError(f"请求新闻页面失败: {e}")
        except Exception as e:
            raise ParseError(f"解析新闻内容失败: {e}")