# API 使用示例

本文档提供了新闻舆情分析 API 的使用示例，包括不同编程语言的代码示例和常见场景的使用方法。

## Python 示例

### 基本使用

```python
import requests
import json

def analyze_news(keyword: str, limit: int = 20) -> dict:
    """分析新闻舆情.
    
    Args:
        keyword: 搜索关键词
        limit: 最大新闻数量
        
    Returns:
        dict: 分析结果
    """
    url = "http://localhost:8000/api/v1/analyze"
    
    data = {
        "keyword": keyword,
        "limit": limit
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    
    return response.json()

# 使用示例
try:
    result = analyze_news("示例公司", limit=10)
    
    print(f"总新闻数: {result['total']}")
    print(f"舆情新闻数: {result['opinion_count']}")
    
    for news in result['news']:
        print("\n新闻:", news['title'])
        print("情感:", news['sentiment'])
        print("是否舆情:", news['is_opinion'])
        print("摘要:", news['summary'])
        
        if news['companies']:
            print("相关公司:", [company['name'] for company in news['companies']])
        
        if news['people']:
            print("相关人物:", [person['name'] for person in news['people']])
            
except requests.RequestException as e:
    print(f"请求失败: {e}")
except KeyError as e:
    print(f"解析响应失败: {e}")
```

### 异步使用

```python
import asyncio
import aiohttp

async def analyze_news_async(keyword: str, limit: int = 20) -> dict:
    """异步分析新闻舆情.
    
    Args:
        keyword: 搜索关键词
        limit: 最大新闻数量
        
    Returns:
        dict: 分析结果
    """
    url = "http://localhost:8000/api/v1/analyze"
    
    data = {
        "keyword": keyword,
        "limit": limit
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()

# 使用示例
async def main():
    try:
        result = await analyze_news_async("示例公司", limit=10)
        print(f"总新闻数: {result['total']}")
        print(f"舆情新闻数: {result['opinion_count']}")
    except aiohttp.ClientError as e:
        print(f"请求失败: {e}")

asyncio.run(main())
```

## JavaScript/TypeScript 示例

### 使用 Fetch API

```typescript
interface AnalysisRequest {
  keyword: string;
  limit?: number;
}

interface Entity {
  name: string;
  type: string;
  mentions: number;
}

interface NewsInfo {
  title: string;
  url: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  is_opinion: boolean;
  companies: Entity[];
  people: Entity[];
  keywords: string[];
  summary: string;
  pub_time: string;
}

interface AnalysisResponse {
  keyword: string;
  total: number;
  opinion_count: number;
  news: NewsInfo[];
}

async function analyzeNews(
  keyword: string,
  limit: number = 20
): Promise<AnalysisResponse> {
  const url = 'http://localhost:8000/api/v1/analyze';
  
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      keyword,
      limit,
    }),
  });
  
  if (!response.ok) {
    throw new Error(`请求失败: ${response.statusText}`);
  }
  
  return response.json();
}

// 使用示例
async function main() {
  try {
    const result = await analyzeNews('示例公司', 10);
    
    console.log(`总新闻数: ${result.total}`);
    console.log(`舆情新闻数: ${result.opinion_count}`);
    
    result.news.forEach(news => {
      console.log('\n新闻:', news.title);
      console.log('情感:', news.sentiment);
      console.log('是否舆情:', news.is_opinion);
      console.log('摘要:', news.summary);
      
      if (news.companies.length) {
        console.log('相关公司:', news.companies.map(c => c.name));
      }
      
      if (news.people.length) {
        console.log('相关人物:', news.people.map(p => p.name));
      }
    });
  } catch (error) {
    console.error('分析失败:', error);
  }
}

main();
```

### 使用 Axios

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,  // 30秒超时
});

async function analyzeNews(
  keyword: string,
  limit: number = 20
): Promise<AnalysisResponse> {
  const { data } = await api.post<AnalysisResponse>('/api/v1/analyze', {
    keyword,
    limit,
  });
  
  return data;
}

// 使用示例与上面相同
```

## 常见场景

### 1. 批量分析

```python
async def batch_analyze(keywords: list[str]) -> list[dict]:
    """批量分析多个关键词.
    
    Args:
        keywords: 关键词列表
        
    Returns:
        list[dict]: 分析结果列表
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for keyword in keywords:
            task = asyncio.create_task(
                analyze_news_async(keyword, session=session)
            )
            tasks.append(task)
        
        return await asyncio.gather(*tasks)

# 使用示例
keywords = ["公司A", "公司B", "公司C"]
results = asyncio.run(batch_analyze(keywords))
```

### 2. 定时监控

```python
import schedule
import time

def monitor_news():
    """定时监控新闻舆情."""
    try:
        result = analyze_news("目标公司")
        
        # 检查是否有新的舆情
        if result['opinion_count'] > 0:
            # 发送通知
            send_notification(result)
            
    except Exception as e:
        print(f"监控失败: {e}")

# 每小时执行一次
schedule.every().hour.do(monitor_news)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 3. 数据分析

```python
import pandas as pd
from collections import Counter

def analyze_trends(results: list[dict]) -> dict:
    """分析舆情趋势.
    
    Args:
        results: 多次分析的结果列表
        
    Returns:
        dict: 趋势分析结果
    """
    # 转换为DataFrame
    news_data = []
    for result in results:
        for news in result['news']:
            news_data.append({
                'date': news['pub_time'],
                'sentiment': news['sentiment'],
                'is_opinion': news['is_opinion'],
                'companies': [c['name'] for c in news['companies']],
                'people': [p['name'] for p in news['people']]
            })
    
    df = pd.DataFrame(news_data)
    
    # 分析情感趋势
    sentiment_trend = df['sentiment'].value_counts().to_dict()
    
    # 分析相关实体
    all_companies = [c for news in df['companies'] for c in news]
    company_mentions = Counter(all_companies)
    
    all_people = [p for news in df['people'] for p in news]
    people_mentions = Counter(all_people)
    
    return {
        'sentiment_trend': sentiment_trend,
        'top_companies': dict(company_mentions.most_common(5)),
        'top_people': dict(people_mentions.most_common(5))
    }
```

## 注意事项

1. **错误处理**
   - 始终包装API调用在try-catch块中
   - 处理网络错误、超时和服务器错误
   - 实现重试机制

2. **性能优化**
   - 使用异步请求处理并发
   - 实现本地缓存
   - 批量处理时控制并发数量

3. **数据验证**
   - 验证响应数据的完整性
   - 处理特殊字符和编码
   - 注意时间格式的处理

4. **资源管理**
   - 正确关闭网络连接
   - 释放不再需要的资源
   - 控制内存使用