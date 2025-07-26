package com.zanewu.yuqingplatform.service.impl;

import com.zanewu.yuqingplatform.bo.SentimentAnalysisBO;
import com.zanewu.yuqingplatform.bo.StockAnalysisBO;
import com.zanewu.yuqingplatform.client.PythonServiceClient;
import com.zanewu.yuqingplatform.common.ErrorCode;
import com.zanewu.yuqingplatform.converter.AnalysisConverter;
import com.zanewu.yuqingplatform.dto.SentimentAnalysisRequest;
import com.zanewu.yuqingplatform.dto.SentimentAnalysisResponse;
import com.zanewu.yuqingplatform.dto.StockAnalysisRequest;
import com.zanewu.yuqingplatform.dto.StockAnalysisResponse;
import com.zanewu.yuqingplatform.exception.BusinessException;
import com.zanewu.yuqingplatform.service.AnalysisService;
import com.zanewu.yuqingplatform.vo.SentimentAnalysisRequestVO;
import com.zanewu.yuqingplatform.vo.SentimentAnalysisResponseVO;
import com.zanewu.yuqingplatform.vo.StockAnalysisRequestVO;
import com.zanewu.yuqingplatform.vo.StockAnalysisResponseVO;
import lombok.extern.slf4j.Slf4j;

import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.time.LocalDate;
import java.util.Map;

/**
 * 分析服务实现类
 * @author zanewu
 */
@Slf4j
@Service
public class AnalysisServiceImpl implements AnalysisService {

    private final PythonServiceClient pythonServiceClient;
    private final AnalysisConverter analysisConverter;

    public AnalysisServiceImpl(PythonServiceClient pythonServiceClient, AnalysisConverter analysisConverter) {
        this.pythonServiceClient = pythonServiceClient;
        this.analysisConverter = analysisConverter;
    }

    @Override
    public StockAnalysisResponseVO analyzeStock(StockAnalysisRequestVO requestVO) {
        log.info("开始股票分析，股票代码: {}", requestVO.getStockCode());
        
        // VO -> BO 转换
        StockAnalysisBO analysisBO = analysisConverter.convertToBO(requestVO);
        
        // 参数验证
        validateStockAnalysisRequest(requestVO);
        
        try {
            // BO -> Python DTO 转换
            StockAnalysisRequest pythonRequest = analysisConverter.convertToPythonRequest(analysisBO);
            
            // 调用Python服务进行分析
            StockAnalysisResponse pythonResponse = pythonServiceClient.analyzeStock(pythonRequest);
            
            // 更新BO对象
            analysisConverter.updateBOFromPythonResponse(analysisBO, pythonResponse);
            
            // BO -> VO 转换
            StockAnalysisResponseVO responseVO = analysisConverter.convertToVO(analysisBO);
            
            log.info("股票分析完成 - 股票代码: {}, 分析类型: {}, 推荐操作: {}", 
                    requestVO.getStockCode(), 
                    requestVO.getAnalysisType(),
                    responseVO.getAnalysisResult() != null ? responseVO.getAnalysisResult().getRecommendation() : "未知");
            
            return responseVO;
            
        } catch (BusinessException e) {
            // 业务异常直接抛出
            throw e;
        } catch (Exception e) {
            log.error("股票分析失败 - 股票代码: {}, 分析类型: {}, 错误: {}", 
                    requestVO.getStockCode(), requestVO.getAnalysisType(), e.getMessage(), e);
            throw new BusinessException(ErrorCode.STOCK_ANALYSIS_FAILED, "股票分析失败: " + e.getMessage());
        }
    }

    @Override
    public SentimentAnalysisResponseVO analyzeSentiment(SentimentAnalysisRequestVO requestVO) {
        log.info("开始舆情分析，分析类型: {}", requestVO.getAnalysisType());
        
        // VO -> BO 转换
        SentimentAnalysisBO analysisBO = analysisConverter.convertToBO(requestVO);
        
        // 参数验证
        validateSentimentAnalysisRequest(requestVO);
        
        try {
            // BO -> Python DTO 转换
            SentimentAnalysisRequest pythonRequest = analysisConverter.convertToPythonRequest(analysisBO);
            
            // 调用Python服务进行分析
            SentimentAnalysisResponse pythonResponse = pythonServiceClient.analyzeSentiment(pythonRequest);
            
            // 更新BO对象
            analysisConverter.updateBOFromPythonResponse(analysisBO, pythonResponse);
            
            // BO -> VO 转换
            SentimentAnalysisResponseVO responseVO = analysisConverter.convertToVO(analysisBO);
            
            log.info("舆情分析完成 - 分析类型: {}, 整体情感: {}, 情感分数: {}, 内容长度: {}", 
                    requestVO.getAnalysisType(),
                    responseVO.getOverallSentiment(), 
                    responseVO.getSentimentScore(),
                    requestVO.getContent().length());
            
            return responseVO;
            
        } catch (BusinessException e) {
            // 业务异常直接抛出
            throw e;
        } catch (Exception e) {
            log.error("舆情分析失败 - 分析类型: {}, 内容长度: {}, 错误: {}", 
                    requestVO.getAnalysisType(), requestVO.getContent().length(), e.getMessage(), e);
            throw new BusinessException(ErrorCode.SENTIMENT_ANALYSIS_FAILED, "舆情分析失败: " + e.getMessage());
        }
    }

    @Override
    public Map<String, Object> getPythonServiceStatus() {
        return pythonServiceClient.getServiceStatus();
    }

    @Override
    public boolean checkPythonServiceHealth() {
        return pythonServiceClient.checkHealth();
    }

    /**
     * 验证股票分析请求参数
     */
    private void validateStockAnalysisRequest(StockAnalysisRequestVO request) {
        if (!StringUtils.hasText(request.getStockCode())) {
            throw new BusinessException(ErrorCode.STOCK_CODE_INVALID, "股票代码不能为空");
        }
        
        if (!StringUtils.hasText(request.getAnalysisType())) {
            throw new BusinessException(ErrorCode.STOCK_ANALYSIS_TYPE_INVALID, "分析类型不能为空");
        }
        
        // 验证日期范围
        if (request.getStartDate() != null && request.getEndDate() != null) {
            if (request.getStartDate().isAfter(request.getEndDate())) {
                throw new BusinessException(ErrorCode.STOCK_DATE_RANGE_INVALID, "开始日期不能晚于结束日期");
            }
            
            if (request.getEndDate().isAfter(LocalDate.now())) {
                throw new BusinessException(ErrorCode.STOCK_DATE_RANGE_INVALID, "结束日期不能晚于当前日期");
            }
        }
    }

    /**
     * 验证舆情分析请求参数
     */
    private void validateSentimentAnalysisRequest(SentimentAnalysisRequestVO request) {
        if (!StringUtils.hasText(request.getContent())) {
            throw new BusinessException(ErrorCode.SENTIMENT_CONTENT_EMPTY);
        }
        
        if (request.getContent().length() > 10000) {
            throw new BusinessException(ErrorCode.SENTIMENT_CONTENT_TOO_LONG);
        }
        
        // 验证日期范围
        if (request.getStartDate() != null && request.getEndDate() != null) {
            if (request.getStartDate().isAfter(request.getEndDate())) {
                throw new BusinessException(ErrorCode.PARAM_ERROR, "开始日期不能晚于结束日期");
            }
        }
    }
} 