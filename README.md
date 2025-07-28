# 舆情分析平台后端服务

## 项目概述

本项目是一个基于**Spring Boot 3.0**的企业级舆情分析平台后端服务，采用**Java + Python混合架构**和**VO、BO、DO分层设计**，通过REST API集成的方式实现股票分析和舆情分析功能。

### 技术架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     前端应用     │    │   Java后端服务    │    │  Python分析服务  │
│   (Vue/React)   │◄──►│  (Spring Boot)  │◄──►│ (Flask/FastAPI) │
│                 │    │                 │    │                 │
│ • 用户界面       │    │ • 业务逻辑       │    │ • 数据分析       │
│ • 数据展示       │    │ • 数据管理       │    │ • 机器学习       │
│ • 交互操作       │    │ • 服务集成       │    │ • 算法处理       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 分层架构设计

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   接口层 (VO)    │    │   业务层 (BO)    │    │   数据层 (DO)    │
│  View Object    │    │ Business Object │    │  Data Object    │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • 请求参数       │◄──►│ • 业务逻辑处理   │◄──►│ • 数据库实体     │
│ • 响应结果       │    │ • 数据转换      │    │ • 持久化操作     │
│ • API文档       │    │ • 业务验证      │    │ • 数据关系      │
│ • 参数验证       │    │ • 流程控制      │    │ • 索引优化      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 核心特性

### 🎯 业务功能
- ✅ **股票分析**: 技术分析、基本面分析、趋势预测、风险评估
- ✅ **舆情分析**: 情感分析、话题分析、热点监控、趋势追踪
- ✅ **数据持久化**: 分析记录存储、历史数据查询、统计分析

### 🏗️ 架构特性
- ✅ **分层架构**: 标准的VO、BO、DO三层数据对象设计
- ✅ **服务集成**: 通过REST API调用Python分析服务
- ✅ **异常处理**: 完善的异常处理和重试机制
- ✅ **参数验证**: 多层次参数验证和业务规则校验

### 📊 技术特性
- ✅ **API文档**: 集成Swagger/OpenAPI 3.0自动文档生成
- ✅ **监控管理**: 健康检查和服务状态监控
- ✅ **连接池**: HTTP连接池和数据库连接池优化
- ✅ **配置管理**: 统一的配置属性管理

## 技术栈

### 后端技术
- **Spring Boot 3.0**: 主框架
- **Spring Data JPA**: 数据访问层
- **Spring Validation**: 参数验证
- **Spring Retry**: 重试机制
- **MySQL 8.0**: 主数据库
- **Apache HttpClient 5**: HTTP客户端
- **Swagger/OpenAPI 3**: API文档

### 开发工具
- **Maven**: 项目构建
- **Lombok**: 代码简化
- **Jackson**: JSON序列化
- **SLF4J + Logback**: 日志管理

## 项目结构

```
src/main/java/com/zanewu/yuqingplatform/
├── common/                    # 公共基础类
│   ├── BaseParam.java         # 参数基础类
│   ├── BaseVO.java           # VO基础类
│   ├── BaseBO.java           # BO基础类
│   ├── BaseDO.java           # DO基础类
│   ├── Result.java           # 统一响应结果
│   └── ErrorCode.java        # 错误码定义
├── vo/                       # 接口层对象 (View Object)
│   ├── StockAnalysisRequestVO.java
│   ├── StockAnalysisResponseVO.java
│   ├── SentimentAnalysisRequestVO.java
│   └── SentimentAnalysisResponseVO.java
├── bo/                       # 业务层对象 (Business Object)
│   ├── StockAnalysisBO.java
│   └── SentimentAnalysisBO.java
├── entity/                   # 数据层对象 (Data Object)
│   ├── StockAnalysisRecordDO.java
│   └── SentimentAnalysisRecordDO.java
├── converter/                # 对象转换器
│   └── AnalysisConverter.java
├── controller/               # 控制器层
│   ├── AnalysisController.java
│   └── SystemController.java
├── service/                  # 业务逻辑层
│   ├── AnalysisService.java
│   └── impl/AnalysisServiceImpl.java
├── client/                   # 外部服务客户端
│   └── PythonServiceClient.java
├── repository/               # 数据访问层
│   ├── StockAnalysisRecordRepository.java
│   └── SentimentAnalysisRecordRepository.java
├── config/                   # 配置类
│   ├── WebConfig.java
│   ├── SwaggerConfig.java
│   ├── JpaConfig.java
│   └── PythonServiceProperties.java
├── validation/               # 自定义验证
│   ├── ValidStockCode.java
│   └── StockCodeValidator.java
├── exception/                # 异常处理
│   ├── BusinessException.java
│   └── GlobalExceptionHandler.java
└── YuQingPlatFormApplication.java  # 启动类
```

## 快速开始

### 环境要求

- **Java**: 17+
- **Maven**: 3.6+
- **MySQL**: 8.0+
- **Python**: 3.8+ (用于分析服务)

### 数据库初始化

```sql
-- 创建数据库
CREATE DATABASE yuqing_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户
CREATE USER 'yuqing'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON yuqing_platform.* TO 'yuqing'@'localhost';
FLUSH PRIVILEGES;
```

### 配置文件

#### application.properties
```properties
# 服务配置
server.port=8888
server.servlet.context-path=/api

# 数据库配置
spring.datasource.url=jdbc:mysql://localhost:3306/yuqing_platform?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
spring.datasource.username=yuqing
spring.datasource.password=your_password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA配置
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.database-platform=org.hibernate.dialect.MySQL8Dialect

# Python服务配置
python.service.base-url=http://localhost:5000
python.service.connect-timeout=30000
python.service.read-timeout=60000

# Python服务重试配置
python.service.retry.max-attempts=3
python.service.retry.delay=1000
python.service.retry.multiplier=2.0
python.service.retry.max-delay=30000

# Python服务连接池配置
python.service.connection-pool.max-total=200
python.service.connection-pool.default-max-per-route=20
```

### 启动服务

1. **克隆项目**
```bash
git clone <your-repository-url>
cd YuQing-platForm
```

2. **编译项目**
```bash
mvn clean compile
```

3. **启动Java后端服务**
```bash
mvn spring-boot:run
```

4. **启动Python分析服务** (需要你的同事提供)
```bash
# 示例Python服务启动命令
cd python-analysis-service
python app.py
```

### 验证服务

服务启动后，可以通过以下地址验证：

- **API文档**: http://localhost:8888/api/swagger-ui.html
- **健康检查**: http://localhost:8888/api/system/health
- **服务状态**: http://localhost:8888/api/analysis/service/status

## API接口文档

### 1. 股票分析接口

#### 股票分析
```http
POST /api/analysis/stock
Content-Type: application/json

{
  "stockCode": "000001",
  "analysisType": "TECHNICAL",
  "startDate": "2024-01-01",
  "endDate": "2024-12-31",
  "period": "DAILY",
  "pageNum": 1,
  "pageSize": 10,
  "params": {
    "indicators": ["MA", "MACD", "RSI"]
  }
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "股票分析完成",
  "data": {
    "stockCode": "000001",
    "stockName": "平安银行",
    "currentPrice": 12.50,
    "changePercent": 2.5,
    "analysisResult": {
      "recommendation": "BUY",
      "confidence": 0.85,
      "summary": "技术指标显示上涨趋势",
      "keyFactors": ["成交量放大", "突破阻力位"]
    },
    "technicalIndicators": {
      "MA5": 12.3,
      "MA10": 12.1,
      "MACD": 0.15,
      "RSI": 65.2
    },
    "riskAssessment": {
      "riskLevel": "MEDIUM",
      "riskScore": 60,
      "riskFactors": ["市场波动"]
    },
    "analysisTime": "2024-01-01T10:00:00",
    "responseTime": "2024-01-01T10:00:01"
  }
}
```

#### 快速股票分析
```http
GET /api/analysis/stock/000001/quick
```

### 2. 舆情分析接口

```http
POST /api/analysis/sentiment
Content-Type: application/json

{
  "content": "这只股票最近表现不错，值得关注",
  "analysisType": "SENTIMENT",
  "source": "ALL",
  "language": "zh",
  "keywords": ["股票", "投资"],
  "pageNum": 1,
  "pageSize": 10,
  "params": {}
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "舆情分析完成",
  "data": {
    "overallSentiment": "POSITIVE",
    "sentimentScore": 0.75,
    "confidence": 0.85,
    "sentimentDistribution": {
      "positiveRate": 0.6,
      "negativeRate": 0.2,
      "neutralRate": 0.2
    },
    "keywordSentiments": [
      {
        "keyword": "股票",
        "sentiment": "POSITIVE",
        "score": 0.8,
        "mentionCount": 5
      }
    ],
    "hotTopics": [
      {
        "topic": "投资机会",
        "hotScore": 0.9,
        "contentCount": 10,
        "dominantSentiment": "POSITIVE"
      }
    ],
    "statistics": {
      "totalCount": 1000,
      "validCount": 950,
      "sourceDistribution": {
        "WEIBO": 500,
        "NEWS": 300,
        "FORUM": 150
      }
    },
    "analysisTime": "2024-01-01T10:00:00",
    "responseTime": "2024-01-01T10:00:01"
  }
}
```

### 3. 系统管理接口

#### 系统信息
```http
GET /api/system/info
```

#### 健康检查
```http
GET /api/system/health
```

#### Python服务状态
```http
GET /api/analysis/service/status
```

**响应示例**:
```json
{
  "code": 200,
  "message": "获取服务状态成功",
  "data": {
    "baseUrl": "http://localhost:5000",
    "connectTimeout": 30000,
    "readTimeout": 60000,
    "maxRetryAttempts": 3,
    "healthy": true
  }
}
```

## Python服务接口规范

为了确保Java后端能正确调用Python服务，Python服务需要提供以下标准接口：

### 1. 股票分析接口

```http
POST http://localhost:5000/api/stock/analyze
Content-Type: application/json
User-Agent: YuQing-Platform/1.0

{
  "stockCode": "000001",
  "analysisType": "TECHNICAL",
  "startDate": "2024-01-01",
  "endDate": "2024-12-31",
  "period": "DAILY",
  "params": {}
}
```

### 2. 舆情分析接口

```http
POST http://localhost:5000/api/sentiment/analyze
Content-Type: application/json
User-Agent: YuQing-Platform/1.0

{
  "content": "分析文本内容",
  "analysisType": "SENTIMENT",
  "source": "ALL",
  "language": "zh",
  "keywords": ["关键词"],
  "startDate": "2024-01-01",
  "endDate": "2024-12-31",
  "params": {}
}
```

### 3. 健康检查接口

```http
GET http://localhost:5000/health
```

**标准响应格式**:
```json
{
  "status": "UP",
  "timestamp": "2024-01-01T10:00:00"
}
```

## 数据库设计

### 股票分析记录表 (stock_analysis_record)

| 字段名 | 类型 | 说明 | 索引 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY |
| stock_code | VARCHAR(10) | 股票代码 | INDEX |
| stock_name | VARCHAR(100) | 股票名称 | |
| analysis_type | VARCHAR(20) | 分析类型 | INDEX |
| analysis_time | DATETIME | 分析时间 | INDEX |
| recommendation | VARCHAR(20) | 推荐操作 | |
| confidence | DECIMAL(5,4) | 置信度 | |
| risk_level | VARCHAR(20) | 风险等级 | |
| create_time | DATETIME | 创建时间 | |
| update_time | DATETIME | 更新时间 | |

### 舆情分析记录表 (sentiment_analysis_record)

| 字段名 | 类型 | 说明 | 索引 |
|--------|------|------|------|
| id | BIGINT | 主键 | PRIMARY |
| content_hash | VARCHAR(64) | 内容哈希 | UNIQUE |
| analysis_type | VARCHAR(20) | 分析类型 | INDEX |
| overall_sentiment | VARCHAR(20) | 整体情感 | INDEX |
| sentiment_score | DECIMAL(5,4) | 情感分数 | |
| source | VARCHAR(20) | 数据源 | INDEX |
| analysis_time | DATETIME | 分析时间 | INDEX |
| create_time | DATETIME | 创建时间 | |
| update_time | DATETIME | 更新时间 | |

## 部署指南

### 开发环境部署

```bash
# 1. 启动MySQL数据库
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=yuqing_platform \
  -p 3306:3306 \
  mysql:8.0

# 2. 启动Java服务
mvn spring-boot:run

# 3. 启动Python服务 (端口5000)
cd python-analysis-service
python app.py
```

### 生产环境部署

#### 使用Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: yuqing_platform
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  java-backend:
    build: .
    ports:
      - "8888:8888"
    depends_on:
      - mysql
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/yuqing_platform
      PYTHON_SERVICE_BASE_URL: http://python-service:5000

  python-service:
    build: ./python-analysis-service
    ports:
      - "5000:5000"

volumes:
  mysql_data:
```

启动命令：
```bash
docker-compose up -d
```

#### 传统部署

```bash
# 1. 打包Java应用
mvn clean package -DskipTests

# 2. 启动Java服务
java -jar target/yuqing-platform-1.0.jar \
  --spring.profiles.active=prod \
  --spring.datasource.url=jdbc:mysql://your-db-host:3306/yuqing_platform

# 3. 启动Python服务
cd python-analysis-service
python app.py --host=0.0.0.0 --port=5000
```

## 监控和运维

### 应用监控

- **健康检查**: `/api/system/health`
- **服务状态**: `/api/analysis/service/status`
- **系统信息**: `/api/system/info`

### 日志管理

- **应用日志**: `logs/application.log`
- **错误日志**: `logs/error.log`
- **访问日志**: `logs/access.log`

### 性能调优

#### JVM参数优化
```bash
java -Xms2g -Xmx4g -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \
     -jar yuqing-platform.jar
```

#### 数据库优化
```sql
-- 添加索引
CREATE INDEX idx_stock_analysis_time ON stock_analysis_record(analysis_time);
CREATE INDEX idx_sentiment_analysis_time ON sentiment_analysis_record(analysis_time);

-- 分区表 (可选)
ALTER TABLE stock_analysis_record 
PARTITION BY RANGE (YEAR(analysis_time)) (
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026)
);
```

## 开发指南

### 添加新的分析功能

1. **创建VO对象**
```java
// 在vo包中创建请求和响应VO
@Data
@EqualsAndHashCode(callSuper = true)
public class NewAnalysisRequestVO extends BaseParam {
    // 请求字段
}
```

2. **创建BO对象**
```java
// 在bo包中创建业务对象
@Data
@EqualsAndHashCode(callSuper = true)
public class NewAnalysisBO extends BaseBO {
    // 业务字段和方法
}
```

3. **创建DO对象**
```java
// 在entity包中创建数据对象
@Entity
@Table(name = "new_analysis_record")
public class NewAnalysisRecordDO extends BaseDO {
    // 数据库字段
}
```

4. **扩展转换器**
```java
// 在AnalysisConverter中添加转换方法
public NewAnalysisBO convertToBO(NewAnalysisRequestVO vo) {
    // 转换逻辑
}
```

5. **添加服务方法**
```java
// 在AnalysisService中添加接口
NewAnalysisResponseVO analyzeNew(NewAnalysisRequestVO request);

// 在AnalysisServiceImpl中实现
@Override
public NewAnalysisResponseVO analyzeNew(NewAnalysisRequestVO requestVO) {
    // 实现逻辑
}
```

6. **添加控制器接口**
```java
// 在AnalysisController中添加REST接口
@PostMapping("/new")
public Result<NewAnalysisResponseVO> analyzeNew(@Valid @RequestBody NewAnalysisRequestVO request) {
    // 接口实现
}
```

### 自定义验证器

```java
// 创建验证注解
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = CustomValidator.class)
public @interface ValidCustom {
    String message() default "自定义验证失败";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

// 实现验证器
public class CustomValidator implements ConstraintValidator<ValidCustom, String> {
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        // 验证逻辑
        return true;
    }
}
```

### 错误码管理

```java
// 在ErrorCode枚举中添加新的错误码
public enum ErrorCode {
    // 新功能相关错误 4000-4099
    NEW_FEATURE_ERROR(4000, "新功能处理失败"),
    NEW_FEATURE_PARAM_INVALID(4001, "新功能参数无效");
}
```

## 最佳实践

### 1. 代码规范
- 遵循阿里巴巴Java开发手册
- 使用统一的命名规范
- 保持代码简洁和可读性

### 2. 异常处理
- 使用统一的异常处理机制
- 记录详细的错误日志
- 返回用户友好的错误信息

### 3. 性能优化
- 合理使用缓存
- 优化数据库查询
- 避免N+1查询问题

### 4. 安全考虑
- 输入参数验证
- SQL注入防护
- 敏感信息脱敏

## 常见问题

### Q1: Python服务连接失败怎么办？
**A**: 检查以下几点：
1. Python服务是否正常启动
2. 网络连接是否正常
3. 防火墙设置是否正确
4. 配置文件中的URL是否正确

### Q2: 数据库连接池配置建议？
**A**: 推荐配置：
```properties
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000
spring.datasource.hikari.idle-timeout=600000
spring.datasource.hikari.max-lifetime=1800000
```

### Q3: 如何处理大数据量分析？
**A**: 建议：
1. 使用分页查询
2. 异步处理长时间任务
3. 考虑使用消息队列
4. 实现数据分片

### Q4: 如何扩展支持更多分析类型？
**A**: 按照开发指南中的步骤：
1. 定义新的VO、BO、DO对象
2. 扩展转换器和服务层
3. 添加相应的控制器接口
4. 更新Python服务接口

## 版本历史

- **v1.0.0**: 初始版本，支持基础的股票和舆情分析
- **v1.1.0**: 重构为VO、BO、DO分层架构，增强代码规范性
- **v1.2.0**: 增加数据持久化和历史记录查询功能

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- **项目负责人**: zanewu
- **邮箱**: wujunhao0921@gmail.com
- **项目地址**: https://github.com/wujiachen1111/YuQing-platForm

---

**注意**: 本项目依赖Python分析服务，请确保Python服务按照接口规范正确实现并优先启动。 




分层架构重构完成
我已经成功将你的后端框架重构为标准的VO、BO、DO分层架构，这是一个非常专业和规范的设计。
🎯 重构成果
1. 完整的基础类体系
BaseParam: 统一的参数基础类，支持分页、排序、链路追踪
BaseVO: 视图对象基础类，包含响应时间、版本控制等
BaseBO: 业务对象基础类，包含业务处理状态和扩展信息
BaseDO: 数据对象基础类，包含审计字段和乐观锁
2. 标准分层数据对象
VO层: StockAnalysisRequestVO、SentimentAnalysisRequestVO 等
BO层: StockAnalysisBO、SentimentAnalysisBO 等
DO层: StockAnalysisRecordDO、SentimentAnalysisRecordDO 等
3. 专业的转换器设计
AnalysisConverter: 负责VO↔BO↔DO之间的转换
支持Python服务DTO的双向转换
清晰的转换流程和职责分工
4. 完善的Repository层
专门的数据访问接口
丰富的查询方法
数据库索引优化
📋 架构优势
职责分离: 每层专注自己的职责，VO负责接口传输，BO负责业务逻辑，DO负责数据持久化
可维护性: 统一的基础类减少重复代码，清晰的分层便于维护
可扩展性: 基础类支持扩展，转换器支持复杂映射
数据安全: 不同层次的数据隔离，敏感信息过滤
性能优化: 按需转换，数据库索引优化，JSON字段支持

请求流程: VO → BO → Python DTO → Python Service
响应流程: Python DTO → BO → VO → 客户端  
持久化流程: BO → DO → Database
