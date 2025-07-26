package com.zanewu.yuqingplatform.converter;

import com.zanewu.yuqingplatform.bo.SentimentAnalysisBO;
import com.zanewu.yuqingplatform.bo.StockAnalysisBO;
import com.zanewu.yuqingplatform.dto.SentimentAnalysisRequest;
import com.zanewu.yuqingplatform.dto.SentimentAnalysisResponse;
import com.zanewu.yuqingplatform.dto.StockAnalysisRequest;
import com.zanewu.yuqingplatform.dto.StockAnalysisResponse;
import com.zanewu.yuqingplatform.entity.SentimentAnalysisRecordDO;
import com.zanewu.yuqingplatform.entity.StockAnalysisRecordDO;
import com.zanewu.yuqingplatform.vo.SentimentAnalysisRequestVO;
import com.zanewu.yuqingplatform.vo.SentimentAnalysisResponseVO;
import com.zanewu.yuqingplatform.vo.StockAnalysisRequestVO;
import com.zanewu.yuqingplatform.vo.StockAnalysisResponseVO;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.UUID;

/**
 * 分析对象转换器
 * @author zanewu
 */
@Component
public class AnalysisConverter {

    // ===== 股票分析相关转换 =====

    /**
     * VO -> BO
     */
    public StockAnalysisBO convertToBO(StockAnalysisRequestVO vo) {
        if (vo == null) return null;
        
        StockAnalysisBO bo = new StockAnalysisBO();
        bo.setStockCode(vo.getStockCode());
        bo.setAnalysisType(vo.getAnalysisType());
        bo.setPeriod(vo.getPeriod());
        bo.setStartDate(vo.getStartDate());
        bo.setEndDate(vo.getEndDate());
        bo.setAnalysisStartTime(LocalDateTime.now());
        
        // 设置业务处理信息
        bo.setProcessor("SYSTEM");
        bo.setProcessStatus("PROCESSING");
        bo.setExtendData(vo.getParams());
        
        return bo;
    }

    /**
     * BO -> VO
     */
    public StockAnalysisResponseVO convertToVO(StockAnalysisBO bo) {
        if (bo == null) return null;
        
        StockAnalysisResponseVO vo = new StockAnalysisResponseVO();
        vo.setStockCode(bo.getStockCode());
        vo.setStockName(bo.getStockName());
        vo.setCurrentPrice(bo.getCurrentPrice());
        vo.setChangePercent(bo.getChangePercent());
        vo.setAnalysisTime(bo.getAnalysisEndTime());
        vo.setResponseTime(LocalDateTime.now());
        
        // 转换分析结果
        if (bo.getAnalysisResult() != null) {
            StockAnalysisResponseVO.AnalysisResultVO resultVO = new StockAnalysisResponseVO.AnalysisResultVO();
            resultVO.setRecommendation(bo.getAnalysisResult().getRecommendation());
            resultVO.setConfidence(bo.getAnalysisResult().getConfidence());
            resultVO.setSummary(bo.getAnalysisResult().getSummary());
            resultVO.setKeyFactors(bo.getAnalysisResult().getKeyFactors());
            vo.setAnalysisResult(resultVO);
        }
        
        return vo;
    }

    /**
     * BO -> DO
     */
    public StockAnalysisRecordDO convertToDO(StockAnalysisBO bo) {
        if (bo == null) return null;
        
        StockAnalysisRecordDO dO = new StockAnalysisRecordDO();
        dO.setStockCode(bo.getStockCode());
        dO.setStockName(bo.getStockName());
        dO.setAnalysisType(bo.getAnalysisType());
        dO.setPeriod(bo.getPeriod());
        dO.setStartDate(bo.getStartDate());
        dO.setEndDate(bo.getEndDate());
        dO.setCurrentPrice(bo.getCurrentPrice());
        dO.setChangePercent(bo.getChangePercent());
        dO.setAnalysisTime(bo.getAnalysisEndTime());
        dO.setAnalysisDuration(bo.getAnalysisDuration());
        dO.setRequestId(UUID.randomUUID().toString());
        
        // 转换分析结果
        if (bo.getAnalysisResult() != null) {
            dO.setRecommendation(bo.getAnalysisResult().getRecommendation());
            dO.setConfidence(bo.getAnalysisResult().getConfidence());
            dO.setAnalysisSummary(bo.getAnalysisResult().getSummary());
            // TODO: 将复杂对象序列化为JSON字符串
        }
        
        return dO;
    }

    // ===== 舆情分析相关转换 =====

    /**
     * VO -> BO
     */
    public SentimentAnalysisBO convertToBO(SentimentAnalysisRequestVO vo) {
        if (vo == null) return null;
        
        SentimentAnalysisBO bo = new SentimentAnalysisBO();
        bo.setContent(vo.getContent());
        bo.setContentLength(vo.getContent().length());
        bo.setAnalysisType(vo.getAnalysisType());
        bo.setSource(vo.getSource());
        bo.setLanguage(vo.getLanguage());
        bo.setKeywords(vo.getKeywords());
        bo.setStartDate(vo.getStartDate());
        bo.setEndDate(vo.getEndDate());
        bo.setAnalysisStartTime(LocalDateTime.now());
        
        // 设置业务处理信息
        bo.setProcessor("SYSTEM");
        bo.setProcessStatus("PROCESSING");
        bo.setExtendData(vo.getParams());
        
        return bo;
    }

    /**
     * BO -> VO
     */
    public SentimentAnalysisResponseVO convertToVO(SentimentAnalysisBO bo) {
        if (bo == null) return null;
        
        SentimentAnalysisResponseVO vo = new SentimentAnalysisResponseVO();
        vo.setOverallSentiment(bo.getOverallSentiment());
        vo.setSentimentScore(bo.getSentimentScore());
        vo.setConfidence(bo.getConfidence());
        vo.setAnalysisTime(bo.getAnalysisEndTime());
        vo.setResponseTime(LocalDateTime.now());
        
        // 转换情感分布
        if (bo.getSentimentDistribution() != null) {
            SentimentAnalysisResponseVO.SentimentDistributionVO distributionVO = 
                new SentimentAnalysisResponseVO.SentimentDistributionVO();
            distributionVO.setPositiveRate(bo.getSentimentDistribution().getPositiveRate());
            distributionVO.setNegativeRate(bo.getSentimentDistribution().getNegativeRate());
            distributionVO.setNeutralRate(bo.getSentimentDistribution().getNeutralRate());
            vo.setSentimentDistribution(distributionVO);
        }
        
        return vo;
    }

    /**
     * BO -> DO
     */
    public SentimentAnalysisRecordDO convertToDO(SentimentAnalysisBO bo) {
        if (bo == null) return null;
        
        SentimentAnalysisRecordDO dO = new SentimentAnalysisRecordDO();
        dO.setContent(bo.getContent());
        dO.setContentLength(bo.getContentLength());
        dO.setAnalysisType(bo.getAnalysisType());
        dO.setSource(bo.getSource());
        dO.setLanguage(bo.getLanguage());
        dO.setOverallSentiment(bo.getOverallSentiment());
        dO.setSentimentScore(bo.getSentimentScore());
        dO.setConfidence(bo.getConfidence());
        dO.setAnalysisTime(bo.getAnalysisEndTime());
        dO.setAnalysisDuration(bo.getAnalysisDuration());
        dO.setRequestId(UUID.randomUUID().toString());
        
        // 转换情感分布
        if (bo.getSentimentDistribution() != null) {
            dO.setPositiveRate(bo.getSentimentDistribution().getPositiveRate());
            dO.setNegativeRate(bo.getSentimentDistribution().getNegativeRate());
            dO.setNeutralRate(bo.getSentimentDistribution().getNeutralRate());
        }
        
        // TODO: 将复杂对象序列化为JSON字符串
        
        return dO;
    }

    // ===== Python服务DTO转换 =====

    /**
     * BO -> Python Request DTO
     */
    public StockAnalysisRequest convertToPythonRequest(StockAnalysisBO bo) {
        if (bo == null) return null;
        
        StockAnalysisRequest dto = new StockAnalysisRequest();
        dto.setStockCode(bo.getStockCode());
        dto.setAnalysisType(bo.getAnalysisType());
        dto.setPeriod(bo.getPeriod());
        dto.setStartDate(bo.getStartDate());
        dto.setEndDate(bo.getEndDate());
        dto.setParams((java.util.Map<String, Object>) bo.getExtendData());
        
        return dto;
    }

    /**
     * Python Response DTO -> BO
     */
    public void updateBOFromPythonResponse(StockAnalysisBO bo, StockAnalysisResponse dto) {
        if (bo == null || dto == null) return;
        
        bo.setStockName(dto.getStockName());
        bo.setCurrentPrice(dto.getCurrentPrice());
        bo.setChangePercent(dto.getChangePercent());
        bo.setTechnicalIndicators(dto.getTechnicalIndicators());
        bo.setAnalysisEndTime(LocalDateTime.now());
        
        // 转换分析结果
        if (dto.getAnalysisResult() != null) {
            StockAnalysisBO.AnalysisResult result = new StockAnalysisBO.AnalysisResult();
            result.setRecommendation(dto.getAnalysisResult().getRecommendation());
            result.setConfidence(dto.getAnalysisResult().getConfidence());
            result.setSummary(dto.getAnalysisResult().getSummary());
            result.setKeyFactors(dto.getAnalysisResult().getKeyFactors());
            bo.setAnalysisResult(result);
        }
    }

    /**
     * BO -> Python Request DTO (舆情)
     */
    public SentimentAnalysisRequest convertToPythonRequest(SentimentAnalysisBO bo) {
        if (bo == null) return null;
        
        SentimentAnalysisRequest dto = new SentimentAnalysisRequest();
        dto.setContent(bo.getContent());
        dto.setAnalysisType(bo.getAnalysisType());
        dto.setSource(bo.getSource());
        dto.setLanguage(bo.getLanguage());
        dto.setKeywords(bo.getKeywords());
        dto.setStartDate(bo.getStartDate());
        dto.setEndDate(bo.getEndDate());
        dto.setParams((java.util.Map<String, Object>) bo.getExtendData());
        
        return dto;
    }

    /**
     * Python Response DTO -> BO (舆情)
     */
    public void updateBOFromPythonResponse(SentimentAnalysisBO bo, SentimentAnalysisResponse dto) {
        if (bo == null || dto == null) return;
        
        bo.setOverallSentiment(dto.getOverallSentiment());
        bo.setSentimentScore(dto.getSentimentScore());
        bo.setConfidence(dto.getConfidence());
        bo.setAnalysisEndTime(LocalDateTime.now());
        
        // 转换情感分布
        if (dto.getSentimentDistribution() != null) {
            SentimentAnalysisBO.SentimentDistribution distribution = new SentimentAnalysisBO.SentimentDistribution();
            distribution.setPositiveRate(dto.getSentimentDistribution().getPositiveRate());
            distribution.setNegativeRate(dto.getSentimentDistribution().getNegativeRate());
            distribution.setNeutralRate(dto.getSentimentDistribution().getNeutralRate());
            bo.setSentimentDistribution(distribution);
        }
    }
} 