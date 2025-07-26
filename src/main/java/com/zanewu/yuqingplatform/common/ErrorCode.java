package com.zanewu.yuqingplatform.common;

import lombok.Getter;

/**
 * 错误码枚举
 * @author zanewu
 */
@Getter
public enum ErrorCode {

    // 系统相关错误 1000-1999
    SUCCESS(200, "操作成功"),
    SYSTEM_ERROR(1000, "系统内部错误"),
    PARAM_ERROR(1001, "参数错误"),
    VALIDATION_ERROR(1002, "参数验证失败"),
    
    // 业务相关错误 2000-2999
    BUSINESS_ERROR(2000, "业务处理失败"),
    
    // 股票分析相关错误 3000-3099
    STOCK_CODE_INVALID(3000, "股票代码格式不正确"),
    STOCK_ANALYSIS_TYPE_INVALID(3001, "股票分析类型不支持"),
    STOCK_DATE_RANGE_INVALID(3002, "股票分析日期范围无效"),
    STOCK_ANALYSIS_FAILED(3003, "股票分析失败"),
    
    // 舆情分析相关错误 3100-3199
    SENTIMENT_CONTENT_EMPTY(3100, "舆情分析内容不能为空"),
    SENTIMENT_CONTENT_TOO_LONG(3101, "舆情分析内容过长"),
    SENTIMENT_ANALYSIS_TYPE_INVALID(3102, "舆情分析类型不支持"),
    SENTIMENT_ANALYSIS_FAILED(3103, "舆情分析失败"),
    
    // 外部服务相关错误 4000-4999
    PYTHON_SERVICE_UNAVAILABLE(4000, "Python分析服务不可用"),
    PYTHON_SERVICE_TIMEOUT(4001, "Python分析服务超时"),
    PYTHON_SERVICE_ERROR(4002, "Python分析服务返回错误"),
    
    // 网络相关错误 5000-5999
    NETWORK_ERROR(5000, "网络连接异常"),
    REQUEST_TIMEOUT(5001, "请求超时"),
    CONNECTION_REFUSED(5002, "连接被拒绝");

    private final int code;
    private final String message;

    ErrorCode(int code, String message) {
        this.code = code;
        this.message = message;
    }
} 