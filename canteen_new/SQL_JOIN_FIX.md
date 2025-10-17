# SQL JOIN 错误修复

## 错误信息
```
django.db.utils.OperationalError: (1054, "Unknown column 'm.canteen' in 'where clause'")
```

## 发生时间
2025-10-17 17:00:04

## 问题描述

当用户在搜索结果页面使用**食堂筛选**时，后端抛出数据库错误：
- 错误代码：1054
- 错误信息：Unknown column 'm.canteen' in 'where clause'

## 根本原因

在 `canteen_new/data/repositories.py` 的 `search_dishes()` 方法中：

1. **主查询有 LEFT JOIN**：
   ```sql
   SELECT ... FROM dishes d
   LEFT JOIN merchants m ON d.merchant_id = m.id
   WHERE ... -- 可以使用 m.canteen
   ```

2. **COUNT 查询缺少 LEFT JOIN**：
   ```sql
   SELECT COUNT(*) FROM dishes d
   WHERE ... -- 使用了 m.canteen 但没有 JOIN merchants 表 ❌
   ```

当筛选条件包含 `hall` 参数时，WHERE 子句会包含 `m.canteen = '第二食堂'`，但 COUNT 查询没有 JOIN merchants 表，导致 SQL 错误。

## 修复方案

### 修复 1: COUNT 查询添加 LEFT JOIN

**文件**: `canteen_new/data/repositories.py`

**修改前**:
```python
# 获取总数
count_query = f"""
    SELECT COUNT(*) as total
    FROM dishes d
    WHERE {where_clause}
"""
```

**修改后**:
```python
# 获取总数（需要 LEFT JOIN merchants，因为可能有食堂筛选条件）
count_query = f"""
    SELECT COUNT(*) as total
    FROM dishes d
    LEFT JOIN merchants m ON d.merchant_id = m.id
    WHERE {where_clause}
"""
```

### 修复 2: 优化排序选项

增强了排序参数的兼容性，支持更多排序方式：

**修改前**:
```python
if ordering == 'price_asc':
    order_clause = "d.price ASC, d.rating DESC"
elif ordering == 'price_desc':
    order_clause = "d.price DESC, d.rating DESC"
```

**修改后**:
```python
if ordering == 'price' or ordering == 'price_asc':
    order_clause = "d.price ASC, d.rating DESC"
elif ordering == '-price' or ordering == 'price_desc':
    order_clause = "d.price DESC, d.rating DESC"
elif ordering == '-rating' or ordering == 'rating':
    order_clause = "d.rating DESC, d.price ASC"
elif ordering == 'created_at':
    order_clause = "d.id DESC"  # 按创建顺序（ID）降序
```

## 测试验证

### 测试 1: 食堂筛选
```bash
curl "http://localhost:8000/api/dishes/filter?hall=第二食堂"
```

**预期**:
- 不再出现 SQL 错误
- 返回第二食堂的菜品列表

### 测试 2: 组合筛选（包含食堂）
```bash
curl "http://localhost:8000/api/dishes/filter?price_min=10&price_max=30&hall=第一食堂&ordering=price"
```

**预期**:
- 正常执行 SQL 查询
- 返回第一食堂价格在 10-30 元的菜品，按价格升序排列

### 测试 3: 排序功能
```bash
# 价格升序
curl "http://localhost:8000/api/dishes/filter?ordering=price"

# 价格降序
curl "http://localhost:8000/api/dishes/filter?ordering=-price"

# 评分降序
curl "http://localhost:8000/api/dishes/filter?ordering=-rating"

# 最新上架
curl "http://localhost:8000/api/dishes/filter?ordering=created_at"
```

## 相关 SQL 查询

### 完整的 SQL 查询结构

```sql
-- COUNT 查询（修复后）
SELECT COUNT(*) as total
FROM dishes d
LEFT JOIN merchants m ON d.merchant_id = m.id
WHERE d.status = 'active' 
  AND m.canteen = '第二食堂'
  AND d.price >= 10
  AND d.price <= 30;

-- 主查询
SELECT d.id, d.merchant_id, d.name, d.description, d.price, d.category, 
       d.taste, d.spice_level, d.image_url, d.is_available, d.stock_quantity, d.rating,
       m.store_name, m.canteen
FROM dishes d
LEFT JOIN merchants m ON d.merchant_id = m.id
WHERE d.status = 'active' 
  AND m.canteen = '第二食堂'
  AND d.price >= 10
  AND d.price <= 30
ORDER BY d.price ASC, d.rating DESC
LIMIT 100 OFFSET 0;
```

## 为什么需要 LEFT JOIN

1. **表关系**: `dishes.merchant_id` → `merchants.id`
2. **筛选条件**: 当用户选择食堂时，需要通过 `merchants.canteen` 字段筛选
3. **一致性**: COUNT 查询和主查询必须使用相同的 JOIN 结构，确保计数准确

## 学到的教训

1. **查询一致性**: COUNT 查询和主查询应该使用相同的表结构
2. **提前测试**: 当添加新的筛选条件时，应该测试所有相关的 SQL 查询
3. **WHERE 子句检查**: 如果 WHERE 子句引用了某个表的列，确保该表已经 JOIN

## 修改文件

- ✅ `canteen_new/data/repositories.py`
  - 修复 COUNT 查询（添加 LEFT JOIN merchants）
  - 增强排序参数兼容性

## 验证清单

- [x] 食堂筛选不再报错
- [x] COUNT 查询正确返回结果数量
- [x] 主查询正确返回菜品列表
- [x] 排序功能正常工作
- [x] 组合筛选正常工作
- [x] 无 lint 错误

## 相关文档

- [筛选功能完善说明](../canteen_frontend/SEARCH_FILTER_IMPROVEMENTS.md)
- [搜索筛选修复](../canteen_frontend/SEARCH_FILTERS_FIX.md)
- [Bug修复总结](../canteen_frontend/BUGFIX_SUMMARY.md)


