package com.zanewu.yuqingplatform.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/**
 * 舆情分析响应DTO
 * @author zanewu
 */
@Data
@Schema(description = "舆情分析响应")
public class SentimentAnalysisResponse {

    @Schema(description = "整体情感倾向", allowableValues = {"POSITIVE", "NEGATIVE", "NEUTRAL"})
    private String overallSentiment;

    @Schema(description = "情感分数", minimum = "-1", maximum = "1", example = "0.75")
    private BigDecimal sentimentScore;

    @Schema(description = "置信度", minimum = "0", maximum = "1", example = "0.85")
    private BigDecimal confidence;

    @Schema(description = "情感分布")
    private SentimentDistribution sentimentDistribution;

    @Schema(description = "关键词情感分析")
    private List<KeywordSentiment> keywordSentiments;

    @Schema(description = "热点话题")
    private List<HotTopic> hotTopics;

    @Schema(description = "情感趋势")
    private List<SentimentTrend> sentimentTrends;

    @Schema(description = "数据统计")
    private DataStatistics statistics;

    @Schema(description = "分析时间")
    private LocalDateTime analysisTime;

    @Data
    @Schema(description = "情感分布")
    public static class SentimentDistribution {
        @Schema(description = "积极情感占比")
        private BigDecimal positiveRate;

        @Schema(description = "消极情感占比")
        private BigDecimal negativeRate;

        @Schema(description = "中性情感占比")
        private BigDecimal neutralRate;
    }

    @Data
    @Schema(description = "关键词情感")
    public static class KeywordSentiment {
        @Schema(description = "关键词")
        private String keyword;

        @Schema(description = "情感倾向")
        private String sentiment;

        @Schema(description = "情感分数")
        private BigDecimal score;

        @Schema(description = "提及次数")
        private Integer mentionCount;
    }

    @Data
    @Schema(description = "热点话题")
    public static class HotTopic {
        @Schema(description = "话题名称")
        private String topic;

        @Schema(description = "热度分数")
        private BigDecimal hotScore;

        @Schema(description = "相关内容数量")
        private Integer contentCount;

        @Schema(description = "主要情感")
        private String dominantSentiment;
    }

    @Data
    @Schema(description = "情感趋势")
    public static class SentimentTrend {
        @Schema(description = "时间点")
        private LocalDateTime timestamp;

        @Schema(description = "情感分数")
        private BigDecimal sentimentScore;

        @Schema(description = "内容数量")
        private Integer contentCount;
    }

    @Data
    @Schema(description = "数据统计")
    public static class DataStatistics {
        @Schema(description = "总内容数")
        private Integer totalCount;

        @Schema(description = "有效内容数")
        private Integer validCount;

        @Schema(description = "数据来源分布")
        private Map<String, Integer> sourceDistribution;
    }
} 