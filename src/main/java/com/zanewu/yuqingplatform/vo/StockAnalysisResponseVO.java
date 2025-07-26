package com.zanewu.yuqingplatform.vo;

import com.zanewu.yuqingplatform.common.BaseVO;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/**
 * 股票分析响应VO
 * @author zanewu
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Schema(description = "股票分析响应")
public class StockAnalysisResponseVO extends BaseVO {

    @Schema(description = "股票代码")
    private String stockCode;

    @Schema(description = "股票名称")
    private String stockName;

    @Schema(description = "当前价格")
    private BigDecimal currentPrice;

    @Schema(description = "涨跌幅")
    private BigDecimal changePercent;

    @Schema(description = "分析结果")
    private AnalysisResultVO analysisResult;

    @Schema(description = "技术指标")
    private Map<String, Object> technicalIndicators;

    @Schema(description = "价格预测")
    private List<PricePredictionVO> predictions;

    @Schema(description = "风险评估")
    private RiskAssessmentVO riskAssessment;

    @Schema(description = "分析时间")
    private LocalDateTime analysisTime;

    @Data
    @Schema(description = "分析结果")
    public static class AnalysisResultVO {
        @Schema(description = "推荐操作", allowableValues = {"BUY", "SELL", "HOLD"})
        private String recommendation;

        @Schema(description = "置信度", minimum = "0", maximum = "1")
        private BigDecimal confidence;

        @Schema(description = "分析摘要")
        private String summary;

        @Schema(description = "关键因素")
        private List<String> keyFactors;
    }

    @Data
    @Schema(description = "价格预测")
    public static class PricePredictionVO {
        @Schema(description = "预测日期")
        private LocalDateTime date;

        @Schema(description = "预测价格")
        private BigDecimal predictedPrice;

        @Schema(description = "置信区间上限")
        private BigDecimal upperBound;

        @Schema(description = "置信区间下限")
        private BigDecimal lowerBound;
    }

    @Data
    @Schema(description = "风险评估")
    public static class RiskAssessmentVO {
        @Schema(description = "风险等级", allowableValues = {"LOW", "MEDIUM", "HIGH"})
        private String riskLevel;

        @Schema(description = "风险分数", minimum = "0", maximum = "100")
        private Integer riskScore;

        @Schema(description = "风险因素")
        private List<String> riskFactors;
    }
} 