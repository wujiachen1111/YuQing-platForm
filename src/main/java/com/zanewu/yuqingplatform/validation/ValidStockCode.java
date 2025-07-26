package com.zanewu.yuqingplatform.validation;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;

import java.lang.annotation.*;

/**
 * 股票代码验证注解
 * @author zanewu
 */
@Target({ElementType.FIELD, ElementType.PARAMETER})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = StockCodeValidator.class)
@Documented
public @interface ValidStockCode {

    String message() default "股票代码格式不正确，应为6位数字";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
} 