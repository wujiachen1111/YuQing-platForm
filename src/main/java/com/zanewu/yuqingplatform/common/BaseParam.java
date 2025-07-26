package com.zanewu.yuqingplatform.common;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 参数基础类
 * @author zanewu
 */
@Data
@Schema(description = "基础参数类")
public abstract class BaseParam implements Serializable {

    private static final long serialVersionUID = 1L;

    @Schema(description = "页码", example = "1")
    @Min(value = 1, message = "页码不能小于1")
    private Integer pageNum = 1;

    @Schema(description = "每页大小", example = "10")
    @Min(value = 1, message = "每页大小不能小于1")
    @Max(value = 100, message = "每页大小不能超过100")
    private Integer pageSize = 10;

    @Schema(description = "排序字段", example = "createTime")
    private String orderBy;

    @Schema(description = "排序方向", example = "DESC", allowableValues = {"ASC", "DESC"})
    private String orderDirection = "DESC";

    @Schema(description = "请求时间戳")
    private LocalDateTime requestTime = LocalDateTime.now();

    @Schema(description = "请求ID，用于链路追踪")
    private String requestId;

    /**
     * 获取偏移量
     */
    public int getOffset() {
        return (pageNum - 1) * pageSize;
    }

    /**
     * 是否升序排序
     */
    public boolean isAscending() {
        return "ASC".equalsIgnoreCase(orderDirection);
    }
} 