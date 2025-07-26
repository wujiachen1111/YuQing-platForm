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
 * 舆情分析业务对象
 * @author zanewu
 */
@Data
@EqualsAndHashCode(callSuper = true)
public class SentimentAnalysisBO extends BaseBO {

    /**
     * 分析内容
     */
    private String content;

    /**
     * 内容长度
     */
    private Integer contentLength;

    /**
     * 分析类型
     */
    private String analysisType;

    /**
     * 数据源
     */
    private String source;

    /**
     * 语言
     */
    private String language;

    /**
     * 关键词列表
     */
    private List<String> keywords;

    /**
     * 开始日期
     */
    private LocalDate startDate;

    /**
     * 结束日期
     */
    private LocalDate endDate;

    /**
     * 整体情感倾向
     */
    private String overallSentiment;

    /**
     * 情感分数
     */
    private BigDecimal sentimentScore;

    /**
     * 置信度
     */
    private BigDecimal confidence;

    /**
     * 情感分布
     */
    private SentimentDistribution sentimentDistribution;

    /**
     * 关键词情感分析
     */
    private List<KeywordSentiment> keywordSentiments;

    /**
     * 热点话题
     */
    private List<HotTopic> hotTopics;

    /**
     * 情感趋势
     */
    private List<SentimentTrend> sentimentTrends;

    /**
     * 数据统计
     */
    private DataStatistics statistics;

    /**
     * 分析开始时间
     */
    private LocalDateTime analysisStartTime;

    /**
     * 分析结束时间
     */
    private LocalDateTime analysisEndTime;

    /**
     * 内容预处理结果
     */
    private ContentPreprocessResult preprocessResult;

    /**
     * 业务规则验证结果
     */
    private ValidationResult validationResult;

    @Data
    public static class SentimentDistribution {
        private BigDecimal positiveRate;
        private BigDecimal negativeRate;
        private BigDecimal neutralRate;
    }

    @Data
    public static class KeywordSentiment {
        private String keyword;
        private String sentiment;
        private BigDecimal score;
        private Integer mentionCount;
        private BigDecimal importance;
    }

    @Data
    public static class HotTopic {
        private String topic;
        private BigDecimal hotScore;
        private Integer contentCount;
        private String dominantSentiment;
        private List<String> relatedKeywords;
    }

    @Data
    public static class SentimentTrend {
        private LocalDateTime timestamp;
        private BigDecimal sentimentScore;
        private Integer contentCount;
        private String trendDirection;
    }

    @Data
    public static class DataStatistics {
        private Integer totalCount;
        private Integer validCount;
        private Integer filteredCount;
        private Map<String, Integer> sourceDistribution;
        private Map<String, Integer> languageDistribution;
    }

    @Data
    public static class ContentPreprocessResult {
        private String cleanedContent;
        private List<String> removedElements;
        private Integer originalLength;
        private Integer cleanedLength;
        private String preprocessStatus;
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
     * 判断是否为负面情感
     */
    public Boolean isNegative() {
        return "NEGATIVE".equals(overallSentiment);
    }

    /**
     * 获取内容压缩比
     */
    public BigDecimal getCompressionRatio() {
        if (preprocessResult != null && 
            preprocessResult.getOriginalLength() != null && 
            preprocessResult.getCleanedLength() != null &&
            preprocessResult.getOriginalLength() > 0) {
            return BigDecimal.valueOf(preprocessResult.getCleanedLength())
                    .divide(BigDecimal.valueOf(preprocessResult.getOriginalLength()), 4, BigDecimal.ROUND_HALF_UP);
        }
        return null;
    }
} 