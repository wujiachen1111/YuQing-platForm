package com.zanewu.yuqingplatform.repository;

import com.zanewu.yuqingplatform.entity.SentimentAnalysisRecordDO;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

/**
 * 舆情分析记录Repository
 * @author zanewu
 */
@Repository
public interface SentimentAnalysisRecordRepository extends JpaRepository<SentimentAnalysisRecordDO, Long> {

    /**
     * 分页查询舆情分析记录
     */
    Page<SentimentAnalysisRecordDO> findByDeletedFalseOrderByAnalysisTimeDesc(Pageable pageable);

    /**
     * 根据内容哈希查询（去重）
     */
    Optional<SentimentAnalysisRecordDO> findByContentHashAndDeletedFalse(String contentHash);

    /**
     * 根据分析时间范围查询
     */
    @Query("SELECT s FROM SentimentAnalysisRecordDO s WHERE s.analysisTime BETWEEN :startTime AND :endTime " +
           "AND s.deleted = false ORDER BY s.analysisTime DESC")
    List<SentimentAnalysisRecordDO> findByAnalysisTimeBetween(
            @Param("startTime") LocalDateTime startTime, 
            @Param("endTime") LocalDateTime endTime);

    /**
     * 根据情感倾向统计
     */
    @Query("SELECT s.overallSentiment, COUNT(s) FROM SentimentAnalysisRecordDO s " +
           "WHERE s.analysisTime >= :startTime AND s.deleted = false " +
           "GROUP BY s.overallSentiment")
    List<Object[]> countBySentimentAfter(@Param("startTime") LocalDateTime startTime);

    /**
     * 查询负面情感记录
     */
    @Query("SELECT s FROM SentimentAnalysisRecordDO s WHERE s.overallSentiment = 'NEGATIVE' " +
           "AND s.analysisTime >= :startTime AND s.deleted = false " +
           "ORDER BY s.sentimentScore ASC")
    List<SentimentAnalysisRecordDO> findNegativeSentiments(@Param("startTime") LocalDateTime startTime);

    /**
     * 根据数据源查询
     */
    List<SentimentAnalysisRecordDO> findBySourceAndDeletedFalseOrderByAnalysisTimeDesc(String source);

    /**
     * 根据分析类型查询
     */
    List<SentimentAnalysisRecordDO> findByAnalysisTypeAndDeletedFalseOrderByAnalysisTimeDesc(String analysisType);

    /**
     * 根据请求ID查询
     */
    Optional<SentimentAnalysisRecordDO> findByRequestIdAndDeletedFalse(String requestId);

    /**
     * 统计平均情感分数
     */
    @Query("SELECT AVG(s.sentimentScore) FROM SentimentAnalysisRecordDO s " +
           "WHERE s.analysisTime >= :startTime AND s.deleted = false")
    Double getAverageSentimentScore(@Param("startTime") LocalDateTime startTime);

    /**
     * 查询热门关键词（需要解析JSON）
     */
    @Query(value = "SELECT COUNT(*) FROM sentiment_analysis_record " +
                   "WHERE JSON_CONTAINS(keywords, JSON_QUOTE(:keyword)) " +
                   "AND analysis_time >= :startTime AND deleted = false", 
           nativeQuery = true)
    Long countByKeyword(@Param("keyword") String keyword, 
                       @Param("startTime") LocalDateTime startTime);
} 