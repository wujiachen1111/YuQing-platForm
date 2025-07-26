package com.zanewu.yuqingplatform.bo;

import com.zanewu.yuqingplatform.common.BaseBO;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/**
 * 股票分析业务对象
 * @author zanewu
 */
@Data
@EqualsAndHashCode(callSuper = true)
public class StockAnalysisBO extends BaseBO {

    /**
     * 股票代码
     */
    private String stockCode;

    /**
     * 股票名称
     */
    private String stockName;

    /**
     * 分析类型
     */
    private String analysisType;

    /**
     * 分析周期
     */
    private String period;

    /**
     * 开始日期
     */
    private LocalDate startDate;

    /**
     * 结束日期
     */
    private LocalDate endDate;

    /**
     * 当前价格
     */
    private BigDecimal currentPrice;

    /**
     * 涨跌幅
     */
    private BigDecimal changePercent;

    /**
     * 分析结果
     */
    private AnalysisResult analysisResult;

    /**
     * 技术指标
     */
    private Map<String, Object> technicalIndicators;

    /**
     * 价格预测列表
     */
    private List<PricePrediction> predictions;

    /**
     * 风险评估
     */
    private RiskAssessment riskAssessment;

    /**
     * 分析开始时间
     */
    private LocalDateTime analysisStartTime;

    /**
     * 分析结束时间
     */
    private LocalDateTime analysisEndTime;

    /**
     * 数据源信息
     */
    private Map<String, Object> dataSource;

    /**
     * 业务规则验证结果
     */
    private ValidationResult validationResult;

    @Data
    public static class AnalysisResult {
        private String recommendation;
        private BigDecimal confidence;
        private String summary;
        private List<String> keyFactors;
        private String riskLevel;
    }

    @Data
    public static class PricePrediction {
        private LocalDateTime date;
        private BigDecimal predictedPrice;
        private BigDecimal upperBound;
        private BigDecimal lowerBound;
        private BigDecimal accuracy;
    }

    @Data
    public static class RiskAssessment {
        private String riskLevel;
        private Integer riskScore;
        private List<String> riskFactors;
        private BigDecimal volatility;
        private String riskCategory;
    }

    @Data
    public static class ValidationResult {
        private Boolean isValid;
        private List<String> errorMessages;
        private List<String> warningMessages;
        private String validationStatus;
    }

    /**
     * 计算分析耗时（毫秒）
     */
    public Long getAnalysisDuration() {
        if (analysisStartTime != null && analysisEndTime != null) {
            return java.time.Duration.between(analysisStartTime, analysisEndTime).toMillis();
        }
        return null;
    }

    /**
     * 判断是否为高风险股票
     */
    public Boolean isHighRisk() {
        return riskAssessment != null && "HIGH".equals(riskAssessment.getRiskLevel());
    }
} 