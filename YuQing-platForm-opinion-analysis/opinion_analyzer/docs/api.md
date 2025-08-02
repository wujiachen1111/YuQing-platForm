# 新闻舆情分析 API 文档

## 目录

- [概述](#概述)
- [基本信息](#基本信息)
- [认证](#认证)
- [API 端点](#api-端点)
  - [分析新闻舆情](#分析新闻舆情)
  - [健康检查](#健康检查)
- [数据模型](#数据模型)
- [错误处理](#错误处理)
- [性能说明](#性能说明)
- [最佳实践](#最佳实践)
- [更新日志](#更新日志)

## 概述

新闻舆情分析 API 提供了一套完整的新闻舆情分析功能，包括新闻搜索、内容爬取、舆情判断、情感分析、实体提取等。该 API 使用 AI 模型（Deepseek V3）进行智能分析，为用户提供准确的舆情洞察。

## 基本信息

- **基础URL**: `http://localhost:8000`
- **API版本**: v1.0.0
- **文档URL**: `/api/docs`（Swagger UI）或 `/api/redoc`（ReDoc）
- **OpenAPI规范**: `/api/openapi.json`

## 认证

目前版本不需要认证。未来版本可能会添加 API 密钥认证机制。

## API 端点

### 分析新闻舆情

分析指定关键词相关的新闻舆情。

**请求**:
- **方法**: POST
- **路径**: `/api/v1/analyze`
- **Content-Type**: `application/json`

**请求参数**:
```json
{
  "keyword": "示例公司",     // 必填，搜索关键词，1-50个字符
  "opinion_count": 30      // 可选，最大新闻数量，默认30，范围1-50
}
```

**响应**:
- **状态码**: 200
- **Content-Type**: `application/json`
- **响应头**:
  - `X-Process-Time`: 请求处理时间（秒）

**响应体**:
```json
{
  "keyword": "示例公司",
  "total_count": 10,        // 搜索到的新闻总数
  "opinion_count": 3,       // 舆情新闻数量
  "opinions": [             // 新闻列表
    {
      "title": "示例新闻标题",
      "url": "https://news.sina.com.cn/example",
      "pub_time": "2025-07-30 21:38",
      "source": "新闻来源",
      "sentiment": "positive",  // positive/negative/neutral
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
      "summary": "新闻内容摘要"
    }
  ]
}
```

**示例请求**:
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "Content-Type: application/json" \
     -d '{
           "keyword": "示例公司",
           "opinion_count": 30
         }'
```

**错误响应**:
```json
{
  "detail": "错误信息"
}
```

### 健康检查

检查 API 服务是否正常运行。

**请求**:
- **方法**: GET
- **路径**: `/api/v1/health`

**响应**:
- **状态码**: 200
- **Content-Type**: `application/json`

**响应体**:
```json
{
  "status": "ok"
}
```

## 数据模型

### AnalyzeRequest（分析请求）

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| keyword | string | 是 | 搜索关键词，1-50个字符 | "示例公司" |
| opinion_count | integer | 否 | 最大新闻数量，1-50之间 | 30 |

### AnalysisResult（分析结果）

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| title | string | 是 | 新闻标题 | "示例新闻标题" |
| url | string | 是 | 新闻链接 | "https://news.sina.com.cn/example" |
| pub_time | string | 否 | 发布时间 | "2025-07-30 21:38" |
| source | string | 否 | 新闻来源 | "新浪财经" |
| sentiment | string | 是 | 情感倾向 | "positive" |
| is_opinion | boolean | 是 | 是否为舆情 | true |
| companies | array | 否 | 相关机构列表 | [{"name": "示例公司", "type": "company", "mentions": 1}] |
| people | array | 否 | 相关人物列表 | [{"name": "张三", "type": "person", "mentions": 1}] |
| locations | array | 否 | 相关地点列表 | [{"name": "北京", "type": "location", "mentions": 1}] |
| projects | array | 否 | 相关项目列表 | [{"name": "示例项目", "type": "project", "mentions": 1}] |
| keywords | array | 否 | 关键词列表（第一个为新闻板块） | ["[科技]", "关键词1", "关键词2"] |
| summary | string | 是 | 新闻摘要 | "新闻内容摘要" |

### Entity（实体）

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| name | string | 是 | 实体名称 | "示例公司" |
| type | string | 是 | 实体类型（company/person/location/project） | "company" |
| mentions | integer | 是 | 提及次数 | 1 |

## 错误处理

API 使用标准的 HTTP 状态码表示请求结果：

| 状态码 | 说明 | 示例响应 |
|--------|------|----------|
| 200 | 请求成功 | `{"keyword": "...", ...}` |
| 400 | 请求参数错误 | `{"detail": "关键词不能为空"}` |
| 429 | 请求频率过高 | `{"detail": "请求过于频繁"}` |
| 500 | 服务器内部错误 | `{"detail": "服务器内部错误"}` |

## 性能说明

1. **缓存机制**:
   - 搜索结果缓存：1小时
   - 新闻内容缓存：2小时
   - 分析结果缓存：2小时

2. **请求处理时间**:
   - 通过响应头 `X-Process-Time` 返回
   - 典型处理时间：3-30秒
   - 影响因素：
     - 新闻数量
     - 新闻内容长度
     - 缓存命中率
     - 服务器负载

3. **并发处理**:
   - 支持异步处理
   - 自动负载均衡

## 最佳实践

1. **关键词选择**:
   - 使用具体的公司名、人名或事件名
   - 避免过于宽泛的关键词
   - 建议长度：2-10个字符

2. **请求频率**:
   - 建议间隔：至少1秒
   - 批量分析：使用单次请求的 opinion_count 参数
   - 优先使用缓存结果

3. **错误处理**:
   - 实现请求重试机制
   - 处理所有可能的错误状态
   - 记录详细的错误信息

4. **数据处理**:
   - 验证响应数据完整性
   - 处理特殊字符和编码
   - 注意时间格式（使用北京时间）

## 更新日志

### v1.0.0 (2025-07-30)

- 新增功能：
  - 新闻发布时间和来源提取
  - 新闻板块智能分类
  - 多维度实体识别（机构、人物、地点、项目）
  - 终端实时反馈分析结果
- 性能优化：
  - 改进爬虫的时间和来源提取
  - 优化实体分类准确度
  - 增强新闻板块分类
- 改进：
  - 更新默认返回新闻数量为30条
  - 完善错误处理和日志记录
  - 更新 API 文档