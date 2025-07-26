package com.zanewu.yuqingplatform.config;

import org.springframework.context.annotation.Configuration;

/**
 * Swagger配置类
 * 使用springdoc-openapi，会自动配置OpenAPI文档
 * 访问地址：http://localhost:8888/api/swagger-ui.html
 * @author zanewu
 */
@Configuration
public class SwaggerConfig {
    
    // springdoc-openapi 会自动配置，无需额外配置
    // 如需自定义配置，可以添加 @Bean OpenAPI customOpenAPI() 方法
} 