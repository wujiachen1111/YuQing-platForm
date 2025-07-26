package com.zanewu.yuqingplatform.common;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * VO基础类 - View Object，用于接口层的数据传输
 * @author zanewu
 */
@Data
@Schema(description = "VO基础类")
public abstract class BaseVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @Schema(description = "响应时间戳")
    private LocalDateTime responseTime = LocalDateTime.now();

    @Schema(description = "请求ID，用于链路追踪")
    private String requestId;

    @Schema(description = "数据版本号，用于乐观锁")
    private Long version;
} 