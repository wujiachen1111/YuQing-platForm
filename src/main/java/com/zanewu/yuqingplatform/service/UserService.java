package com.zanewu.yuqingplatform.service;

import com.zanewu.yuqingplatform.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.Optional;

/**
 * 用户服务接口
 * @author zanewu
 */
public interface UserService {

    /**
     * 创建用户
     */
    User createUser(User user);

    /**
     * 根据ID获取用户
     */
    Optional<User> getUserById(Long id);

    /**
     * 根据用户名获取用户
     */
    Optional<User> getUserByUsername(String username);

    /**
     * 更新用户信息
     */
    User updateUser(Long id, User user);

    /**
     * 删除用户（逻辑删除）
     */
    void deleteUser(Long id);

    /**
     * 分页查询用户
     */
    Page<User> getUsers(String keyword, Pageable pageable);

    /**
     * 检查用户名是否存在
     */
    boolean existsByUsername(String username);

    /**
     * 检查邮箱是否存在
     */
    boolean existsByEmail(String email);
} 