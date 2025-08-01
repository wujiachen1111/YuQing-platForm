from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import pymysql
import requests
import asyncio
import logging
import traceback
import sys
import json
import re
from datetime import datetime
import random
from typing import List, Dict, Any
from pydantic import BaseModel
import uvicorn

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置为DEBUG级别以获取更多信息

# 创建格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 文件处理器
file_handler = logging.FileHandler("stock_api.log", encoding='utf-8')
file_handler.setFormatter(formatter)

# 添加处理器
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# ---------- 全局设置 ----------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://finance.sina.com.cn/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
}

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'QTSqts1030+',
    'database': 'stock_db',
    'charset': 'utf8mb4',
    'connect_timeout': 10
}

# 创建FastAPI应用
app = FastAPI(title="股票数据API", version="1.0.0")

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 任务队列
task_queue = asyncio.Queue()

# ---------- 数据库操作 ----------
def create_tables():
    """创建数据库表（如果不存在）"""
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # 创建基本信息表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stock_code VARCHAR(10) NOT NULL,
                stock_name VARCHAR(50) NOT NULL,
                latest_price DECIMAL(10,2) NOT NULL,
                pe_ttm VARCHAR(20),
                pb VARCHAR(20),
                turnover_rate DECIMAL(10,4) NOT NULL,
                heat BIGINT NOT NULL,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY (stock_code)
            )
            """)
            
            # 创建股东信息表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_holders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stock_code VARCHAR(10) NOT NULL,
                holder_name VARCHAR(100) NOT NULL,
                shares BIGINT NOT NULL,
                ratio DECIMAL(10,4) NOT NULL,
                report_date CHAR(8) NOT NULL,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX (stock_code)
            )
            """)
            
            # 创建日K线表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_kline_day (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stock_code VARCHAR(10) NOT NULL,
                date DATE NOT NULL,
                open DECIMAL(10,2) NOT NULL,
                high DECIMAL(10,2) NOT NULL,
                low DECIMAL(10,2) NOT NULL,
                close DECIMAL(10,2) NOT NULL,
                price_change DECIMAL(10,2) NOT NULL,
                change_pct DECIMAL(10,2) NOT NULL,
                volume DECIMAL(15,2) NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY (stock_code, date)
            )
            """)
            
            # 创建月K线表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_kline_month (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stock_code VARCHAR(10) NOT NULL,
                date DATE NOT NULL,
                open DECIMAL(10,2) NOT NULL,
                high DECIMAL(10,2) NOT NULL,
                low DECIMAL(10,2) NOT NULL,
                close DECIMAL(10,2) NOT NULL,
                price_change DECIMAL(10,2) NOT NULL,
                change_pct DECIMAL(10,2) NOT NULL,
                volume DECIMAL(15,2) NOT NULL,
                amount DECIMAL(15,2) NOT NULL,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY (stock_code, date)
            )
            """)
            
            conn.commit()
            logger.info("数据库表创建/验证完成 [OK]")
    except pymysql.MySQLError as e:
        logger.error(f"数据库连接失败 [ERROR]: {e}")
        logger.error(traceback.format_exc())
    except Exception as e:
        logger.error(f"数据库表创建失败 [ERROR]: {e}")
        logger.error(traceback.format_exc())
    finally:
        if conn:
            conn.close()

# ---------- 股票数据处理类 ----------
class StockProcessor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.mount("https://", requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=100))
    
    def get_stock_basic_info(self, stock_code: str):
        """获取股票基本信息"""
        try:
            # 使用更稳定的腾讯财经接口
            market = "sz" if stock_code.startswith(("0", "3")) else "sh"
            symbol = f"{market}{stock_code}"
            url = f"https://qt.gtimg.cn/q={symbol}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # 解析数据: v_sz000651="1~格力电器~000651~34.40~34.30~34.20~...~12345678~..."
            data_str = response.text
            if '="' not in data_str:
                logger.error(f"腾讯接口返回数据格式异常: {data_str}")
                return None
                
            data = data_str.split('="')[1].strip('";').split('~')
            
            if len(data) < 40:
                logger.error(f"腾讯接口返回数据不足: {data}")
                return None
            
            return {
                "stock_name": data[1],
                "latest_price": float(data[3]),
                "pe_ttm": data[39] if len(data) > 39 else "N/A",
                "pb": data[46] if len(data) > 46 else "N/A",
                "turnover_rate": float(data[37]) if len(data) > 37 else 0,
                "heat": data[36]  # 总手作为热度
            }
        except Exception as e:
            logger.error(f"获取股票基本信息异常 [ERROR]: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def get_kline_data(self, stock_code: str, period: str, count: int):
        """
        获取K线数据（使用腾讯接口）
        :param stock_code: 股票代码
        :param period: 周期 ('day' 或 'month')
        :param count: 需要的数据条数
        """
        try:
            market = "sz" if stock_code.startswith(("0", "3")) else "sh"
            symbol = f"{market}{stock_code}"
            
            # 使用您之前成功的接口URL格式
            url = (
                "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
                f"?param={symbol},{period},,,1000,qfq"  # 固定请求1000条数据
            )
            
            logger.info(f"请求K线数据: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # 解析腾讯接口返回的数据 - 按照您之前成功的代码
            raw_list = (
                data.get("data", {})
                .get(symbol, {})
                .get("qfq" + period, []) or data["data"][symbol][period]
            )
            
            # 只取最近count条数据
            klines = []
            for item in raw_list[-count:]:
                if len(item) < 6:
                    continue
                date, open_, close, high, low, volume = item[:6]
                try:
                    open_, close, high, low, volume = map(float, (open_, close, high, low, volume))
                    
                    # 计算成交额（估算）
                    amount = (open_ + close) / 2 * volume
                    
                    klines.append({
                        "date": date,
                        "open": open_,
                        "high": high,
                        "low": low,
                        "close": close,
                        "volume": volume / 1e4,  # 转换为万手
                        "amount": amount / 1e8,  # 转换为亿元
                    })
                except ValueError as e:
                    logger.warning(f"K线数据转换失败: {e} in {item}")
                    continue
            
            # 计算涨跌幅 - 按照您之前成功的代码
            for i in range(1, len(klines)):
                prev = klines[i - 1]["close"]
                curr = klines[i]["close"]
                klines[i]["change"] = round(curr - prev, 2)
                klines[i]["change_pct"] = round((curr - prev) / prev * 100, 2)
            
            if klines:
                klines[0]["change"] = klines[0]["change_pct"] = 0
            
            logger.info(f"获取到 {len(klines)} 条{period}K线数据")
            return klines
        except Exception as e:
            logger.error(f"获取K线数据异常 [ERROR]: {e}")
            logger.error(traceback.format_exc())
            return []
    
    def save_to_database(self, stock_code, basic_info, day_kline, month_kline):
        """保存数据到数据库"""
        conn = None
        try:
            conn = pymysql.connect(**DB_CONFIG)
            with conn.cursor() as cursor:
                # 保存基本信息
                if basic_info:
                    cursor.execute("""
                    INSERT INTO stock_info (stock_code, stock_name, latest_price, pe_ttm, pb, turnover_rate, heat)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        stock_name = VALUES(stock_name),
                        latest_price = VALUES(latest_price),
                        pe_ttm = VALUES(pe_ttm),
                        pb = VALUES(pb),
                        turnover_rate = VALUES(turnover_rate),
                        heat = VALUES(heat)
                    """, (
                        stock_code,
                        basic_info["stock_name"],
                        basic_info["latest_price"],
                        basic_info["pe_ttm"],
                        basic_info["pb"],
                        basic_info["turnover_rate"],
                        basic_info["heat"]
                    ))
                    logger.info(f"股票 {stock_code} 基本信息保存成功")
                
                # 保存日K线数据
                for k in day_kline:
                    try:
                        # 确保日期格式正确
                        date_obj = datetime.strptime(k["date"], "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%Y-%m-%d")
                    except (ValueError, TypeError):
                        formatted_date = k["date"]
                    
                    cursor.execute("""
                    INSERT INTO stock_kline_day (stock_code, date, open, high, low, close, price_change, change_pct, volume, amount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        open = VALUES(open),
                        high = VALUES(high),
                        low = VALUES(low),
                        close = VALUES(close),
                        price_change = VALUES(price_change),
                        change_pct = VALUES(change_pct),
                        volume = VALUES(volume),
                        amount = VALUES(amount)
                    """, (
                        stock_code,
                        formatted_date,
                        k["open"],
                        k["high"],
                        k["low"],
                        k["close"],
                        k.get("change", 0),
                        k.get("change_pct", 0),
                        k["volume"],
                        k["amount"]
                    ))
                
                # 保存月K线数据
                for k in month_kline:
                    try:
                        # 确保日期格式正确
                        date_obj = datetime.strptime(k["date"], "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%Y-%m-%d")
                    except (ValueError, TypeError):
                        formatted_date = k["date"]
                    
                    cursor.execute("""
                    INSERT INTO stock_kline_month (stock_code, date, open, high, low, close, price_change, change_pct, volume, amount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        open = VALUES(open),
                        high = VALUES(high),
                        low = VALUES(low),
                        close = VALUES(close),
                        price_change = VALUES(price_change),
                        change_pct = VALUES(change_pct),
                        volume = VALUES(volume),
                        amount = VALUES(amount)
                    """, (
                        stock_code,
                        formatted_date,
                        k["open"],
                        k["high"],
                        k["low"],
                        k["close"],
                        k.get("change", 0),
                        k.get("change_pct", 0),
                        k["volume"],
                        k["amount"]
                    ))
                
                conn.commit()
                logger.info(f"股票 {stock_code} K线数据保存成功")
                return True
        except pymysql.MySQLError as e:
            logger.error(f"数据库错误 [ERROR]: {e}")
            if conn:
                conn.rollback()
            return False
        except Exception as e:
            logger.error(f"保存失败 [ERROR]: {e}")
            logger.error(traceback.format_exc())
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

# ---------- Pydantic模型 ----------
class BatchStockRequest(BaseModel):
    stock_codes: List[str]

class StockResponse(BaseModel):
    status: str
    message: str
    stock_code: str
    basic_info: Dict[str, Any] = None
    day_kline_count: int = 0
    month_kline_count: int = 0

class QueueStatusResponse(BaseModel):
    status: str
    queue_size: int

# ---------- API 接口 ----------
@app.get("/api/stock/{stock_code}", response_model=StockResponse)
async def get_stock_data(stock_code: str):
    """获取单个股票数据并保存到数据库"""
    try:
        processor = StockProcessor()
        
        # 获取基本信息
        basic_info = processor.get_stock_basic_info(stock_code)
        if not basic_info:
            return {
                "status": "error",
                "message": "获取基本信息失败",
                "stock_code": stock_code
            }
        
        # 获取K线数据
        day_kline = processor.get_kline_data(stock_code, "day", 22)
        month_kline = processor.get_kline_data(stock_code, "month", 24)
        
        # 保存到数据库
        if processor.save_to_database(stock_code, basic_info, day_kline, month_kline):
            return {
                "status": "success",
                "message": "数据已保存",
                "stock_code": stock_code,
                "basic_info": basic_info,
                "day_kline_count": len(day_kline),
                "month_kline_count": len(month_kline)
            }
        else:
            return {
                "status": "error",
                "message": "数据保存失败",
                "stock_code": stock_code
            }
    except Exception as e:
        logger.error(f"处理股票 {stock_code} 失败 [ERROR]: {e}")
        logger.error(traceback.format_exc())
        return {
            "status": "error",
            "message": str(e),
            "stock_code": stock_code
        }

@app.post("/api/stocks/batch", response_model=dict)
async def batch_process_stocks(request: BatchStockRequest, background_tasks: BackgroundTasks):
    """批量处理股票数据（异步）"""
    stock_codes = request.stock_codes
    
    if not stock_codes:
        return {"status": "error", "message": "未提供股票代码"}
    
    # 添加到任务队列
    added_count = 0
    for code in stock_codes:
        if isinstance(code, str) and code.strip():
            # 使用后台任务处理
            background_tasks.add_task(process_stock_task, code.strip())
            added_count += 1
    
    logger.info(f"已添加 {added_count} 个股票到后台任务")
    return {
        "status": "success",
        "message": "任务已添加到后台处理",
        "task_count": added_count
    }

@app.get("/api/queue/status", response_model=QueueStatusResponse)
async def get_queue_status():
    """获取任务队列状态"""
    # 在FastAPI中，我们通常不直接使用队列大小，但这里保留接口
    return {
        "status": "success",
        "queue_size": task_queue.qsize()
    }

# ---------- 后台任务处理 ----------
async def process_stock_task(stock_code: str):
    """处理单个股票的后台任务"""
    await task_queue.put(stock_code)
    logger.info(f"开始处理股票: {stock_code}")
    
    processor = StockProcessor()
    try:
        # 获取基本信息
        basic_info = processor.get_stock_basic_info(stock_code)
        
        if not basic_info:
            logger.error(f"无法获取股票 {stock_code} 基本信息 [ERROR]")
            return
            
        # 获取K线数据
        day_kline = processor.get_kline_data(stock_code, "day", 22)
        month_kline = processor.get_kline_data(stock_code, "month", 24)
        
        # 保存到数据库
        if processor.save_to_database(stock_code, basic_info, day_kline, month_kline):
            logger.info(f"股票 {stock_code} 处理成功 [OK]")
        else:
            logger.error(f"股票 {stock_code} 保存失败 [ERROR]")
        
        # 添加延时
        await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"处理股票失败 [ERROR]: {e}")
        logger.error(traceback.format_exc())
    finally:
        await task_queue.get()
        task_queue.task_done()

# ---------- 生命周期事件 ----------
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    create_tables()
    logger.info("应用启动完成 [OK]")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理"""
    # 等待队列任务完成
    await task_queue.join()
    logger.info("应用安全关闭 [OK]")

# 运行应用
if __name__ == '__main__':
    # 确保日志级别为DEBUG
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG)
    
    uvicorn.run(
        app, 
        host='0.0.0.0', 
        port=5000,
        log_config=None,
        access_log=False
    )