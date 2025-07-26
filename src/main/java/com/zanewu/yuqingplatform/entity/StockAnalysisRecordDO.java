package com.zanewu.yuqingplatform.entity;

import com.zanewu.yuqingplatform.common.BaseDO;
import lombok.Data;
import lombok.EqualsAndHashCode;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 股票分析记录数据对象
 * @author zanewu
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "stock_analysis_record", indexes = {
    @Index(name = "idx_stock_code", columnList = "stock_code"),
    @Index(name = "idx_analysis_time", columnList = "analysis_time"),
    @Index(name = "idx_analysis_type", columnList = "analysis_type")
})
public class StockAnalysisRecordDO extends BaseDO {

    @Column(name = "stock_code", nullable = false, length = 10)
    private String stockCode;

    @Column(name = "stock_name", length = 100)
    private String stockName;

    @Column(name = "analysis_type", nullable = false, length = 20)
    private String analysisType;

    @Column(name = "analysis_period", length = 20)
    private String period;

    @Column(name = "start_date")
    private LocalDate startDate;

    @Column(name = "end_date")
    private LocalDate endDate;

    @Column(name = "current_price", precision = 10, scale = 2)
    private BigDecimal currentPrice;

    @Column(name = "change_percent", precision = 8, scale = 4)
    private BigDecimal changePercent;

    @Column(name = "recommendation", length = 20)
    private String recommendation;

    @Column(name = "confidence", precision = 5, scale = 4)
    private BigDecimal confidence;

    @Column(name = "risk_level", length = 20)
    private String riskLevel;

    @Column(name = "risk_score")
    private Integer riskScore;

    @Column(name = "analysis_summary", columnDefinition = "TEXT")
    private String analysisSummary;

    @Column(name = "key_factors", columnDefinition = "JSON")
    private String keyFactors;

    @Column(name = "technical_indicators", columnDefinition = "JSON")
    private String technicalIndicators;

    @Column(name = "predictions", columnDefinition = "JSON")
    private String predictions;

    @Column(name = "risk_factors", columnDefinition = "JSON")
    private String riskFactors;

    @Column(name = "analysis_time", nullable = false)
    private LocalDateTime analysisTime;

    @Column(name = "analysis_duration")
    private Long analysisDuration;

    @Column(name = "data_source", columnDefinition = "JSON")
    private String dataSource;

    @Column(name = "status", length = 20, nullable = false)
    private String status = "COMPLETED";

    @Column(name = "error_message", columnDefinition = "TEXT")
    private String errorMessage;

    @Column(name = "request_id", length = 64)
    private String requestId;
} 