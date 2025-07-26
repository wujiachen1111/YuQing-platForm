package com.zanewu.yuqingplatform.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.Duration;

/**
 * Python服务配置属性
 * @author zanewu
 */
@Data
@Validated
@ConfigurationProperties(prefix = "python.service")
public class PythonServiceProperties {

    /**
     * Python服务基础URL
     */
    @NotBlank(message = "Python服务基础URL不能为空")
    private String baseUrl = "http://localhost:5000";

    /**
     * 连接超时时间（毫秒）
     */
    @Min(value = 1000, message = "连接超时时间不能小于1秒")
    private long connectTimeout = 30000;

    /**
     * 读取超时时间（毫秒）
     */
    @Min(value = 1000, message = "读取超时时间不能小于1秒")
    private long readTimeout = 60000;

    /**
     * 重试配置
     */
    @NotNull
    private Retry retry = new Retry();

    /**
     * 连接池配置
     */
    @NotNull
    private ConnectionPool connectionPool = new ConnectionPool();

    /**
     * 重试配置
     */
    @Data
    public static class Retry {
        /**
         * 最大重试次数
         */
        @Min(value = 1, message = "最大重试次数不能小于1")
        private int maxAttempts = 3;

        /**
         * 重试延迟（毫秒）
         */
        @Min(value = 100, message = "重试延迟不能小于100毫秒")
        private long delay = 1000;

        /**
         * 重试延迟倍数
         */
        @Min(value = 1, message = "重试延迟倍数不能小于1")
        private double multiplier = 2.0;

        /**
         * 最大重试延迟（毫秒）
         */
        @Min(value = 1000, message = "最大重试延迟不能小于1秒")
        private long maxDelay = 30000;
    }

    /**
     * 连接池配置
     */
    @Data
    public static class ConnectionPool {
        /**
         * 最大连接数
         */
        @Min(value = 10, message = "最大连接数不能小于10")
        private int maxTotal = 200;

        /**
         * 每个路由的最大连接数
         */
        @Min(value = 5, message = "每个路由的最大连接数不能小于5")
        private int defaultMaxPerRoute = 20;

        /**
         * 连接存活时间
         */
        private Duration timeToLive = Duration.ofMinutes(30);

        /**
         * 连接空闲超时时间
         */
        private Duration connectionIdleTimeout = Duration.ofMinutes(5);
    }

    /**
     * 获取完整的API URL
     */
    public String getApiUrl(String path) {
        return baseUrl + (path.startsWith("/") ? path : "/" + path);
    }
} 