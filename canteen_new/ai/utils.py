"""
AI工具函数模块
定义AI模型可调用的工具函数Schema
"""
from typing import Dict, Any, List, Optional


def get_dishes_by_criteria(
    name: str = None,
    category: str = None,
    taste: str = None,
    min_price: float = None,
    max_price: float = None,
    min_rating: float = None,
    spice_level: int = None,
    sort_by: str = None,
    limit: int = 10,
    max_wait_time: int = None,
    crowd_level: str = None
) -> List[Dict[str, Any]]:
    """
    根据多种条件查询菜品，支持等待时间和客流级别筛选
    
    Args:
        name: 菜品名称关键词，支持模糊匹配
        category: 菜品分类：饭、面、饺子、其他
        taste: 口味偏好：辣、咸、淡、酸甜
        min_price: 最低价格，单位：元
        max_price: 最高价格，单位：元
        min_rating: 最低评分，范围0.0-5.0
        spice_level: 辣度级别，整数值0到5，0为不辣，5为特辣
        sort_by: 排序方式：rating(评分)、price_asc(价格升序)、price_desc(价格降序)、created_at(最新)
        limit: 返回结果数量限制，默认10，最大50
        max_wait_time: 最大等待时间（分钟），用于筛选出餐快的菜品
        crowd_level: 客流级别：低、中等、高，用于推荐等待时间合适的菜品
    
    Returns:
        符合条件的菜品列表
    """
    print(f"\n=== 工具函数调试信息 ===")
    print(f"接收参数: name={name}, category={category}, taste={taste}, min_price={min_price}, max_price={max_price}, min_rating={min_rating}, spice_level={spice_level}, sort_by={sort_by}, limit={limit}")
    
    from data.services import dish_service
    
    # 构建查询条件
    criteria = {}
    if name:
        criteria['name'] = name
    if category:
        criteria['category'] = category
    if taste:
        criteria['taste'] = taste
    if min_price is not None:
        criteria['priceMin'] = min_price
    if max_price is not None:
        criteria['priceMax'] = max_price
    if spice_level is not None:
        criteria['spice_level'] = spice_level
    if sort_by:
        criteria['ordering'] = sort_by
    
    print(f"构建的查询条件: {criteria}")
    
    # 执行查询
    print("调用dish_service.filter_dishes_service...")
    result = dish_service.filter_dishes_service(criteria)
    dishes = result.get('dishes', [])
    print(f"查询结果: 获取到 {len(dishes)} 个菜品")
    
    # 显示前几个菜品信息用于调试
    for i, dish in enumerate(dishes[:3]):
        print(f"菜品 {i+1}: {dish.get('name')} - ¥{dish.get('price')} - {dish.get('taste')} - 评分: {dish.get('rating')}")
    
    # 应用评分筛选
    if min_rating is not None:
        print(f"应用评分筛选: min_rating={min_rating}")
        dishes = [dish for dish in dishes if dish.get('rating', 0) >= min_rating]
        print(f"评分筛选后: {len(dishes)} 个菜品")
    
    # 应用数量限制
    if limit and len(dishes) > limit:
        print(f"应用数量限制: limit={limit}")
        dishes = dishes[:limit]
        print(f"限制后: {len(dishes)} 个菜品")
    
    print(f"最终返回: {len(dishes)} 个菜品")
    return dishes


# 工具函数Schema定义（符合OpenAI Function Calling规范）
GET_DISHES_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_dishes_by_criteria",
        "description": "根据用户需求查询符合条件的菜品，支持等待时间和客流级别筛选",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "菜品名称关键词，支持模糊匹配"
                },
                "category": {
                    "type": "string", 
                    "description": "菜品分类：饭、面、饺子、其他"
                },
                "taste": {
                    "type": "string",
                    "description": "口味偏好：辣、咸、淡、酸甜"
                },
                "min_price": {
                    "type": "number",
                    "description": "最低价格，单位：元"
                },
                "max_price": {
                    "type": "number", 
                    "description": "最高价格，单位：元"
                },
                "min_rating": {
                    "type": "number",
                    "description": "最低评分，范围0.0-5.0"
                },
                "spice_level": {
                    "type": "integer",
                    "description": "辣度级别，整数值0到5，0为不辣，5为特辣"
                },
                "sort_by": {
                    "type": "string",
                    "description": "排序方式：rating(评分)、price_asc(价格升序)、price_desc(价格降序)、created_at(最新)"
                },
                "limit": {
                    "type": "integer", 
                    "description": "返回结果数量限制，默认10，最大50"
                },
                "max_wait_time": {
                    "type": "integer",
                    "description": "最大等待时间（分钟），用于筛选出餐快的菜品"
                },
                "crowd_level": {
                    "type": "string",
                    "description": "客流级别：低、中等、高，用于推荐等待时间合适的菜品"
                }
            },
            "required": []  # 所有参数均为可选
        }
    }
}


def validate_tool_arguments(tool_args: Dict) -> Dict:
    """
    验证工具函数参数的有效性
    
    Args:
        tool_args: 原始工具函数参数
        
    Returns:
        验证后的参数
    """
    validated_args = {}
    
    # 数值有效性检查
    if tool_args.get('min_price') and tool_args.get('max_price'):
        if tool_args['min_price'] > tool_args['max_price']:
            # 交换价格范围
            tool_args['min_price'], tool_args['max_price'] = tool_args['max_price'], tool_args['min_price']
    
    # 价格范围限制
    if tool_args.get('min_price') and tool_args['min_price'] < 0:
        tool_args['min_price'] = 0
    if tool_args.get('max_price') and tool_args['max_price'] > 1000:
        tool_args['max_price'] = 1000
    
    # 枚举值验证
    valid_categories = ['饭', '面', '饺子', '其他']
    if tool_args.get('category') and tool_args['category'] not in valid_categories:
        # 记录警告但不阻止查询
        print(f"警告：无效的分类值: {tool_args['category']}")
        del tool_args['category']
    
    valid_tastes = ['辣', '咸', '淡', '酸甜']
    if tool_args.get('taste') and tool_args['taste'] not in valid_tastes:
        print(f"警告：无效的口味值: {tool_args['taste']}")
        del tool_args['taste']
    
    # 辣度范围限制
    if tool_args.get('spice_level'):
        spice_level = tool_args['spice_level']
        if spice_level < 0:
            tool_args['spice_level'] = 0
        elif spice_level > 5:
            tool_args['spice_level'] = 5
    
    # 结果数量限制
    if tool_args.get('limit'):
        limit = tool_args['limit']
        if limit < 1:
            tool_args['limit'] = 1
        elif limit > 50:
            tool_args['limit'] = 50
    
    # 过滤空参数
    validated_args = {k: v for k, v in tool_args.items() if v is not None}
    
    return validated_args
