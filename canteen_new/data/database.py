"""
数据库连接和工具函数
使用Django的数据库连接
"""
from typing import Dict, Any, List, Optional
from django.db import connection


def execute_raw_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """
    执行原始SQL查询
    
    Args:
        query: SQL查询语句
        params: 查询参数
        
    Returns:
        查询结果列表
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params or ())
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


def execute_raw_update(query: str, params: tuple = None) -> int:
    """
    执行原始SQL更新操作
    
    Args:
        query: SQL更新语句
        params: 更新参数
        
    Returns:
        受影响的行数
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.rowcount


def execute_raw_insert(query: str, params: tuple = None) -> int:
    """
    执行原始SQL插入操作
    
    Args:
        query: SQL插入语句
        params: 插入参数
        
    Returns:
        插入的ID
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.lastrowid


# 便捷函数
def query_one(query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
    """查询单条记录"""
    results = execute_raw_query(query, params)
    return results[0] if results else None


def query_all(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """查询多条记录"""
    return execute_raw_query(query, params)


def execute_update(query: str, params: tuple = None) -> int:
    """执行更新操作"""
    return execute_raw_update(query, params)


def execute_insert(query: str, params: tuple = None) -> int:
    """执行插入操作并返回ID"""
    return execute_raw_insert(query, params)
