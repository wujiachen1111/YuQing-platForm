package com.zanewu.yuqingplatform.vo;

import com.zanewu.yuqingplatform.common.BaseParam;
import com.zanewu.yuqingplatform.validation.ValidStockCode;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.time.LocalDate;
import java.util.Map;

/**
 * 股票分析请求VO
 * @author zanewu
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Schema(description = "股票分析请求")
public class StockAnalysisRequestVO extends BaseParam {

    @Schema(description = "股票代码", example = "000001")
    @NotBlank(message = "股票代码不能为空")
    @ValidStockCode
    private String stockCode;

    @Schema(description = "分析类型", example = "TECHNICAL", allowableValues = {"TECHNICAL", "FUNDAMENTAL", "TREND"})
    @NotBlank(message = "分析类型不能为空")
    private String analysisType;

    @Schema(description = "开始日期", example = "2024-01-01")
    private LocalDate startDate;

    @Schema(description = "结束日期", example = "2024-12-31")
    private LocalDate endDate;

    @Schema(description = "分析周期", example = "DAILY", allowableValues = {"DAILY", "WEEKLY", "MONTHLY"})
    private String period = "DAILY";

    @Schema(description = "扩展参数")
    private Map<String, Object> params;
} 