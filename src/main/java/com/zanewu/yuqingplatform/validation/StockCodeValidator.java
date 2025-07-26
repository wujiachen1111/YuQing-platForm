package com.zanewu.yuqingplatform.validation;

import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;
import org.springframework.util.StringUtils;

import java.util.regex.Pattern;

/**
 * 股票代码验证器
 * @author zanewu
 */
public class StockCodeValidator implements ConstraintValidator<ValidStockCode, String> {

    private static final Pattern STOCK_CODE_PATTERN = Pattern.compile("^[0-9]{6}$");

    @Override
    public void initialize(ValidStockCode constraintAnnotation) {
        // 初始化方法，可以获取注解参数
    }

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        // 允许为空，由@NotBlank等其他注解处理
        if (!StringUtils.hasText(value)) {
            return true;
        }
        
        return STOCK_CODE_PATTERN.matcher(value).matches();
    }
} 