"""Cache utilities."""
import time
import hashlib
import json
from typing import Any, Dict, Optional, Tuple
from functools import wraps

class Cache:
    """简单的内存缓存实现.
    
    使用字典存储缓存数据，支持TTL（生存时间）。
    
    Attributes:
        _cache: 缓存数据字典
        _ttl: 缓存项的默认生存时间（秒）
    """
    
    def __init__(self, ttl: int = 3600):
        """初始化缓存.
        
        Args:
            ttl: 缓存项的默认生存时间（秒），默认1小时
        """
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存项.
        
        Args:
            key: 缓存键
            
        Returns:
            Any: 缓存值，如果不存在或已过期则返回None
        """
        if key not in self._cache:
            return None
            
        value, expire_time = self._cache[key]
        if time.time() > expire_time:
            del self._cache[key]
            return None
            
        return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """设置缓存项.
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: 该项的生存时间（秒），如果为None则使用默认值
        """
        expire_time = time.time() + (ttl or self._ttl)
        self._cache[key] = (value, expire_time)
    
    def delete(self, key: str) -> None:
        """删除缓存项.
        
        Args:
            key: 缓存键
        """
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """清空缓存."""
        self._cache.clear()

def _generate_cache_key(prefix: str, func_name: str, args: tuple, kwargs: dict) -> str:
    """生成缓存键.
    
    Args:
        prefix: 键前缀
        func_name: 函数名
        args: 位置参数
        kwargs: 关键字参数
        
    Returns:
        str: 缓存键
    """
    # 将参数转换为字符串
    args_str = [str(arg) for arg in args[1:]]  # 跳过self参数
    kwargs_str = [f"{k}={v}" for k, v in sorted(kwargs.items())]
    
    # 组合所有部分
    key_parts = [prefix, func_name] + args_str + kwargs_str
    
    # 使用冒号连接
    key = ":".join(key_parts)
    
    # 如果键太长，使用哈希
    if len(key) > 250:
        key = f"{prefix}:{func_name}:{hashlib.md5(key.encode()).hexdigest()}"
    
    return key

def cached(cache: Cache, key_prefix: str = "", ttl: Optional[int] = None):
    """缓存装饰器.
    
    用于缓存函数调用结果。缓存键由前缀和函数参数组成。
    
    Args:
        cache: 缓存实例
        key_prefix: 缓存键前缀
        ttl: 缓存生存时间（秒）
        
    Returns:
        函数装饰器
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = _generate_cache_key(
                key_prefix,
                func.__name__,
                args,
                kwargs
            )
            
            # 尝试从缓存获取
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 调用原函数
            result = func(*args, **kwargs)
            
            # 存入缓存
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator