package com.zanewu.yuqingplatform.client;

import com.zanewu.yuqingplatform.dto.SentimentAnalysisRequest;
import com.zanewu.yuqingplatform.dto.SentimentAnalysisResponse;
import com.zanewu.yuqingplatform.dto.StockAnalysisRequest;
import com.zanewu.yuqingplatform.dto.StockAnalysisResponse;
import com.zanewu.yuqingplatform.exception.BusinessException;
import lombok.extern.slf4j.Slf4j;
import com.zanewu.yuqingplatform.config.PythonServiceProperties;
import org.springframework.http.*;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

/**
 * Python服务调用客户端
 * @author zanewu
 */
@Slf4j
@Component
public class PythonServiceClient {

    private final RestTemplate restTemplate;
    private final PythonServiceProperties pythonServiceProperties;

    public PythonServiceClient(RestTemplate restTemplate, PythonServiceProperties pythonServiceProperties) {
        this.restTemplate = restTemplate;
        this.pythonServiceProperties = pythonServiceProperties;
    }

    /**
     * 调用Python股票分析服务
     */
    @Retryable(value = {RestClientException.class}, maxAttempts = 3, 
               backoff = @Backoff(delay = 1000, multiplier = 2))
    public StockAnalysisResponse analyzeStock(StockAnalysisRequest request) {
        log.info("调用Python股票分析服务，股票代码: {}, 分析类型: {}", 
                request.getStockCode(), request.getAnalysisType());
        
        try {
            String url = pythonServiceProperties.getApiUrl("/api/stock/analyze");
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("User-Agent", "YuQing-Platform/1.0");
            
            HttpEntity<StockAnalysisRequest> entity = new HttpEntity<>(request, headers);
            
            ResponseEntity<StockAnalysisResponse> response = restTemplate.exchange(
                url, HttpMethod.POST, entity, StockAnalysisResponse.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                log.info("股票分析完成，股票代码: {}", request.getStockCode());
                return response.getBody();
            } else {
                throw new BusinessException("Python服务返回异常状态: " + response.getStatusCode());
            }
            
        } catch (RestClientException e) {
            log.error("调用Python股票分析服务失败: {}", e.getMessage(), e);
            throw new BusinessException("股票分析服务暂时不可用，请稍后重试");
        }
    }

    /**
     * 调用Python舆情分析服务
     */
    @Retryable(value = {RestClientException.class}, maxAttempts = 3,
               backoff = @Backoff(delay = 1000, multiplier = 2))
    public SentimentAnalysisResponse analyzeSentiment(SentimentAnalysisRequest request) {
        log.info("调用Python舆情分析服务，分析类型: {}, 内容长度: {}", 
                request.getAnalysisType(), request.getContent().length());
        
        try {
            String url = pythonServiceProperties.getApiUrl("/api/sentiment/analyze");
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("User-Agent", "YuQing-Platform/1.0");
            
            HttpEntity<SentimentAnalysisRequest> entity = new HttpEntity<>(request, headers);
            
            ResponseEntity<SentimentAnalysisResponse> response = restTemplate.exchange(
                url, HttpMethod.POST, entity, SentimentAnalysisResponse.class
            );
            
            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                log.info("舆情分析完成，整体情感: {}", response.getBody().getOverallSentiment());
                return response.getBody();
            } else {
                throw new BusinessException("Python服务返回异常状态: " + response.getStatusCode());
            }
            
        } catch (RestClientException e) {
            log.error("调用Python舆情分析服务失败: {}", e.getMessage(), e);
            throw new BusinessException("舆情分析服务暂时不可用，请稍后重试");
        }
    }

    /**
     * 健康检查
     */
    public boolean checkHealth() {
        try {
            String url = pythonServiceProperties.getApiUrl("/health");
            ResponseEntity<Map> response = restTemplate.getForEntity(url, Map.class);
            return response.getStatusCode() == HttpStatus.OK;
        } catch (Exception e) {
            log.warn("Python服务健康检查失败: {}", e.getMessage());
            return false;
        }
    }

    /**
     * 获取服务状态信息
     */
    public Map<String, Object> getServiceStatus() {
        Map<String, Object> status = new HashMap<>();
        status.put("baseUrl", pythonServiceProperties.getBaseUrl());
        status.put("connectTimeout", pythonServiceProperties.getConnectTimeout());
        status.put("readTimeout", pythonServiceProperties.getReadTimeout());
        status.put("maxRetryAttempts", pythonServiceProperties.getRetry().getMaxAttempts());
        status.put("healthy", checkHealth());
        return status;
    }
} 