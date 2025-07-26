package com.zanewu.yuqingplatform.service;

import com.zanewu.yuqingplatform.vo.SentimentAnalysisRequestVO;
import com.zanewu.yuqingplatform.vo.SentimentAnalysisResponseVO;
import com.zanewu.yuqingplatform.vo.StockAnalysisRequestVO;
import com.zanewu.yuqingplatform.vo.StockAnalysisResponseVO;

import java.util.Map;

/**
 * 分析服务接口
 * @author zanewu
 */
public interface AnalysisService {

    /**
     * 股票分析
     */
    StockAnalysisResponseVO analyzeStock(StockAnalysisRequestVO request);

    /**
     * 舆情分析
     */
    SentimentAnalysisResponseVO analyzeSentiment(SentimentAnalysisRequestVO request);

    /**
     * 获取Python服务状态
     */
    Map<String, Object> getPythonServiceStatus();

    /**
     * 检查Python服务健康状态
     */
    boolean checkPythonServiceHealth();
} 