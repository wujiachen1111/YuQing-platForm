# 舆情分析服务

这是一个基于 Deepseek V3 模型的舆情分析服务，可以分析新闻文本中的舆情信息，包括情感倾向、相关实体等。

## 功能特点

- 输入关键词，自动搜索相关新闻
- 爬取新闻内容并进行舆情分析
- 提供 RESTful API 接口
- 支持情感分析、实体提取、摘要生成等功能
- 智能分类新闻板块（科技、金融、政治等）
- 多维度实体识别（机构、人物、地点、项目）

## 安装

1. 安装 Python 3.9 或更高版本
2. 使用 Poetry 安装依赖：

```bash
# 安装 Poetry
pip install poetry

# 安装项目依赖
poetry install
```

## 配置

1. 创建 `.env` 文件并设置以下环境变量：

```env
DEEPSEEK_API_KEY=your_api_key
```

2. 可选配置项：

```env
CRAWLER_TIMEOUT=30
CRAWLER_MAX_RETRIES=3
CRAWLER_DELAY_MIN=0.5
CRAWLER_DELAY_MAX=2.0
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=true
```

## 运行

启动 API 服务：

```bash
python run.py
```

服务将在 http://127.0.0.1:8000 上运行。

## API 文档

API 文档可在服务运行后通过 http://127.0.0.1:8000/api/docs 访问。

### 主要接口

#### 1. 舆情分析

```http
POST /api/v1/analyze
```

请求体：
```json
{
    "keyword": "搜索关键词",
    "opinion_count": 30  // 可选，默认30条
}
```

响应：
```json
{
    "keyword": "搜索关键词",
    "total_count": 10,
    "opinion_count": 3,
    "opinions": [
        {
            "title": "新闻标题",
            "url": "新闻链接",
            "pub_time": "2025-07-30 21:38",
            "source": "新闻来源",
            "sentiment": "positive/negative/neutral",
            "is_opinion": true,
            "companies": [
                {
                    "name": "机构名称",
                    "type": "company",
                    "mentions": 1
                }
            ],
            "people": [
                {
                    "name": "人物名称",
                    "type": "person",
                    "mentions": 1
                }
            ],
            "locations": [
                {
                    "name": "地点名称",
                    "type": "location",
                    "mentions": 1
                }
            ],
            "projects": [
                {
                    "name": "项目名称",
                    "type": "project",
                    "mentions": 1
                }
            ],
            "keywords": ["[板块]", "关键词1", "关键词2"],
            "summary": "新闻摘要"
        }
    ]
}
```

#### 2. 健康检查

```http
GET /api/v1/health
```

响应：
```json
{
    "status": "ok"
}
```

## 开发

### 项目结构

```
opinion_analyzer/
├── src/
│   ├── api/            # API 相关代码
│   │   ├── main.py     # FastAPI 应用
│   │   ├── routes.py   # API 路由
│   │   └── models.py   # API 数据模型
│   ├── analyzer/       # 舆情分析模块
│   │   ├── opinion_analyzer.py  # 分析器核心
│   │   └── models.py   # 分析数据模型
│   ├── crawler/        # 新闻爬虫模块
│   │   ├── sina_crawler.py  # 新浪新闻爬虫
│   │   └── models.py   # 爬虫数据模型
│   └── utils/          # 工具函数
│       ├── logger.py   # 日志工具
│       ├── cache.py    # 缓存工具
│       ├── config.py   # 配置工具
│       └── exceptions.py  # 异常定义
├── docs/              # 文档
├── tests/             # 测试代码
├── .env               # 环境变量配置
├── pyproject.toml     # 项目依赖配置
└── run.py            # 服务入口
```

### 运行测试

```bash
poetry run pytest
```

### 手动测试

```bash
# 测试分析器
python src/tests/manual/test_analyzer.py

# 测试 API
python src/tests/manual/test_api.py
```

## 许可证

MIT