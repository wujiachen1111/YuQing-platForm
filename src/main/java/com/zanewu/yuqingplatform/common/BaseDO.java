package com.zanewu.yuqingplatform.common;

import lombok.Data;
import lombok.EqualsAndHashCode;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * DO基础类 - Data Object，用于数据层的实体对象
 * @author zanewu
 */
@Data
@EqualsAndHashCode(callSuper = true)
@MappedSuperclass
public abstract class BaseDO extends BaseEntity {

    @Column(name = "create_time", nullable = false, updatable = false)
    private LocalDateTime createTime;

    @Column(name = "update_time")
    private LocalDateTime updateTime;

    @Column(name = "create_by", length = 64)
    private String createBy;

    @Column(name = "update_by", length = 64)
    private String updateBy;

    @Column(name = "deleted", nullable = false)
    private Boolean deleted = false;

    @Version
    @Column(name = "version")
    private Long version = 0L;

    @PrePersist
    protected void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        if (createTime == null) {
            createTime = now;
        }
        if (updateTime == null) {
            updateTime = now;
        }
        if (deleted == null) {
            deleted = false;
        }
        if (version == null) {
            version = 0L;
        }
    }

    @PreUpdate
    protected void onUpdate() {
        updateTime = LocalDateTime.now();
    }
} 