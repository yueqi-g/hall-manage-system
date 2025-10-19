"""
情景数据服务模块
提供天气、节日、用户偏好、客流量等情景数据
"""
import datetime
import os
from typing import List, Dict, Any, Optional
from lunarcalendar import Converter, Solar
import holidays
import requests
from django.conf import settings


class ContextService:
    """情景数据服务类"""
    
    def __init__(self):
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.weather_api_provider = os.getenv('WEATHER_API_PROVIDER', 'gaode')
        self.weather_city = os.getenv('WEATHER_CITY', '北京')
        self.weather_api_url = "https://restapi.amap.com/v3/weather/weatherInfo"
    
    def get_situational_festival_info(self, target_date: datetime.date = None) -> List[str]:
        """
        聚合获取指定日期的中国传统节日、24节气、法定/公共节日等情景信息。
        
        Args:
            target_date: 要查询的日期，默认为今天。
            
        Returns:
            一个包含所有识别出的节日/节气名称的列表。
        """
        if target_date is None:
            target_date = datetime.date.today()
        
        festivals = set()
        year, month, day = target_date.year, target_date.month, target_date.day
        
        # ------------------- A. 农历和 24 节气 (使用 LunarCalendar) -------------------
        try:
            # 1. 构造 Solar 对象 (公历日期)
            current_solar = Solar(year, month, day)
            current_date = datetime.date(year, month, day) # 用于 holidays 库

            # 2. 提取 24 节气信息
            try:
                if hasattr(current_solar, 'solar_term') and current_solar.solar_term:
                    festivals.add(f"节气: {current_solar.solar_term}")
            except AttributeError:
                pass

            # 3. 提取公历节日信息 (LunarCalendar自带的)
            if hasattr(current_solar, 'solar_festival') and current_solar.solar_festival:
                festivals.update(current_solar.solar_festival)

            # 4. 提取农历节日信息 (需要先转换)
            try:
                lunar = Converter.Solar2Lunar(current_solar)
                
                if hasattr(lunar, 'lunar_festival') and lunar.lunar_festival:
                    festivals.update(lunar.lunar_festival)

            except Exception:
                # 农历转换异常处理
                pass
                
        except Exception as e:
            print(f"LunarCalendar 处理异常: {e}")
            pass

        # ------------------- B. 法定/公共节假日 (使用 holidays 库) -------------------
        
        # 使用中国 (CN) 地区设置，获取公共假期
        try:
            cn_holidays = holidays.CountryHoliday('CN', years=year)
            if target_date in cn_holidays:
                festival_name = cn_holidays.get(target_date)
                if festival_name:
                    festivals.add(festival_name)
        except Exception as e:
            print(f"holidays 处理异常: {e}")
            pass

        # ------------------- C. 有趣的/非官方的固定节日 (自定义) -------------------
        
        # 添加一些可能影响心情或饮食倾向的节日
        custom_festivals = {
            (1, 1): "元旦节",
            (2, 14): "情人节",
            (3, 8): "妇女节",
            (3, 15): "消费者权益日",
            (5, 1): "劳动节",
            (6, 1): "儿童节",
            (7, 7): "七夕节",  # 这里的七夕是公历的，农历的已由 LunarCalendar 处理
            (8, 8): "全民健身日",
            (11, 11): "光棍节/购物节",
            (12, 31): "跨年夜"
        }
        
        today_tuple = (month, day)
        if today_tuple in custom_festivals:
            festivals.add(custom_festivals[today_tuple])
        
        # ------------------- D. 趣味信息输出 -------------------
        
        festival_str = "".join(festivals)
        if "立春" in festival_str:
            festivals.add("新岁伊始，宜养肝")
        if "情人节" in festival_str or "七夕" in festival_str:
            festivals.add("浪漫氛围，宜情侣套餐")
        if "冬至" in festival_str:
            festivals.add("冬至进补，宜温补食物")
        if "夏至" in festival_str:
            festivals.add("夏至清热，宜清淡饮食")

        # 如果列表为空，返回一个默认标签
        if not festivals:
            # 判断是否为周末
            if target_date.weekday() >= 5:  # 5=周六, 6=周日
                return ["周末"]
            else:
                return ["普通工作日"]
        
        return sorted(list(festivals))
    
    def get_weather_info(self) -> Dict[str, Any]:
        """
        获取天气信息
        使用高德天气API获取真实天气数据
        
        Returns:
            天气信息字典
        """
        # 如果没有配置天气API密钥，返回空数据
        if not self.weather_api_key:
            print("警告: 未配置天气API密钥，天气数据不可用")
            return {
                "weather": "未知",
                "temperature": 0,
                "season": self._get_season(datetime.date.today()),
                "humidity": 0,
                "wind_level": 0
            }
        
        try:
            # 调用高德天气API
            params = {
                'key': self.weather_api_key,
                'city': self.weather_city,
                'extensions': 'base',  # base: 实时天气, all: 预报天气
                'output': 'JSON'
            }
            
            response = requests.get(self.weather_api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # 检查API返回状态
                if data.get('status') == '1' and data.get('lives'):
                    weather_data = data['lives'][0]
                    
                    # 解析天气数据
                    weather = weather_data.get('weather', '未知')
                    temperature = int(weather_data.get('temperature', 0))
                    humidity = int(weather_data.get('humidity', 0))
                    wind_direction = weather_data.get('winddirection', '未知')
                    wind_power = weather_data.get('windpower', '0级')
                    
                    # 将风力等级转换为数字
                    wind_level = self._convert_wind_power_to_level(wind_power)
                    
                    return {
                        "weather": weather,
                        "temperature": temperature,
                        "season": self._get_season(datetime.date.today()),
                        "humidity": humidity,
                        "wind_level": wind_level,
                        "wind_direction": wind_direction
                    }
                else:
                    print(f"高德天气API返回错误: {data.get('info', '未知错误')}")
                    return self._get_fallback_weather_data()
            else:
                print(f"天气API调用失败: {response.status_code}")
                return self._get_fallback_weather_data()
                
        except Exception as e:
            print(f"天气API调用异常: {e}")
            return self._get_fallback_weather_data()
    
    def _get_fallback_weather_data(self) -> Dict[str, Any]:
        """获取备用天气数据（当API不可用时）"""
        current_season = self._get_season(datetime.date.today())
        
        # 基于季节的合理默认值
        if current_season == "春季":
            temperature = 15
            weather = "多云"
        elif current_season == "夏季":
            temperature = 28
            weather = "晴朗"
        elif current_season == "秋季":
            temperature = 18
            weather = "晴朗"
        else:  # 冬季
            temperature = 5
            weather = "阴天"
        
        return {
            "weather": weather,
            "temperature": temperature,
            "season": current_season,
            "humidity": 65,
            "wind_level": 2
        }
    
    def get_crowd_info(self) -> Dict[str, Any]:
        """
        获取客流量信息
        从数据库获取实时客流量数据
        
        Returns:
            客流量信息字典
        """
        try:
            from data.services import dish_service
            
            # 获取当前时间段的客流量统计
            current_hour = datetime.datetime.now().hour
            current_date = datetime.date.today()
            
            # 从数据库获取实时客流量数据
            crowd_data = dish_service.get_crowd_statistics(current_date, current_hour)
            
            if crowd_data:
                return {
                    "crowd_level": crowd_data.get('crowd_level', '中等'),
                    "avg_wait_time": crowd_data.get('avg_wait_time', 15),
                    "peak_hours": crowd_data.get('peak_hours', [11, 12, 13, 17, 18, 19])
                }
            else:
                # 如果没有数据，基于时间估算
                return self._estimate_crowd_info()
                
        except Exception as e:
            print(f"获取客流量数据失败: {e}")
            return self._estimate_crowd_info()
    
    def _estimate_crowd_info(self) -> Dict[str, Any]:
        """基于时间估算客流量信息"""
        current_hour = datetime.datetime.now().hour
        
        # 基于典型食堂客流模式估算
        if 11 <= current_hour <= 13 or 17 <= current_hour <= 19:
            crowd_level = "高"
            avg_wait_time = 20
        elif 7 <= current_hour <= 10 or 14 <= current_hour <= 16:
            crowd_level = "中等"
            avg_wait_time = 15
        else:
            crowd_level = "低"
            avg_wait_time = 10
        
        return {
            "crowd_level": crowd_level,
            "avg_wait_time": avg_wait_time,
            "peak_hours": [11, 12, 13, 17, 18, 19]
        }
    
    def get_user_preferences(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        获取用户偏好信息
        从数据库获取用户真实的收藏和历史数据
        
        Args:
            user_id: 用户ID，如果为None则返回空偏好
            
        Returns:
            用户偏好信息字典
        """
        if user_id is None:
            # 返回空偏好，让LLM基于情景数据自主推理
            return {
                "preferred_categories": [],
                "preferred_tastes": [],
                "budget_range": [],
                "spice_tolerance": ""
            }
        
        try:
            from data.services import dish_service
            
            # 获取用户真实的收藏数据
            user_favorites = dish_service.get_user_favorites_summary(user_id)
            
            if user_favorites:
                return user_favorites
            else:
                # 如果没有收藏数据，返回空偏好
                return {
                    "preferred_categories": [],
                    "preferred_tastes": [],
                    "budget_range": [],
                    "spice_tolerance": ""
                }
                
        except Exception as e:
            print(f"获取用户偏好失败: {e}")
            return {
                "preferred_categories": [],
                "preferred_tastes": [],
                "budget_range": [],
                "spice_tolerance": ""
            }
    
    def get_all_context_data(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        获取所有情景数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            包含所有情景数据的字典
        """
        current_date = datetime.date.today()
        
        return {
            "date_info": {
                "current_date": current_date.strftime('%Y年%m月%d日'),
                "festival_tags": self.get_situational_festival_info(current_date),
                "is_weekend": current_date.weekday() >= 5,
                "current_season": self._get_season(current_date)
            },
            "weather_info": self.get_weather_info(),
            "crowd_info": self.get_crowd_info(),
            "user_preferences": self.get_user_preferences(user_id)
        }
    
    def _get_season(self, date: datetime.date) -> str:
        """根据日期判断季节"""
        month = date.month
        if month in [3, 4, 5]:
            return "春季"
        elif month in [6, 7, 8]:
            return "夏季"
        elif month in [9, 10, 11]:
            return "秋季"
        else:
            return "冬季"
    
    def _convert_wind_speed_to_level(self, wind_speed: float) -> int:
        """将风速(m/s)转换为风力等级"""
        if wind_speed < 0.3:
            return 0
        elif wind_speed < 1.6:
            return 1
        elif wind_speed < 3.4:
            return 2
        elif wind_speed < 5.5:
            return 3
        elif wind_speed < 8.0:
            return 4
        elif wind_speed < 10.8:
            return 5
        elif wind_speed < 13.9:
            return 6
        elif wind_speed < 17.2:
            return 7
        elif wind_speed < 20.8:
            return 8
        elif wind_speed < 24.5:
            return 9
        elif wind_speed < 28.5:
            return 10
        elif wind_speed < 32.7:
            return 11
        else:
            return 12
    
    def _convert_wind_power_to_level(self, wind_power: str) -> int:
        """将高德天气的风力描述转换为风力等级"""
        # 高德天气返回的风力格式如："3-4级", "5-6级", "微风"等
        if not wind_power or wind_power == '微风':
            return 1
        
        # 提取数字部分
        import re
        numbers = re.findall(r'\d+', wind_power)
        if numbers:
            # 取第一个数字作为风力等级
            return int(numbers[0])
        else:
            return 1


# 测试函数
def test_context_service():
    """测试情景数据服务"""
    service = ContextService()
    
    print("=== 情景数据服务测试 ===")
    
    # 测试节日信息
    today = datetime.date.today()
    festival_info = service.get_situational_festival_info(today)
    print(f"今天({today})的节日标签: {festival_info}")
    
    # 测试天气信息
    weather_info = service.get_weather_info()
    print(f"天气信息: {weather_info}")
    
    # 测试客流量信息
    crowd_info = service.get_crowd_info()
    print(f"客流量信息: {crowd_info}")
    
    # 测试用户偏好
    user_prefs = service.get_user_preferences(1)
    print(f"用户偏好: {user_prefs}")
    
    # 测试所有情景数据
    context_data = service.get_all_context_data()
    print(f"完整情景数据: {context_data}")


if __name__ == "__main__":
    test_context_service()
