"""
数据模块应用配置
"""
from django.apps import AppConfig


class DataConfig(AppConfig):
    """数据模块配置"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data'
    
    def ready(self):
        """应用启动时执行"""
        # 导入数据库初始化
        try:
            from .database_init import initialize_database_on_startup, insert_sample_data_on_startup
            
            # 初始化数据库表
            if initialize_database_on_startup():
                print("数据库表初始化成功")
                
                # 插入示例数据
                if insert_sample_data_on_startup():
                    print("示例数据插入成功")
                else:
                    print("示例数据插入失败或已存在数据")
            else:
                print("数据库表初始化失败")
                
        except Exception as e:
            print(f"数据库初始化过程中出现错误: {e}")
