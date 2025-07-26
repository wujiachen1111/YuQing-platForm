package com.zanewu.yuqingplatform.repository;

import com.zanewu.yuqingplatform.entity.StockAnalysisRecordDO;
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
 * 股票分析记录Repository
 * @author zanewu
 */
@Repository
public interface StockAnalysisRecordRepository extends JpaRepository<StockAnalysisRecordDO, Long> {

    /**
     * 根据股票代码查询分析记录
     */
    List<StockAnalysisRecordDO> findByStockCodeAndDeletedFalseOrderByAnalysisTimeDesc(String stockCode);

    /**
     * 根据股票代码和分析类型查询最新记录
     */
    Optional<StockAnalysisRecordDO> findFirstByStockCodeAndAnalysisTypeAndDeletedFalseOrderByAnalysisTimeDesc(
            String stockCode, String analysisType);

    /**
     * 分页查询股票分析记录
     */
    Page<StockAnalysisRecordDO> findByDeletedFalseOrderByAnalysisTimeDesc(Pageable pageable);

    /**
     * 根据分析时间范围查询
     */
    @Query("SELECT s FROM StockAnalysisRecordDO s WHERE s.analysisTime BETWEEN :startTime AND :endTime " +
           "AND s.deleted = false ORDER BY s.analysisTime DESC")
    List<StockAnalysisRecordDO> findByAnalysisTimeBetween(
            @Param("startTime") LocalDateTime startTime, 
            @Param("endTime") LocalDateTime endTime);

    /**
     * 根据推荐操作统计
     */
    @Query("SELECT s.recommendation, COUNT(s) FROM StockAnalysisRecordDO s " +
           "WHERE s.analysisTime >= :startTime AND s.deleted = false " +
           "GROUP BY s.recommendation")
    List<Object[]> countByRecommendationAfter(@Param("startTime") LocalDateTime startTime);

    /**
     * 查询高风险股票
     */
    @Query("SELECT s FROM StockAnalysisRecordDO s WHERE s.riskLevel = 'HIGH' " +
           "AND s.analysisTime >= :startTime AND s.deleted = false " +
           "ORDER BY s.riskScore DESC")
    List<StockAnalysisRecordDO> findHighRiskStocks(@Param("startTime") LocalDateTime startTime);

    /**
     * 根据请求ID查询
     */
    Optional<StockAnalysisRecordDO> findByRequestIdAndDeletedFalse(String requestId);

    /**
     * 统计分析次数
     */
    @Query("SELECT COUNT(s) FROM StockAnalysisRecordDO s WHERE s.stockCode = :stockCode " +
           "AND s.analysisTime >= :startTime AND s.deleted = false")
    Long countAnalysisByStockCode(@Param("stockCode") String stockCode, 
                                  @Param("startTime") LocalDateTime startTime);
} 