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
 * 舆情分析响应VO
 * @author zanewu
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Schema(description = "舆情分析响应")
public class SentimentAnalysisResponseVO extends BaseVO {

    @Schema(description = "整体情感倾向", allowableValues = {"POSITIVE", "NEGATIVE", "NEUTRAL"})
    private String overallSentiment;

    @Schema(description = "情感分数", minimum = "-1", maximum = "1", example = "0.75")
    private BigDecimal sentimentScore;

    @Schema(description = "置信度", minimum = "0", maximum = "1", example = "0.85")
    private BigDecimal confidence;

    @Schema(description = "情感分布")
    private SentimentDistributionVO sentimentDistribution;

    @Schema(description = "关键词情感分析")
    private List<KeywordSentimentVO> keywordSentiments;

    @Schema(description = "热点话题")
    private List<HotTopicVO> hotTopics;

    @Schema(description = "情感趋势")
    private List<SentimentTrendVO> sentimentTrends;

    @Schema(description = "数据统计")
    private DataStatisticsVO statistics;

    @Schema(description = "分析时间")
    private LocalDateTime analysisTime;

    @Data
    @Schema(description = "情感分布")
    public static class SentimentDistributionVO {
        @Schema(description = "积极情感占比")
        private BigDecimal positiveRate;

        @Schema(description = "消极情感占比")
        private BigDecimal negativeRate;

        @Schema(description = "中性情感占比")
        private BigDecimal neutralRate;
    }

    @Data
    @Schema(description = "关键词情感")
    public static class KeywordSentimentVO {
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
    public static class HotTopicVO {
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
    public static class SentimentTrendVO {
        @Schema(description = "时间点")
        private LocalDateTime timestamp;

        @Schema(description = "情感分数")
        private BigDecimal sentimentScore;

        @Schema(description = "内容数量")
        private Integer contentCount;
    }

    @Data
    @Schema(description = "数据统计")
    public static class DataStatisticsVO {
        @Schema(description = "总内容数")
        private Integer totalCount;

        @Schema(description = "有效内容数")
        private Integer validCount;

        @Schema(description = "数据来源分布")
        private Map<String, Integer> sourceDistribution;
    }
} 