"""Custom exception classes."""

class OpinionAnalyzerError(Exception):
    """基础异常类."""
    pass

class CrawlerError(OpinionAnalyzerError):
    """爬虫相关异常."""
    pass

class RequestError(CrawlerError):
    """请求错误."""
    pass

class ParseError(CrawlerError):
    """解析错误."""
    pass

class APIError(OpinionAnalyzerError):
    """API调用相关异常."""
    pass

class ConfigError(OpinionAnalyzerError):
    """配置相关异常."""
    pass