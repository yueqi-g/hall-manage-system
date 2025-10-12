"""
安全相关工具函数：密码哈希、验证等
"""
import hashlib
import secrets


def hash_password(password: str) -> str:
    """
    对密码进行哈希处理
    
    Args:
        password: 原始密码
        
    Returns:
        哈希后的密码字符串
    """
    # 使用SHA-256进行哈希，实际项目中可以考虑使用更安全的算法如bcrypt
    salt = secrets.token_hex(16)  # 生成随机盐值
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    
    # 返回格式: 算法$盐值$哈希值
    return f"sha256${salt}${password_hash}"


def verify_password(password: str, hashed_password: str) -> bool:
    """
    验证密码是否匹配
    
    Args:
        password: 待验证的密码
        hashed_password: 存储的哈希密码
        
    Returns:
        密码是否匹配
    """
    try:
        # 解析哈希密码格式
        parts = hashed_password.split('$')
        if len(parts) != 3:
            return False
        
        algorithm, salt, stored_hash = parts
        
        if algorithm != 'sha256':
            return False
        
        # 计算输入密码的哈希值
        input_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        
        # 使用恒定时间比较防止时序攻击
        return secrets.compare_digest(input_hash, stored_hash)
        
    except Exception:
        return False


def generate_secure_token(length: int = 32) -> str:
    """
    生成安全的随机令牌
    
    Args:
        length: 令牌长度
        
    Returns:
        随机令牌字符串
    """
    return secrets.token_hex(length)
