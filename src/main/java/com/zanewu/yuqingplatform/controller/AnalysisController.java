package com.zanewu.yuqingplatform.controller;

import com.zanewu.yuqingplatform.common.Result;
import com.zanewu.yuqingplatform.vo.SentimentAnalysisRequestVO;
import com.zanewu.yuqingplatform.vo.SentimentAnalysisResponseVO;
import com.zanewu.yuqingplatform.vo.StockAnalysisRequestVO;
import com.zanewu.yuqingplatform.vo.StockAnalysisResponseVO;
import com.zanewu.yuqingplatform.service.AnalysisService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;

import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 分析控制器
 * @author zanewu
 */
@Slf4j
@RestController
@RequestMapping("/analysis")
@Tag(name = "分析服务", description = "股票分析和舆情分析相关接口")
public class AnalysisController {

    private final AnalysisService analysisService;

    public AnalysisController(AnalysisService analysisService) {
        this.analysisService = analysisService;
    }

    @Operation(summary = "股票分析", description = "对指定股票进行技术分析、基本面分析或趋势分析")
    @PostMapping("/stock")
    public Result<StockAnalysisResponseVO> analyzeStock(
            @Parameter(description = "股票分析请求参数") 
            @Valid @RequestBody StockAnalysisRequestVO request) {
        
        log.info("收到股票分析请求，股票代码: {}, 分析类型: {}", 
                request.getStockCode(), request.getAnalysisType());
        
        StockAnalysisResponseVO response = analysisService.analyzeStock(request);
        return Result.success("股票分析完成", response);
    }

    @Operation(summary = "舆情分析", description = "对文本内容进行情感分析、情绪分析或话题分析")
    @PostMapping("/sentiment")
    public Result<SentimentAnalysisResponseVO> analyzeSentiment(
            @Parameter(description = "舆情分析请求参数")
            @Valid @RequestBody SentimentAnalysisRequestVO request) {
        
        log.info("收到舆情分析请求，分析类型: {}, 内容长度: {}", 
                request.getAnalysisType(), request.getContent().length());
        
        SentimentAnalysisResponseVO response = analysisService.analyzeSentiment(request);
        return Result.success("舆情分析完成", response);
    }

    @Operation(summary = "获取Python服务状态", description = "获取Python分析服务的运行状态和配置信息")
    @GetMapping("/service/status")
    public Result<Map<String, Object>> getServiceStatus() {
        log.info("获取Python服务状态");
        Map<String, Object> status = analysisService.getPythonServiceStatus();
        return Result.success("获取服务状态成功", status);
    }

    @Operation(summary = "健康检查", description = "检查Python分析服务是否正常运行")
    @GetMapping("/service/health")
    public Result<Boolean> checkHealth() {
        log.info("检查Python服务健康状态");
        boolean healthy = analysisService.checkPythonServiceHealth();
        
        if (healthy) {
            return Result.success("Python服务运行正常", true);
        } else {
            return Result.error("Python服务不可用");
        }
    }

    @Operation(summary = "快速股票分析", description = "根据股票代码进行快速技术分析")
    @GetMapping("/stock/{stockCode}/quick")
    public Result<StockAnalysisResponseVO> quickStockAnalysis(
            @Parameter(description = "股票代码", example = "000001")
            @PathVariable String stockCode) {
        
        log.info("收到快速股票分析请求，股票代码: {}", stockCode);
        
        // 构建默认请求
        StockAnalysisRequestVO request = new StockAnalysisRequestVO();
        request.setStockCode(stockCode);
        request.setAnalysisType("TECHNICAL");
        request.setPeriod("DAILY");
        
        StockAnalysisResponseVO response = analysisService.analyzeStock(request);
        return Result.success("快速股票分析完成", response);
    }

    @Operation(summary = "批量股票分析", description = "对多个股票进行批量分析")
    @PostMapping("/stock/batch")
    public Result<Map<String, StockAnalysisResponseVO>> batchStockAnalysis(
            @Parameter(description = "股票代码列表")
            @RequestBody String[] stockCodes) {
        
        log.info("收到批量股票分析请求，股票数量: {}", stockCodes.length);
        
        // 这里可以实现批量分析逻辑
        // 为了简化，暂时返回提示信息
        return Result.error("批量分析功能开发中，请使用单个股票分析接口");
    }
} 