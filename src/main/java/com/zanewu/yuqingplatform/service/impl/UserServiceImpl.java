package com.zanewu.yuqingplatform.service.impl;

import com.zanewu.yuqingplatform.entity.User;
import com.zanewu.yuqingplatform.exception.BusinessException;
import com.zanewu.yuqingplatform.repository.UserRepository;
import com.zanewu.yuqingplatform.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

/**
 * 用户服务实现类
 * @author zanewu
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    @Override
    @Transactional
    public User createUser(User user) {
        // 检查用户名是否已存在
        if (existsByUsername(user.getUsername())) {
            throw new BusinessException("用户名已存在");
        }
        
        // 检查邮箱是否已存在
        if (StringUtils.isNotBlank(user.getEmail()) && existsByEmail(user.getEmail())) {
            throw new BusinessException("邮箱已存在");
        }

        // 这里应该对密码进行加密，暂时简化处理
        log.info("创建用户: {}", user.getUsername());
        return userRepository.save(user);
    }

    @Override
    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id)
                .filter(user -> !user.getDeleted());
    }

    @Override
    public Optional<User> getUserByUsername(String username) {
        return userRepository.findByUsernameAndDeletedFalse(username);
    }

    @Override
    @Transactional
    public User updateUser(Long id, User user) {
        User existingUser = getUserById(id)
                .orElseThrow(() -> new BusinessException("用户不存在"));

        // 检查用户名是否被其他用户占用
        if (!existingUser.getUsername().equals(user.getUsername()) && 
            existsByUsername(user.getUsername())) {
            throw new BusinessException("用户名已存在");
        }

        // 检查邮箱是否被其他用户占用
        if (StringUtils.isNotBlank(user.getEmail()) && 
            !StringUtils.equals(existingUser.getEmail(), user.getEmail()) && 
            existsByEmail(user.getEmail())) {
            throw new BusinessException("邮箱已存在");
        }

        // 更新用户信息
        existingUser.setUsername(user.getUsername());
        existingUser.setEmail(user.getEmail());
        existingUser.setPhone(user.getPhone());
        existingUser.setNickname(user.getNickname());
        existingUser.setStatus(user.getStatus());

        // 如果提供了新密码，则更新密码
        if (StringUtils.isNotBlank(user.getPassword())) {
            existingUser.setPassword(user.getPassword());
        }

        log.info("更新用户: {}", existingUser.getUsername());
        return userRepository.save(existingUser);
    }

    @Override
    @Transactional
    public void deleteUser(Long id) {
        User user = getUserById(id)
                .orElseThrow(() -> new BusinessException("用户不存在"));
        
        // 逻辑删除
        user.setDeleted(true);
        userRepository.save(user);
        log.info("删除用户: {}", user.getUsername());
    }

    @Override
    public Page<User> getUsers(String keyword, Pageable pageable) {
        return userRepository.findByKeyword(keyword, pageable);
    }

    @Override
    public boolean existsByUsername(String username) {
        return userRepository.existsByUsernameAndDeletedFalse(username);
    }

    @Override
    public boolean existsByEmail(String email) {
        return StringUtils.isNotBlank(email) && 
               userRepository.existsByEmailAndDeletedFalse(email);
    }
} 