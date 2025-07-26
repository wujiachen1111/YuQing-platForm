package com.zanewu.yuqingplatform.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

/**
 * 舆情分析请求DTO
 * @author zanewu
 */
@Data
@Schema(description = "舆情分析请求")
public class SentimentAnalysisRequest {

    @Schema(description = "分析内容")
    @NotBlank(message = "分析内容不能为空")
    @Size(max = 10000, message = "分析内容不能超过10000字符")
    private String content;

    @Schema(description = "关键词列表")
    private List<String> keywords;

    @Schema(description = "数据源", example = "WEIBO", allowableValues = {"WEIBO", "NEWS", "FORUM", "WECHAT", "ALL"})
    private String source = "ALL";

    @Schema(description = "分析类型", example = "SENTIMENT", allowableValues = {"SENTIMENT", "EMOTION", "TOPIC", "TREND"})
    private String analysisType = "SENTIMENT";

    @Schema(description = "开始日期")
    private LocalDate startDate;

    @Schema(description = "结束日期")
    private LocalDate endDate;

    @Schema(description = "语言", example = "zh", allowableValues = {"zh", "en"})
    private String language = "zh";

    @Schema(description = "扩展参数")
    private Map<String, Object> params;
} 