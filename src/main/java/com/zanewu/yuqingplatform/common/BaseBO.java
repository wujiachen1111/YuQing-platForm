package com.zanewu.yuqingplatform.common;

import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * BO基础类 - Business Object，用于业务层的数据处理
 * @author zanewu
 */
@Data
public abstract class BaseBO implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * 业务处理时间
     */
    private LocalDateTime processTime = LocalDateTime.now();

    /**
     * 业务处理人员
     */
    private String processor;

    /**
     * 业务处理状态
     */
    private String processStatus;

    /**
     * 业务处理备注
     */
    private String processRemark;

    /**
     * 扩展字段，用于存储业务相关的额外信息
     */
    private Object extendData;
} 