package com.zanewu.yuqingplatform.entity;

import com.zanewu.yuqingplatform.common.BaseDO;
import lombok.Data;
import lombok.EqualsAndHashCode;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * 舆情分析记录数据对象
 * @author zanewu
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Entity
@Table(name = "sentiment_analysis_record", indexes = {
    @Index(name = "idx_analysis_time", columnList = "analysis_time"),
    @Index(name = "idx_analysis_type", columnList = "analysis_type"),
    @Index(name = "idx_overall_sentiment", columnList = "overall_sentiment"),
    @Index(name = "idx_source", columnList = "source")
})
public class SentimentAnalysisRecordDO extends BaseDO {

    @Column(name = "content", columnDefinition = "TEXT", nullable = false)
    private String content;

    @Column(name = "content_length")
    private Integer contentLength;

    @Column(name = "content_hash", length = 64)
    private String contentHash;

    @Column(name = "analysis_type", nullable = false, length = 20)
    private String analysisType;

    @Column(name = "source", length = 20)
    private String source;

    @Column(name = "language", length = 10)
    private String language;

    @Column(name = "keywords", columnDefinition = "JSON")
    private String keywords;

    @Column(name = "start_date")
    private LocalDate startDate;

    @Column(name = "end_date")
    private LocalDate endDate;

    @Column(name = "overall_sentiment", length = 20)
    private String overallSentiment;

    @Column(name = "sentiment_score", precision = 5, scale = 4)
    private BigDecimal sentimentScore;

    @Column(name = "confidence", precision = 5, scale = 4)
    private BigDecimal confidence;

    @Column(name = "positive_rate", precision = 5, scale = 4)
    private BigDecimal positiveRate;

    @Column(name = "negative_rate", precision = 5, scale = 4)
    private BigDecimal negativeRate;

    @Column(name = "neutral_rate", precision = 5, scale = 4)
    private BigDecimal neutralRate;

    @Column(name = "keyword_sentiments", columnDefinition = "JSON")
    private String keywordSentiments;

    @Column(name = "hot_topics", columnDefinition = "JSON")
    private String hotTopics;

    @Column(name = "sentiment_trends", columnDefinition = "JSON")
    private String sentimentTrends;

    @Column(name = "total_count")
    private Integer totalCount;

    @Column(name = "valid_count")
    private Integer validCount;

    @Column(name = "filtered_count")
    private Integer filteredCount;

    @Column(name = "source_distribution", columnDefinition = "JSON")
    private String sourceDistribution;

    @Column(name = "language_distribution", columnDefinition = "JSON")
    private String languageDistribution;

    @Column(name = "analysis_time", nullable = false)
    private LocalDateTime analysisTime;

    @Column(name = "analysis_duration")
    private Long analysisDuration;

    @Column(name = "preprocess_result", columnDefinition = "JSON")
    private String preprocessResult;

    @Column(name = "status", length = 20, nullable = false)
    private String status = "COMPLETED";

    @Column(name = "error_message", columnDefinition = "TEXT")
    private String errorMessage;

    @Column(name = "request_id", length = 64)
    private String requestId;
} 