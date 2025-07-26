package com.zanewu.yuqingplatform.config;

import org.apache.hc.client5.http.config.RequestConfig;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.client5.http.impl.io.PoolingHttpClientConnectionManager;
import org.apache.hc.core5.util.Timeout;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.retry.annotation.EnableRetry;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Web配置类
 * @author zanewu
 */
@Configuration
@EnableRetry
@EnableConfigurationProperties(PythonServiceProperties.class)
public class WebConfig implements WebMvcConfigurer {

    private final PythonServiceProperties pythonServiceProperties;

    public WebConfig(PythonServiceProperties pythonServiceProperties) {
        this.pythonServiceProperties = pythonServiceProperties;
    }

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOriginPatterns("*")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true)
                .maxAge(3600);
    }

    /**
     * 配置RestTemplate用于调用Python服务
     */
    @Bean
    public RestTemplate restTemplate() {
        // 配置连接池
        PoolingHttpClientConnectionManager connectionManager = new PoolingHttpClientConnectionManager();
        connectionManager.setMaxTotal(pythonServiceProperties.getConnectionPool().getMaxTotal());
        connectionManager.setDefaultMaxPerRoute(pythonServiceProperties.getConnectionPool().getDefaultMaxPerRoute());

        // 配置请求超时
        RequestConfig requestConfig = RequestConfig.custom()
                .setConnectionRequestTimeout(Timeout.ofMilliseconds(pythonServiceProperties.getConnectTimeout()))
                .setResponseTimeout(Timeout.ofMilliseconds(pythonServiceProperties.getReadTimeout()))
                .build();

        // 创建HttpClient
        CloseableHttpClient httpClient = HttpClients.custom()
                .setConnectionManager(connectionManager)
                .setDefaultRequestConfig(requestConfig)
                .build();

        // 创建请求工厂
        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory(httpClient);
        
        return new RestTemplate(factory);
    }
} 