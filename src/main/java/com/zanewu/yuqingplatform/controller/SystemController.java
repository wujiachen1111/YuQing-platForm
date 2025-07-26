package com.zanewu.yuqingplatform.controller;

import com.zanewu.yuqingplatform.common.Result;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * 系统控制器
 * @author zanewu
 */
@Slf4j
@RestController
@RequestMapping("/system")
@Tag(name = "系统管理", description = "系统状态和监控相关接口")
public class SystemController {

    @Value("${spring.application.name:YuQing-Platform}")
    private String applicationName;

    @Value("${server.port:8888}")
    private String serverPort;

    @Operation(summary = "系统信息", description = "获取系统基本信息")
    @GetMapping("/info")
    public Result<Map<String, Object>> getSystemInfo() {
        Map<String, Object> info = new HashMap<>();
        info.put("applicationName", applicationName);
        info.put("version", "1.0.0");
        info.put("serverPort", serverPort);
        info.put("currentTime", LocalDateTime.now());
        info.put("javaVersion", System.getProperty("java.version"));
        info.put("osName", System.getProperty("os.name"));
        
        return Result.success("获取系统信息成功", info);
    }

    @Operation(summary = "健康检查", description = "系统健康检查接口")
    @GetMapping("/health")
    public Result<Map<String, Object>> health() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("timestamp", LocalDateTime.now());
        
        // 检查内存使用情况
        Runtime runtime = Runtime.getRuntime();
        long maxMemory = runtime.maxMemory();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;
        
        Map<String, Object> memory = new HashMap<>();
        memory.put("max", maxMemory / 1024 / 1024 + " MB");
        memory.put("total", totalMemory / 1024 / 1024 + " MB");
        memory.put("used", usedMemory / 1024 / 1024 + " MB");
        memory.put("free", freeMemory / 1024 / 1024 + " MB");
        
        health.put("memory", memory);
        
        return Result.success("系统运行正常", health);
    }

    @Operation(summary = "版本信息", description = "获取应用版本信息")
    @GetMapping("/version")
    public Result<Map<String, String>> getVersion() {
        Map<String, String> version = new HashMap<>();
        version.put("application", applicationName);
        version.put("version", "1.0.0");
        version.put("buildTime", "2024-01-01");
        version.put("description", "舆情分析平台后端服务");
        
        return Result.success("获取版本信息成功", version);
    }
} 