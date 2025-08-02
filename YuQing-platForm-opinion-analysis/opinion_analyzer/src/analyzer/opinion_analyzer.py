"""Opinion analysis module using Deepseek V3 model."""
from typing import Dict, List, Optional
import json
import requests
from ..utils.logger import get_logger
from ..utils.exceptions import APIError
from ..utils.cache import Cache, cached
from ..config import get_settings
from .models import SentimentType, Entity, AnalysisResult

logger = get_logger(__name__)

# 创建缓存实例
analysis_cache = Cache(ttl=7200)  # 分析结果缓存2小时

class OpinionAnalyzer:
    """新闻舆情分析器.
    
    该类使用Deepseek V3模型分析新闻内容，判断是否为舆情新闻，
    并提取情感倾向、相关实体等信息。
    
    Attributes:
        api_key: Deepseek API密钥
        api_url: Deepseek API地址
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化分析器.
        
        Args:
            api_key: Deepseek API密钥，如果为None则从环境变量获取
        """
        settings = get_settings()
        self.api_key = api_key or settings.deepseek_api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"  # 在测试中会被mock
    
    def _get_completion(self, prompt: str) -> str:
        """获取Deepseek API补全结果.
        
        Args:
            prompt: 提示词
            
        Returns:
            str: API返回的文本
            
        Raises:
            APIError: API调用失败
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek-chat",  # 需要替换为实际的模型名称
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个专业的新闻分析助手，擅长分析新闻文本中的舆情信息。请用中文回复。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            if not data or "choices" not in data or not data["choices"]:
                raise APIError("API响应格式错误: 缺少必要字段")
            
            return data["choices"][0]["message"]["content"]
            
        except requests.RequestException as e:
            raise APIError(f"API请求失败: {e}")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise APIError(f"API响应格式错误: {e}")
        except Exception as e:
            raise APIError(f"API调用失败: {e}")
    
    @cached(analysis_cache, key_prefix="analysis")
    def analyze_sentiment(self, text: str) -> SentimentType:
        """分析文本情感倾向.
        
        Args:
            text: 待分析文本
            
        Returns:
            SentimentType: 情感倾向
            
        Raises:
            APIError: API调用失败
        """
        prompt = f"""请分析以下文本的情感倾向，只返回"积极"、"消极"或"中性"其中之一：

{text}"""
        
        try:
            result = self._get_completion(prompt).strip()
            if not result:
                raise APIError("情感分析失败: 响应为空")
            sentiment_map = {
                "积极": "positive",
                "消极": "negative",
                "中性": "neutral"
            }
            # 确保返回值是有效的情感类型
            sentiment = sentiment_map.get(result, "neutral")
            if sentiment not in ["positive", "negative", "neutral"]:
                sentiment = "neutral"
            return sentiment
        except Exception as e:
            raise APIError(f"情感分析失败: {e}")
    
    def extract_entities(self, text: str) -> Dict[str, List[Entity]]:
        """提取文本中的实体.
        
        Args:
            text: 待分析文本
            
        Returns:
            Dict[str, List[Entity]]: 实体列表，按类型分组
            
        Raises:
            APIError: API调用失败
        """
        prompt = f"""请提取以下文本中的实体，并按以下规则分类：

1. 公司/机构：包括企业、政府机构、组织等（如：特斯拉、央视、国务院等）
2. 人物：仅包括自然人（如：马斯克、李强等）
3. 地点：包括国家、城市、地区、江河湖海等地理位置（如：中国、北京、长江等）
4. 项目：包括工程项目、建筑物等（如：三峡大坝、港珠澳大桥等）

请按JSON格式返回，相同类型的实体放在一起：

{text}

格式如下：
{{
    "companies": [
        {{"name": "实体名称", "type": "company", "mentions": 1}}
    ],
    "people": [
        {{"name": "实体名称", "type": "person", "mentions": 1}}
    ],
    "locations": [
        {{"name": "实体名称", "type": "location", "mentions": 1}}
    ],
    "projects": [
        {{"name": "实体名称", "type": "project", "mentions": 1}}
    ]
}}"""
        
        try:
            result = self._get_completion(prompt)
            data = json.loads(result)
            
            # 从响应中提取各类实体
            companies = [Entity(**company) for company in data.get("companies", [])]
            people = [Entity(**person) for person in data.get("people", [])]
            locations = [Entity(**location) for location in data.get("locations", [])]
            projects = [Entity(**project) for project in data.get("projects", [])]
            
            return {
                "companies": companies,
                "people": people,
                "locations": locations,
                "projects": projects
            }
        except Exception as e:
            raise APIError(f"实体提取失败: {e}")
    
    def extract_keywords(self, text: str) -> List[str]:
        """提取文本关键词.
        
        Args:
            text: 待分析文本
            
        Returns:
            List[str]: 关键词列表
            
        Raises:
            APIError: API调用失败
        """
        prompt = f"""请分析以下新闻文本：

{text}

请完成以下任务：
1. 判断新闻所属板块（只返回一个）：
   - 科技：科技创新、互联网、人工智能等
   - 金融：股市、银行、投资等
   - 政治：政策、外交、政府等
   - 环境：气候、污染、生态等
   - 民生：教育、医疗、住房等
   - 产业：工业、农业、制造业等
   - 基建：交通、能源、水利等
   - 其他：以上都不是

2. 提取最重要的3-5个关键词（每行一个）

请按以下格式返回：
板块：xxx
关键词：
- xxx
- xxx
- xxx"""
        
        try:
            result = self._get_completion(prompt)
            return [kw.strip() for kw in result.strip().split("\n") if kw.strip()]
        except Exception as e:
            raise APIError(f"关键词提取失败: {e}")
    
    def is_opinion_news(self, text: str) -> bool:
        """判断是否为舆情新闻.
        
        Args:
            text: 待分析文本
            
        Returns:
            bool: 是否为舆情新闻
            
        Raises:
            APIError: API调用失败
        """
        prompt = f"""请判断以下新闻是否属于舆情新闻，只返回"是"或"否"：

{text}"""
        
        try:
            result = self._get_completion(prompt).strip()
            return result == "是"
        except Exception as e:
            raise APIError(f"舆情判断失败: {e}")
    
    def generate_summary(self, text: str) -> str:
        """生成文本摘要.
        
        Args:
            text: 待分析文本
            
        Returns:
            str: 摘要文本
            
        Raises:
            APIError: API调用失败
        """
        prompt = f"""请用一句话总结以下文本的主要内容（不超过20字）：

{text}"""
        
        try:
            return self._get_completion(prompt).strip()
        except Exception as e:
            raise APIError(f"摘要生成失败: {e}")
    
    def analyze(
        self,
        title: str,
        url: str,
        content: str,
        pub_time: str = "",
        source: str = ""
    ) -> AnalysisResult:
        """完整分析新闻内容.
        
        Args:
            title: 新闻标题
            url: 新闻链接
            content: 新闻正文
            pub_time: 发布时间
            source: 新闻来源
            
        Returns:
            AnalysisResult: 分析结果
            
        Raises:
            APIError: API调用失败
        """
        prompt = f"""你是一名舆情分析专家，擅长识别具有争议性或公众关注度的新闻事件。请对以下新闻内容进行全面分析：

新闻内容：
{content[:2000]}  # 限制文本长度

请完成以下分析任务：

1. 舆情判断：
   - 判断是否属于舆情事件（是/否）
   - 分析情感倾向（积极/消极/中性）
   - 用一句话总结核心事件（20字以内）

2. 实体识别：
   提取文中的重要实体，按以下类别分类：
   - 机构：企业、政府部门、组织等（如：央视、国务院）
   - 人物：仅包括自然人（如：马斯克、李强）
   - 地点：国家、城市、地区、江河湖海等（如：中国、长江）
   - 项目：工程、建筑、设施等（如：三峡大坝）

3. 新闻分类：
   判断新闻所属板块（单选）：
   - 科技：科技创新、互联网、人工智能
   - 金融：股市、银行、投资理财
   - 政治：政策、外交、政府事务
   - 环境：气候、污染、生态保护
   - 民生：教育、医疗、住房问题
   - 产业：工业、农业、制造业
   - 基建：交通、能源、水利工程
   - 其他：以上都不是

4. 关键词：
   提取3-5个最具代表性的关键词

请按以下JSON格式输出：
{{
    "is_yuqing": "是/否",
    "sentiment": "积极/消极/中性",
    "summary": "事件概括",
    "companies": [
        {{"name": "机构名称", "type": "company", "mentions": 1}}
    ],
    "people": [
        {{"name": "人物名称", "type": "person", "mentions": 1}}
    ],
    "locations": [
        {{"name": "地点名称", "type": "location", "mentions": 1}}
    ],
    "projects": [
        {{"name": "项目名称", "type": "project", "mentions": 1}}
    ],
    "category": "新闻板块",
    "keywords": ["关键词1", "关键词2", "关键词3"]
}}"""
        
        try:
            result = self._get_completion(prompt)
            # 尝试清理结果中的多余内容
            result = result.strip()
            if result.startswith('```json'):
                result = result[7:]
            if result.endswith('```'):
                result = result[:-3]
            result = result.strip()
            
            data = json.loads(result)
            
            # 转换情感
            sentiment_map = {
                "积极": "positive",
                "消极": "negative",
                "中性": "neutral"
            }
            sentiment = sentiment_map.get(data.get("sentiment", "中性"), "neutral")
            
            # 从响应中提取各类实体
            companies = [Entity(**company) for company in data.get("companies", [])]
            people = [Entity(**person) for person in data.get("people", [])]
            locations = [Entity(**location) for location in data.get("locations", [])]
            projects = [Entity(**project) for project in data.get("projects", [])]
            
            # 获取关键词和板块
            keywords = data.get("keywords", [])
            category = data.get("category", "其他")
            
            # 将板块添加到关键词列表开头
            if keywords:
                keywords.insert(0, f"[{category}]")
            
            return AnalysisResult(
                title=title,
                url=url,
                pub_time=pub_time,
                source=source,
                sentiment=sentiment,
                is_opinion=data.get("is_yuqing", "否") == "是",
                companies=companies,
                people=people,
                locations=locations,
                projects=projects,
                keywords=keywords,
                summary=data.get("summary", "")
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"解析JSON失败: {e}")
            logger.error(f"原始响应: {result}")
            raise APIError(f"解析JSON失败: {e}")
        except Exception as e:
            logger.error(f"分析失败: {e}")
            raise APIError(f"分析失败: {e}")