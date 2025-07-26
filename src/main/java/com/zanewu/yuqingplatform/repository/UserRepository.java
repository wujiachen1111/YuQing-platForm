package com.zanewu.yuqingplatform.repository;

import com.zanewu.yuqingplatform.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * 用户数据访问层
 * @author zanewu
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * 根据用户名查找用户
     */
    Optional<User> findByUsernameAndDeletedFalse(String username);

    /**
     * 根据邮箱查找用户
     */
    Optional<User> findByEmailAndDeletedFalse(String email);

    /**
     * 检查用户名是否存在
     */
    boolean existsByUsernameAndDeletedFalse(String username);

    /**
     * 检查邮箱是否存在
     */
    boolean existsByEmailAndDeletedFalse(String email);

    /**
     * 分页查询未删除的用户
     */
    @Query("SELECT u FROM User u WHERE u.deleted = false AND " +
           "(:keyword IS NULL OR u.username LIKE %:keyword% OR u.nickname LIKE %:keyword% OR u.email LIKE %:keyword%)")
    Page<User> findByKeyword(@Param("keyword") String keyword, Pageable pageable);
} 