"""Test cases for cache utilities."""
import time
import pytest
from src.utils.cache import Cache, cached

def test_cache_set_get():
    """测试缓存的设置和获取."""
    cache = Cache(ttl=1)
    
    # 设置缓存
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    
    # 不存在的键
    assert cache.get("key2") is None

def test_cache_ttl():
    """测试缓存过期."""
    cache = Cache(ttl=1)
    
    # 设置缓存
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    
    # 等待过期
    time.sleep(1.1)
    assert cache.get("key1") is None

def test_cache_custom_ttl():
    """测试自定义TTL."""
    cache = Cache(ttl=10)
    
    # 使用自定义TTL
    cache.set("key1", "value1", ttl=1)
    assert cache.get("key1") == "value1"
    
    # 等待过期
    time.sleep(1.1)
    assert cache.get("key1") is None

def test_cache_delete():
    """测试缓存删除."""
    cache = Cache()
    
    # 设置并删除
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    
    cache.delete("key1")
    assert cache.get("key1") is None
    
    # 删除不存在的键
    cache.delete("key2")  # 不应抛出异常

def test_cache_clear():
    """测试缓存清空."""
    cache = Cache()
    
    # 设置多个缓存项
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    
    # 清空缓存
    cache.clear()
    
    assert cache.get("key1") is None
    assert cache.get("key2") is None

def test_cache_decorator():
    """测试缓存装饰器."""
    cache = Cache()
    call_count = 0
    
    @cached(cache, key_prefix="test")
    def example_function(arg1, arg2=None):
        nonlocal call_count
        call_count += 1
        return f"{arg1}-{arg2}"
    
    # 第一次调用
    result1 = example_function("a", arg2="b")
    assert result1 == "a-b"
    assert call_count == 1
    
    # 第二次调用（应该从缓存获取）
    result2 = example_function("a", arg2="b")
    assert result2 == "a-b"
    assert call_count == 1  # 计数器不应增加
    
    # 不同参数的调用
    result3 = example_function("c", arg2="d")
    assert result3 == "c-d"
    assert call_count == 2  # 计数器应增加

def test_cache_decorator_ttl():
    """测试缓存装饰器的TTL."""
    cache = Cache()
    call_count = 0
    
    @cached(cache, key_prefix="test", ttl=1)
    def example_function():
        nonlocal call_count
        call_count += 1
        return "result"
    
    # 第一次调用
    result1 = example_function()
    assert result1 == "result"
    assert call_count == 1
    
    # 等待过期
    time.sleep(1.1)
    
    # 第二次调用（缓存应该已过期）
    result2 = example_function()
    assert result2 == "result"
    assert call_count == 2

def test_cache_key_generation():
    """测试缓存键生成."""
    cache = Cache()
    
    @cached(cache, key_prefix="test")
    def example_function(arg1, arg2=None):
        return f"{arg1}-{arg2}"
    
    # 测试不同参数组合生成不同的键
    example_function("a", arg2="b")
    example_function("c", arg2="d")
    
    # 检查缓存中的键
    assert len(cache._cache) == 2  # 应该有两个不同的键

def test_cache_key_long_args():
    """测试长参数的缓存键生成."""
    cache = Cache()
    long_string = "x" * 1000  # 生成一个很长的字符串
    
    @cached(cache, key_prefix="test")
    def example_function(arg):
        return arg[:10]
    
    # 使用长参数调用
    result = example_function(long_string)
    assert result == long_string[:10]
    
    # 检查缓存键是否被哈希处理
    assert any(len(key) < 300 for key in cache._cache.keys())